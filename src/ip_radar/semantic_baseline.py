"""Auditable semantic baseline before introducing an LLM provider.

Rules only act on explicit causal language. Structural signals remain context.
"""

from __future__ import annotations

import re

from .reasoning import Relationship, ReasoningResult


REFINEMENT_PATTERNS = (
    re.compile(r"\b(?:refine|refines|refined|improve|improves|improved)\b", re.I),
    re.compile(r"(?:さらに|その上で|従来|これまで).*(?:修正|改善|分離|変更)"),
)
RESPONSE_PATTERNS = (
    re.compile(r"\b(?:caused by|because|failure|failed|regression)\b", re.I),
    re.compile(r"(?:問題|失敗|原因|残留|壊れ|誤置換).*(?:修正|対応|解消|防止)"),
)
VALIDATION_PATTERNS = (
    re.compile(r"\b(?:validated|confirmed|verified|tests? pass)\b", re.I),
    re.compile(r"(?:確認|検証).*(?:成功|解消|動作|通過)"),
)


def infer_from_text(
    *,
    source_id: str,
    target_id: str,
    target_text: str,
    explicit_reference: bool,
    shared_paths: bool,
) -> ReasoningResult:
    """Infer only when the target explicitly references the source and states causality."""
    structural: list[str] = []
    if explicit_reference:
        structural.append(f"{target_id} explicitly references {source_id}")
    if shared_paths:
        structural.append("changed paths overlap")

    if not explicit_reference:
        return ReasoningResult(
            relationship=Relationship.UNKNOWN,
            evidence=tuple(structural),
            missing_evidence=("no explicit source reference",),
            rationale="baseline refuses semantic inference from path overlap alone",
        )

    if any(pattern.search(target_text) for pattern in VALIDATION_PATTERNS):
        return ReasoningResult(
            relationship=Relationship.VALIDATES,
            evidence=tuple(structural + ["target text contains explicit validation language"]),
            rationale="explicit reference plus validation language",
        )

    if any(pattern.search(target_text) for pattern in RESPONSE_PATTERNS):
        return ReasoningResult(
            relationship=Relationship.RESPONDS_TO,
            evidence=tuple(structural + ["target text states a problem/failure response"]),
            rationale="explicit reference plus causal failure/response language",
        )

    if any(pattern.search(target_text) for pattern in REFINEMENT_PATTERNS):
        return ReasoningResult(
            relationship=Relationship.REFINES,
            evidence=tuple(structural + ["target text states an incremental refinement"]),
            rationale="explicit reference plus refinement language",
        )

    return ReasoningResult(
        relationship=Relationship.UNKNOWN,
        evidence=tuple(structural),
        missing_evidence=("reference exists but semantic causal language is insufficient",),
        rationale="explicit reference alone is not a semantic edge",
    )
