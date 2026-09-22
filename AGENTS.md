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

At a checkpoint:

- Review only the recent work and existing PDDRs relevant to the milestone.
- Create or update a PDDR only when the evidence produced a durable Project, Product, or Process decision.
- Prefer updating an existing PDDR when it already represents the same decision.
- Do not promote routine implementation, candidate signals, raw observations, or experiment completion itself into a PDDR.
- If no durable decision is found, create nothing; the checkpoint is an audit, not a record quota.

