"""Fixture loading for reproducible archaeology evaluations."""

from __future__ import annotations

import json
from pathlib import Path

from .github import pull_request_artifact
from .graph import EdgeKind, EvidenceEdge, TemporalEvidenceGraph


def graph_from_github_fixture(path: str | Path) -> TemporalEvidenceGraph:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("freeze", {}).get("future_artifacts_allowed") is not False:
        raise ValueError("evaluation fixture must explicitly forbid future artifacts")

    graph = TemporalEvidenceGraph()
    for payload in data.get("github_pull_requests", []):
        graph.add_artifact(pull_request_artifact(payload))

    for item in data.get("expected_edges", []):
        graph.add_edge(
            EvidenceEdge(
                source=item["source"],
                target=item["target"],
                kind=EdgeKind(item["kind"]),
                rationale=item["rationale"],
            )
        )
    return graph
