# Phase 0 research summary

Before creating this repository, the hypothesis was challenged through competitor review and retrospective analysis to avoid building another patent AI.

## Weakened or rejected as differentiators

- invention discovery from source code or engineering artifacts by itself
- reading issues/project context in addition to code
- candidate tracking and retirement by themselves
- publication-awareness by itself
- explicit decision DAGs created for patent work
- a single opaque IP score
- requiring PDDR

## Surviving hypothesis

> Can technical decision provenance and candidate lineages be reconstructed retrospectively from ordinary development artifacts that were never created for IP analysis?

Target trajectory:

```text
observation → problem → alternatives → rejected/deferred paths
            → decision → implementation → validation → feedback → revision
```

Candidate relationships may include same idea, refinement, split, merge, weakening, absorption, supersession, dormancy, and retirement.

## Retrospective observations

Internal review covered PDDR Kit, Semantic Decision Lab, OBS Audio Guardian, and readme-i18n-kit. External blind checks covered BuilderIO/agent-native, annulusgames/Alchemy, and cloudflare/quiche.

The combined observations suggest:

- important design intent can span multiple PRs;
- rejected/deferred alternatives and failures can be useful evidence;
- sparse histories should produce `insufficient evidence`, not invented rationale;
- mature repositories require noise classification before candidate extraction;
- technical confidence, evidence maturity, prior-art uncertainty, and disclosure risk should remain separate;
- early candidates may weaken, be absorbed, or become irrelevant;
- ADR/PDDR can enrich reconstruction without being mandatory;
- AI-agent attribution may be visible while the underlying reasoning session remains a missing edge.

## Evaluation direction

Evaluate reconstruction quality, not candidate count. Candidate metrics include evidence traceability, lineage precision, recovery of rejected/deferred alternatives, false-positive control, abstention quality, recognition of weakening/absorption/retirement, and human clarification required.

Future ADR/PDDR and local AI-session inputs should be evaluated by incremental information value. AI-session ingestion requires a separate privacy/security design and must be opt-in.
