"""Provider-neutral semantic reasoning interface."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .reasoning import ReasoningResult
from .semantic_baseline import infer_from_text


@dataclass(frozen=True)
class SemanticRequest:
    source_id: str
    target_id: str
    target_text: str
    explicit_reference: bool
    shared_paths: bool


class SemanticProvider(Protocol):
    @property
    def name(self) -> str: ...

    def infer(self, request: SemanticRequest) -> ReasoningResult: ...


class RuleSemanticProvider:
    """Auditable baseline exposed through the same contract as future providers."""

    @property
    def name(self) -> str:
        return "rule-baseline"

    def infer(self, request: SemanticRequest) -> ReasoningResult:
        result = infer_from_text(
            source_id=request.source_id,
            target_id=request.target_id,
            target_text=request.target_text,
            explicit_reference=request.explicit_reference,
            shared_paths=request.shared_paths,
        )
        result.validate()
        return result
