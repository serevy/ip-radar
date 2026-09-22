import pytest

from ip_radar.reasoning import (
    Relationship,
    ReasoningResult,
    conservative_baseline,
)


def test_semantic_edge_requires_evidence():
    result = ReasoningResult(
        relationship=Relationship.REFINES,
        evidence=(),
        rationale="looks related",
    )

    with pytest.raises(ValueError, match="explicit evidence"):
        result.validate()


def test_unknown_is_first_class_and_must_explain_uncertainty():
    result = conservative_baseline(explicit_reference=True, shared_paths=True)

    result.validate()
    assert result.relationship is Relationship.UNKNOWN
    assert "explicit PR reference exists" in result.evidence
    assert result.missing_evidence


def test_unknown_without_missing_or_conflicting_evidence_is_invalid():
    result = ReasoningResult(
        relationship=Relationship.UNKNOWN,
        evidence=("same file",),
    )

    with pytest.raises(ValueError, match="missing or conflicting"):
        result.validate()
