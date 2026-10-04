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


## PDDR CI authoring defaults

Apply these defaults when adding or changing PDDR CI; see the [PDDR Kit adoption guide](https://github.com/serevy/pddr-kit/blob/main/docs/adoption.md) and [Kit issue #47](https://github.com/serevy/pddr-kit/issues/47).

- Set an explicit job timeout. Lightweight PDDR validation, checkpoint, and marker jobs use `timeout-minutes: 5`; justify a different budget from the actual work.
- Cancel superseded validator runs only within the same workflow and pull request. Include the ref and run ID in non-PR groups so separate main or manual runs remain independent.
- Keep checkpoint detection read-only, including PR body and label events and complete base/head comparison. Marker writes use trusted default-branch code in the separate `workflow_run` job, without PR code or artifacts and without cancellation.
- Preserve required-check identities, trigger/path coverage, validation flags, runtime versions, action pins, and permissions. Review those contracts before combining or splitting jobs.
- Add caching, matrices, parallel jobs, or artifacts only when their benefit justifies the extra work. A lightweight validator may share an existing read-only job only after preserving coverage, failure behavior, and check requirements.
- Record job counts and native execution time from normal CI in the PR; separate expected savings from measured results. These defaults retain existing project, review, and publication authority.
