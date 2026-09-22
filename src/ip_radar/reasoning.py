"""Semantic relationship contract.

The contract is intentionally provider-neutral. A future LLM or agent may
implement it, but cannot bypass evidence requirements by returning a label.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Relationship(str, Enum):
    REFINES = "refines"
    RESPONDS_TO = "responds_to"
    CONTRADICTS = "contradicts"
    VALIDATES = "validates"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ReasoningResult:
    relationship: Relationship
    evidence: tuple[str, ...]
    counter_evidence: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
    rationale: str = ""

    def validate(self) -> None:
        if self.relationship is not Relationship.UNKNOWN and not self.evidence:
            raise ValueError("semantic relationships require explicit evidence")
        if self.relationship is Relationship.UNKNOWN and not (
            self.missing_evidence or self.counter_evidence
        ):
            raise ValueError(
                "unknown must explain missing or conflicting evidence"
            )


def conservative_baseline(
    *,
    explicit_reference: bool = False,
    shared_paths: bool = False,
) -> ReasoningResult:
    """Baseline that never invents semantic meaning from structural signals."""
    observed: list[str] = []
    if explicit_reference:
        observed.append("explicit PR reference exists")
    if shared_paths:
        observed.append("changed paths overlap")

    return ReasoningResult(
        relationship=Relationship.UNKNOWN,
        evidence=tuple(observed),
        missing_evidence=(
            "no semantic evidence establishing refinement, response, "
            "contradiction, or validation",
        ),
        rationale="structural relationship signals are insufficient on their own",
    )
