from datetime import datetime, timezone

import pytest

from ip_radar import Artifact, EdgeKind, EvidenceEdge, TemporalEvidenceGraph


def at(hour: int) -> datetime:
    return datetime(2026, 9, 21, hour, tzinfo=timezone.utc)


def test_timeline_is_deterministic():
    graph = TemporalEvidenceGraph()
    graph.add_artifact(Artifact("pr-4", "pull_request", at(4), "repair"))
    graph.add_artifact(Artifact("pr-3", "pull_request", at(3), "detect"))

    assert [item.id for item in graph.timeline()] == ["pr-3", "pr-4"]


def test_edges_require_known_endpoints():
    graph = TemporalEvidenceGraph()
    graph.add_artifact(Artifact("pr-3", "pull_request", at(3), "detect"))

    with pytest.raises(ValueError, match="endpoints"):
        graph.add_edge(EvidenceEdge("pr-3", "pr-4", EdgeKind.RESPONDS_TO, "dogfood failure"))


def test_precedes_edge_cannot_run_backwards():
    graph = TemporalEvidenceGraph()
    graph.add_artifact(Artifact("later", "pull_request", at(4), "later"))
    graph.add_artifact(Artifact("earlier", "pull_request", at(3), "earlier"))
    graph.add_edge(EvidenceEdge("later", "earlier", EdgeKind.PRECEDES, "invalid fixture"))

    assert graph.validate_temporal_edges()
