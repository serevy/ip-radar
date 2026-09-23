from ip_radar.provider_eval import SemanticCase, evaluate_provider
from ip_radar.providers import RuleSemanticProvider, SemanticRequest
from ip_radar.reasoning import Relationship


def cases():
    return (
        SemanticCase(
            SemanticRequest(
                source_id="pr-4",
                target_id="pr-5",
                target_text=(
                    "Related: #4. The previous repair failed because it repeated "
                    "the same prompt. This change fixes the failure with a dedicated prompt."
                ),
                explicit_reference=True,
                shared_paths=True,
            ),
            frozenset({Relationship.RESPONDS_TO, Relationship.REFINES}),
        ),
        SemanticCase(
            SemanticRequest(
                source_id="pr-7",
                target_id="pr-8",
                target_text="Related: #7",
                explicit_reference=True,
                shared_paths=False,
            ),
            frozenset({Relationship.UNKNOWN}),
        ),
        SemanticCase(
            SemanticRequest(
                source_id="change-a",
                target_id="change-b",
                target_text="Namespace cleanup",
                explicit_reference=False,
                shared_paths=True,
            ),
            frozenset({Relationship.UNKNOWN}),
        ),
    )


def test_rule_provider_uses_same_contract_as_future_providers():
    provider = RuleSemanticProvider()
    metrics = evaluate_provider(provider, cases())

    assert provider.name == "rule-baseline"
    assert metrics.cases == 3
    assert metrics.accepted == 3
    assert metrics.false_positive_edges == 0
    assert metrics.abstentions == 2
    assert metrics.accepted_rate == 1.0
