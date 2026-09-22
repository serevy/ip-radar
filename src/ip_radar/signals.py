"""Deterministic relationship signals.

Signals are evidence for later reasoning, not relationship conclusions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RelationshipSignal:
    source: str
    target: str
    signal: str
    evidence: str


PR_REF = re.compile(r"(?<![\w/])#(?P<number>\d+)\b")
URL_REF = re.compile(r"github\.com/[^/]+/[^/]+/pull/(?P<number>\d+)\b")


def explicit_pr_references(source_id: str, text: str) -> tuple[RelationshipSignal, ...]:
    """Extract explicit PR references without assigning semantic edge kinds."""
    numbers = {match.group("number") for match in PR_REF.finditer(text)}
    numbers.update(match.group("number") for match in URL_REF.finditer(text))

    signals = [
        RelationshipSignal(
            source=f"pr-{number}",
            target=source_id,
            signal="explicit_reference",
            evidence=f"{source_id} explicitly references PR #{number}",
        )
        for number in sorted(numbers, key=int)
        if f"pr-{number}" != source_id
    ]
    return tuple(signals)


def shared_paths(
    source_id: str,
    source_paths: set[str],
    target_id: str,
    target_paths: set[str],
) -> RelationshipSignal | None:
    """Record overlapping changed paths as a weak, non-semantic signal."""
    overlap = sorted(source_paths & target_paths)
    if not overlap:
        return None
    return RelationshipSignal(
        source=source_id,
        target=target_id,
        signal="shared_paths",
        evidence=", ".join(overlap),
    )
