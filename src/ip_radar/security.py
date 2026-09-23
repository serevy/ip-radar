"""Security boundary for untrusted development artifacts.

This module is intentionally small: it defines IP Radar's trust contract and
adapter points. Detection engines may be provided by established guardrail
projects rather than reimplemented here.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Protocol


class SecuritySeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKED = "blocked"
    CRITICAL = "critical"


@dataclass(frozen=True)
class SecurityEvent:
    code: str
    severity: SecuritySeverity
    message: str


@dataclass(frozen=True)
class EvidenceEnvelope:
    source_id: str
    target_id: str
    text: str
    explicit_reference: bool
    shared_paths: bool
    untrusted: bool = True


@dataclass(frozen=True)
class GuardResult:
    envelope: EvidenceEnvelope
    events: tuple[SecurityEvent, ...] = ()
    blocked: bool = False


class InputGuard(Protocol):
    def inspect(self, envelope: EvidenceEnvelope) -> GuardResult: ...


class PassThroughGuard:
    """Default local guard for tests; performs no external security claims."""

    def inspect(self, envelope: EvidenceEnvelope) -> GuardResult:
        return GuardResult(envelope=envelope)


def minimize(envelope: EvidenceEnvelope, *, max_chars: int = 12_000) -> GuardResult:
    """Bound disclosure size before any external semantic provider."""
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    if len(envelope.text) <= max_chars:
        return GuardResult(envelope=envelope)

    event = SecurityEvent(
        code="EVIDENCE_TRUNCATED",
        severity=SecuritySeverity.INFO,
        message=f"evidence text truncated to {max_chars} characters before provider disclosure",
    )
    return GuardResult(
        envelope=replace(envelope, text=envelope.text[:max_chars]),
        events=(event,),
    )
