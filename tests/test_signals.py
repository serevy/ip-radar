from ip_radar.evaluation import evaluate_candidate_pairs
from ip_radar.signals import explicit_pr_references, shared_paths


def test_explicit_reference_is_evidence_not_semantic_edge():
    signals = explicit_pr_references(
        "pr-8",
        "Related: #6 and https://github.com/example/repo/pull/7",
    )

    assert [(item.source, item.target, item.signal) for item in signals] == [
        ("pr-6", "pr-8", "explicit_reference"),
        ("pr-7", "pr-8", "explicit_reference"),
    ]


def test_shared_paths_is_weak_signal():
    signal = shared_paths(
        "pr-3",
        {"README.md", "scripts/verify.py"},
        "pr-4",
        {"scripts/verify.py", "workflow.yml"},
    )

    assert signal is not None
    assert signal.signal == "shared_paths"
    assert signal.evidence == "scripts/verify.py"


def test_pair_evaluation_does_not_pretend_to_predict_semantics():
    signals = explicit_pr_references("pr-8", "Related: #6")
    expected = [
        {"source": "pr-6", "target": "pr-8", "kind": "refines"},
        {"source": "pr-5", "target": "pr-6", "kind": "refines"},
    ]

    metrics = evaluate_candidate_pairs(signals, expected)

    assert metrics.expected_pairs == 2
    assert metrics.recovered_pairs == 1
    assert metrics.false_pairs == 0
    assert metrics.pair_recall == 0.5
