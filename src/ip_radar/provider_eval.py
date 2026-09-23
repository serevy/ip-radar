"""Evaluation helpers shared by semantic providers."""

from __future__ import annotations

from dataclasses import dataclass

from .providers import SemanticProvider, SemanticRequest
from .reasoning import Relationship


@dataclass(frozen=True)
class SemanticCase:
    request: SemanticRequest
    accepted_relationships: frozenset[Relationship]


@dataclass(frozen=True)
class SemanticMetrics:
    cases: int
    accepted: int
    false_positive_edges: int
    abstentions: int

    @property
    def accepted_rate(self) -> float:
        return self.accepted / self.cases if self.cases else 1.0


def evaluate_provider(
    provider: SemanticProvider,
    cases: tuple[SemanticCase, ...],
) -> SemanticMetrics:
    accepted = 0
    false_positive_edges = 0
    abstentions = 0

    for case in cases:
        result = provider.infer(case.request)
        result.validate()
        if result.relationship in case.accepted_relationships:
            accepted += 1
        if result.relationship is Relationship.UNKNOWN:
            abstentions += 1
        if (
            case.accepted_relationships == frozenset({Relationship.UNKNOWN})
            and result.relationship is not Relationship.UNKNOWN
        ):
            false_positive_edges += 1

    return SemanticMetrics(
        cases=len(cases),
        accepted=accepted,
        false_positive_edges=false_positive_edges,
        abstentions=abstentions,
    )
