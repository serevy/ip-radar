import pytest

from ip_radar.llm_provider import LLMSemanticProvider
from ip_radar.providers import SemanticRequest
from ip_radar.reasoning import Relationship


REQUEST = SemanticRequest(
    source_id="pr-6",
    target_id="pr-8",
    target_text=(
        "#8 explicitly says that after #6 identity terms were masked, "
        "the glossary leak-through path still remained, then separates "
        "identity preservation from translation glossary enforcement."
    ),
    explicit_reference=True,
    shared_paths=True,
)


def test_llm_provider_uses_injected_transport_and_validates_result():
    captured = {}

    def transport(payload):
        captured.update(payload)
        return {
            "relationship": "refines",
            "evidence": [
                "target states the #6 masking path still left glossary leak-through"
            ],
            "counter_evidence": [],
            "missing_evidence": [],
            "rationale": "The later change narrows and corrects the earlier mechanism.",
        }

    provider = LLMSemanticProvider(transport, model="test-model")
    result = provider.infer(REQUEST)

    assert provider.name == "llm:test-model"
    assert result.relationship is Relationship.REFINES
    assert captured["input"]["signals"]["explicit_reference"] is True
    assert "patentability" in captured["system"]


def test_llm_provider_rejects_confident_edge_without_evidence():
    provider = LLMSemanticProvider(
        lambda payload: {
            "relationship": "refines",
            "evidence": [],
            "counter_evidence": [],
            "missing_evidence": [],
            "rationale": "trust me",
        },
        model="test-model",
    )

    with pytest.raises(ValueError, match="explicit evidence"):
        provider.infer(REQUEST)


def test_llm_provider_accepts_explained_unknown():
    provider = LLMSemanticProvider(
        lambda payload: {
            "relationship": "unknown",
            "evidence": ["the target only references the source"],
            "counter_evidence": [],
            "missing_evidence": ["no causal language establishes a direct relationship"],
            "rationale": "Reference alone is insufficient.",
        },
        model="test-model",
    )

    result = provider.infer(REQUEST)
    assert result.relationship is Relationship.UNKNOWN
