from ip_radar.reasoning import Relationship
from ip_radar.semantic_baseline import infer_from_text


def test_sparse_shared_path_stays_unknown():
    result = infer_from_text(
        source_id="change-a",
        target_id="change-b",
        target_text="Namespace cleanup",
        explicit_reference=False,
        shared_paths=True,
    )

    result.validate()
    assert result.relationship is Relationship.UNKNOWN


def test_explicit_failure_response_can_be_classified():
    result = infer_from_text(
        source_id="pr-4",
        target_id="pr-5",
        target_text=(
            "Related: #4. The previous repair failed because it repeated the same "
            "prompt. This change fixes the failure with a dedicated repair prompt."
        ),
        explicit_reference=True,
        shared_paths=True,
    )

    result.validate()
    assert result.relationship is Relationship.RESPONDS_TO


def test_reference_without_causal_language_stays_unknown():
    result = infer_from_text(
        source_id="pr-7",
        target_id="pr-8",
        target_text="Related: #7",
        explicit_reference=True,
        shared_paths=False,
    )

    result.validate()
    assert result.relationship is Relationship.UNKNOWN
