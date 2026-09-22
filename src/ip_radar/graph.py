"""Minimal temporal evidence graph for the first archaeology PoC."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EdgeKind(str, Enum):
    PRECEDES = "precedes"
    REFERENCES = "references"
    RESPONDS_TO = "responds_to"
    REFINES = "refines"
    CONTRADICTS = "contradicts"
    VALIDATES = "validates"


@dataclass(frozen=True)
class Artifact:
    id: str
    kind: str
    occurred_at: datetime
    title: str
    source_url: str | None = None


@dataclass(frozen=True)
class EvidenceEdge:
    source: str
    target: str
    kind: EdgeKind
    rationale: str


class TemporalEvidenceGraph:
    """Small deterministic graph; inference belongs in later layers."""

    def __init__(self) -> None:
        self._artifacts: dict[str, Artifact] = {}
        self._edges: list[EvidenceEdge] = []

    def add_artifact(self, artifact: Artifact) -> None:
        if artifact.id in self._artifacts:
            raise ValueError(f"duplicate artifact id: {artifact.id}")
        self._artifacts[artifact.id] = artifact

    def add_edge(self, edge: EvidenceEdge) -> None:
        if edge.source not in self._artifacts or edge.target not in self._artifacts:
            raise ValueError("edge endpoints must exist before the edge is added")
        if edge.source == edge.target:
            raise ValueError("self edges are not allowed")
        self._edges.append(edge)

    def timeline(self) -> tuple[Artifact, ...]:
        return tuple(
            sorted(self._artifacts.values(), key=lambda item: (item.occurred_at, item.id))
        )

    def edges(self) -> tuple[EvidenceEdge, ...]:
        return tuple(self._edges)

    def validate_temporal_edges(self) -> tuple[str, ...]:
        """Report explicit PRECEDES edges that contradict artifact timestamps."""
        errors: list[str] = []
        for edge in self._edges:
            if edge.kind is not EdgeKind.PRECEDES:
                continue
            source = self._artifacts[edge.source]
            target = self._artifacts[edge.target]
            if source.occurred_at > target.occurred_at:
                errors.append(
                    f"{edge.source} cannot precede {edge.target}: "
                    f"{source.occurred_at.isoformat()} > {target.occurred_at.isoformat()}"
                )
        return tuple(errors)
