"""Ground semantic results in the evidence actually disclosed to a provider."""

from __future__ import annotations

from dataclasses import dataclass

from .reasoning import ReasoningResult


@dataclass(frozen=True)
class GroundingCheck:
    accepted: bool
    missing_evidence: tuple[str, ...]


def verify_evidence_labels(
    result: ReasoningResult,
    allowed_evidence: tuple[str, ...],
) -> GroundingCheck:
    """Require model evidence labels to come from the supplied evidence catalog.

    Live providers should receive opaque evidence IDs/snippets and return those
    IDs. Free-form model claims are not accepted as provenance.
    """
    allowed = set(allowed_evidence)
    missing = tuple(item for item in result.evidence if item not in allowed)
    return GroundingCheck(accepted=not missing, missing_evidence=missing)
