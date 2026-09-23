# Repository guidance

- Prefer evidence-backed statements over inferred intent.
- Treat insufficient evidence as a valid outcome.
- Do not claim patentability, legal status, or novelty without explicitly scoped external analysis.
- Keep technical confidence, evidence maturity, prior-art uncertainty, and disclosure risk separate.
- Do not require PDDR for core functionality.
- Do not ingest AI development sessions without a separately reviewed privacy/security design.
- Preserve the narrow PoC: GitHub history → temporal evidence graph → candidate lineage → report.
- Durable Project / Product / Process decisions may warrant a PDDR; routine work does not.

## PDDR checkpoints

At these milestones, revisit a bounded set of recent Issues and pull requests against the normal PDDR threshold:

- after a major research or PoC phase boundary;
- during an Issue or roadmap audit;
- when multiple Evidence-bearing Issues or pull requests are being closed or consolidated.

### Pending checkpoint marker

PR本文に `## PDDR checkpoint` と `Review: pending` がある場合は、signalに関係するrecent Issues / PRs / Evidenceだけを対象にbounded auditします。

- SignalはPDDR作成義務ではありません。
- routine implementation、candidate signal、raw observation、experiment completionだけではPDDRへ昇格させません。
- durableなProject / Product / Process判断がなければno-opを正常結果とします。
- review後はPR本文のcurrent stateを `Review: completed` へ更新します。
- 過去のCheck / Job Summaryはsignal発生時点の履歴として扱い、同期更新しません。
- checkpoint CI自体をexternal semantic reasoningやpatentability判定として扱いません。

At a checkpoint:

- Review only the recent work and existing PDDRs relevant to the milestone.
- Create or update a PDDR only when the evidence produced a durable Project, Product, or Process decision.
- Prefer updating an existing PDDR when it already represents the same decision.
- Do not promote routine implementation, candidate signals, raw observations, or experiment completion itself into a PDDR.
- If no durable decision is found, create nothing; the checkpoint is an audit, not a record quota.

