"""LLM semantic provider with an injected transport.

The provider owns the prompt/schema boundary but not network credentials or
vendor SDKs. Callers inject a transport that accepts a JSON-serializable
request and returns a decoded object.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .providers import SemanticRequest
from .reasoning import Relationship, ReasoningResult


Transport = Callable[[dict[str, Any]], dict[str, Any]]


SYSTEM_INSTRUCTIONS = """You classify relationships between two development artifacts.
Use only the supplied evidence. Do not infer legal novelty or patentability.
Return unknown when the evidence does not establish a direct semantic relationship.
An explicit reference or shared file path alone is not enough.
Allowed relationships: refines, responds_to, contradicts, validates, unknown.
For non-unknown results, cite concrete supplied evidence.
For unknown results, explain missing or conflicting evidence.
"""


class LLMSemanticProvider:
    def __init__(self, transport: Transport, *, model: str) -> None:
        self._transport = transport
        self._model = model

    @property
    def name(self) -> str:
        return f"llm:{self._model}"

    def infer(self, request: SemanticRequest) -> ReasoningResult:
        payload = {
            "model": self._model,
            "system": SYSTEM_INSTRUCTIONS,
            "input": {
                "source_id": request.source_id,
                "target_id": request.target_id,
                "target_text": request.target_text,
                "signals": {
                    "explicit_reference": request.explicit_reference,
                    "shared_paths": request.shared_paths,
                },
            },
            "response_schema": {
                "relationship": [item.value for item in Relationship],
                "evidence": "array[string]",
                "counter_evidence": "array[string]",
                "missing_evidence": "array[string]",
                "rationale": "string",
            },
        }
        raw = self._transport(payload)
        result = _decode_result(raw)
        result.validate()
        return result


def _strings(raw: Any, field: str) -> tuple[str, ...]:
    value = raw.get(field, [])
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise ValueError(f"{field} must be an array of non-empty strings")
    return tuple(item.strip() for item in value)


def _decode_result(raw: dict[str, Any]) -> ReasoningResult:
    if not isinstance(raw, dict):
        raise ValueError("provider response must be an object")
    try:
        relationship = Relationship(raw["relationship"])
    except (KeyError, ValueError, TypeError) as exc:
        raise ValueError("provider returned an invalid relationship") from exc

    rationale = raw.get("rationale", "")
    if not isinstance(rationale, str):
        raise ValueError("rationale must be a string")

    return ReasoningResult(
        relationship=relationship,
        evidence=_strings(raw, "evidence"),
        counter_evidence=_strings(raw, "counter_evidence"),
        missing_evidence=_strings(raw, "missing_evidence"),
        rationale=rationale.strip(),
    )
