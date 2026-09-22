"""Small evaluation helpers for relationship reconstruction."""

from __future__ import annotations

from dataclasses import dataclass

from .signals import RelationshipSignal


@dataclass(frozen=True)
class SignalMetrics:
    expected_pairs: int
    recovered_pairs: int
    false_pairs: int

    @property
    def pair_recall(self) -> float:
        return self.recovered_pairs / self.expected_pairs if self.expected_pairs else 1.0

    @property
    def pair_precision(self) -> float:
        observed_pairs = self.recovered_pairs + self.false_pairs
        return self.recovered_pairs / observed_pairs if observed_pairs else 1.0


def evaluate_candidate_pairs(
    signals: tuple[RelationshipSignal, ...],
    expected_edges: list[dict],
) -> SignalMetrics:
    """Evaluate only whether a candidate pair was surfaced.

    This deliberately does not award credit for predicting edge semantics.
    """
    expected = {(item["source"], item["target"]) for item in expected_edges}
    observed = {(item.source, item.target) for item in signals}
    return SignalMetrics(
        expected_pairs=len(expected),
        recovered_pairs=len(expected & observed),
        false_pairs=len(observed - expected),
    )
