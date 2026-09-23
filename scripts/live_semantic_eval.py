#!/usr/bin/env python3
"""Manual live semantic evaluation against OpenAI Responses API."""

from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from ip_radar.llm_provider import LLMSemanticProvider
from ip_radar.providers import SemanticRequest
from ip_radar.reasoning import Relationship


ENDPOINT = "https://api.openai.com/v1/responses"
ALLOWED_HOST = "api.openai.com"
TIMEOUT_SECONDS = 30
MAX_RESPONSE_BYTES = 256_000


CASES = (
    (
        "rich-refinement",
        SemanticRequest(
            source_id="pr-6",
            target_id="pr-8",
            target_text=(
                "#8 states that after #6 identity terms were masked, the translator "
                "glossary still allowed case-insensitive leak-through. It separates "
                "identity preservation from translation glossary enforcement."
            ),
            explicit_reference=True,
            shared_paths=True,
        ),
        frozenset({Relationship.REFINES, Relationship.RESPONDS_TO}),
    ),
    (
        "related-only",
        SemanticRequest(
            source_id="pr-7",
            target_id="pr-8",
            target_text="Related context: #7.",
            explicit_reference=True,
            shared_paths=False,
        ),
        frozenset({Relationship.UNKNOWN}),
    ),
    (
        "sparse-shared-path",
        SemanticRequest(
            source_id="change-a",
            target_id="change-b",
            target_text="Namespace cleanup",
            explicit_reference=False,
            shared_paths=True,
        ),
        frozenset({Relationship.UNKNOWN}),
    ),
)


def _extract_output_text(response: dict) -> str:
    for item in response.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return content["text"]
    raise ValueError("Responses API returned no output_text")


def openai_transport(payload: dict) -> dict:
    key = os.environ["OPENAI_API_KEY"]
    endpoint = os.environ.get("IP_RADAR_OPENAI_ENDPOINT", ENDPOINT)
    parsed = urlparse(endpoint)
    if parsed.scheme != "https" or parsed.hostname != ALLOWED_HOST:
        raise ValueError("live evaluation endpoint is not allowlisted")
    if parsed.path != "/v1/responses" or parsed.query or parsed.fragment:
        raise ValueError("live evaluation endpoint path must be /v1/responses")

    schema = {
        "type": "object",
        "properties": {
            "relationship": {
                "type": "string",
                "enum": payload["response_schema"]["relationship"],
            },
            "evidence": {"type": "array", "items": {"type": "string"}},
            "counter_evidence": {"type": "array", "items": {"type": "string"}},
            "missing_evidence": {"type": "array", "items": {"type": "string"}},
            "rationale": {"type": "string"},
        },
        "required": [
            "relationship",
            "evidence",
            "counter_evidence",
            "missing_evidence",
            "rationale",
        ],
        "additionalProperties": False,
    }
    body = json.dumps(
        {
            "model": payload["model"],
            "instructions": payload["system"],
            "input": json.dumps(payload["input"], ensure_ascii=False),
            "tools": [],
            "store": False,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "semantic_relationship",
                    "strict": True,
                    "schema": schema,
                }
            },
        }
    ).encode()

    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "ip-radar-live-eval/0.0",
        },
    )

    # urllib does not follow POST 30x as a same-method API request; explicitly
    # reject any redirect response rather than relying on implicit behavior.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            raise urllib.error.HTTPError(newurl, code, "redirect rejected", headers, fp)

    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ssl.create_default_context()),
        NoRedirect(),
    )
    with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
        raw = response.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ValueError("provider response exceeded size limit")
    decoded = json.loads(raw)
    return json.loads(_extract_output_text(decoded))


def main() -> int:
    model = os.environ.get("IP_RADAR_LIVE_MODEL", "gpt-5.6-luna")
    provider = LLMSemanticProvider(openai_transport, model=model)
    results = []
    started = time.perf_counter()

    for name, request, accepted in CASES:
        case_start = time.perf_counter()
        result = provider.infer(request)
        elapsed_ms = round((time.perf_counter() - case_start) * 1000, 2)
        results.append(
            {
                "case": name,
                "relationship": result.relationship.value,
                "accepted": result.relationship in accepted,
                "evidence": list(result.evidence),
                "counter_evidence": list(result.counter_evidence),
                "missing_evidence": list(result.missing_evidence),
                "rationale": result.rationale,
                "latency_ms": elapsed_ms,
            }
        )

    report = {
        "provider": provider.name,
        "cases": results,
        "accepted": sum(item["accepted"] for item in results),
        "false_positive_edges": sum(
            item["case"] in {"related-only", "sparse-shared-path"}
            and item["relationship"] != "unknown"
            for item in results
        ),
        "total_latency_ms": round((time.perf_counter() - started) * 1000, 2),
    }
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/live-semantic-eval.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["accepted"] == len(CASES) and report["false_positive_edges"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
