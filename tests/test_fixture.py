import json
from pathlib import Path


def test_readme_i18n_fixture_is_frozen_and_abstains_on_patentability():
    fixture = json.loads(
        Path("evals/readme-i18n-kit/pr-3-8.json").read_text(encoding="utf-8")
    )

    assert fixture["freeze"]["future_artifacts_allowed"] is False
    assert fixture["freeze"]["first_pr"] == 3
    assert fixture["freeze"]["last_pr"] == 8
    assert len(fixture["artifacts"]) == 6
    assert fixture["abstention"]["patentability"] == "unknown"
