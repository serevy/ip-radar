"""Normalization helpers for GitHub artifacts.

Network access is intentionally outside this module. The adapter consumes
already-fetched GitHub payloads so the archaeology core stays testable and
provider-neutral.
"""

from __future__ import annotations

from datetime import datetime

from .graph import Artifact


def _timestamp(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("GitHub timestamps must include a timezone")
    return parsed


def pull_request_artifact(payload: dict) -> Artifact:
    """Normalize the stable subset of a GitHub pull-request payload we need."""
    number = payload.get("number")
    title = payload.get("title")
    created_at = payload.get("created_at")
    url = payload.get("html_url") or payload.get("url")

    if not isinstance(number, int):
        raise ValueError("pull request number must be an integer")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("pull request title must be non-empty")
    if not isinstance(created_at, str):
        raise ValueError("pull request created_at must be an ISO timestamp")

    return Artifact(
        id=f"pr-{number}",
        kind="pull_request",
        occurred_at=_timestamp(created_at),
        title=title.strip(),
        source_url=url if isinstance(url, str) else None,
    )
