from ip_radar.grounding import verify_evidence_labels
from ip_radar.reasoning import Relationship, ReasoningResult
from ip_radar.security import EvidenceEnvelope, minimize


def test_minimize_bounds_external_disclosure():
    result = minimize(
        EvidenceEnvelope(
            source_id="a",
            target_id="b",
            text="x" * 100,
            explicit_reference=True,
            shared_paths=False,
        ),
        max_chars=20,
    )

    assert len(result.envelope.text) == 20
    assert result.events[0].code == "EVIDENCE_TRUNCATED"


def test_grounding_rejects_model_invented_evidence_label():
    result = ReasoningResult(
        relationship=Relationship.REFINES,
        evidence=("ev-real", "ev-invented"),
        rationale="model output",
    )

    check = verify_evidence_labels(result, ("ev-real",))

    assert check.accepted is False
    assert check.missing_evidence == ("ev-invented",)
