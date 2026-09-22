from ip_radar.github import pull_request_artifact


def test_pull_request_normalization_keeps_provenance():
    artifact = pull_request_artifact(
        {
            "number": 8,
            "title": "fix: identity glossary",
            "created_at": "2026-09-21T19:10:00Z",
            "html_url": "https://github.com/example/repo/pull/8",
        }
    )

    assert artifact.id == "pr-8"
    assert artifact.kind == "pull_request"
    assert artifact.source_url.endswith("/pull/8")
    assert artifact.occurred_at.isoformat() == "2026-09-21T19:10:00+00:00"
