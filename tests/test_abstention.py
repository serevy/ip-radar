import json
from pathlib import Path

from ip_radar.signals import shared_paths


def test_sparse_history_does_not_promote_shared_path_to_semantic_lineage():
    fixture = json.loads(
        Path("evals/sparse-history/abstention.json").read_text(encoding="utf-8")
    )

    first, second = fixture["artifacts"][:2]
    signal = shared_paths(
        first["id"],
        set(first["changed_paths"]),
        second["id"],
        set(second["changed_paths"]),
    )

    assert signal is not None
    assert signal.signal == "shared_paths"
    assert fixture["expected"]["direct_semantic_edges"] == []
    assert fixture["expected"]["candidate_lineage"] == "insufficient_evidence"
