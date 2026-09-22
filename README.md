# IP Radar

> Local-first. Evidence-first. Global-ready.

IP Radar is an experimental archaeology engine for reconstructing technical decision provenance and candidate lineages from ordinary development history.

```text
GitHub history → Temporal Evidence Graph → Candidate lineages
               → Evidence / counter-evidence / uncertainty → Human report
```

IP Radar does **not** decide patentability, provide legal advice, draft or file patents, or replace professional review. It should prefer traceable evidence and abstention over confident guesses.

## 🎋 Like bamboo

Good projects should be allowed to grow without unnecessary interruption.

IP Radar observes development quietly, marks evidence when it may matter, and stays out of the way when it does not. Like a *tanzaku* tied gently to bamboo, a candidate marker says only: **this may be worth remembering**. It does not decide what the idea must become.

**Observe quietly. Mark gently. Interrupt only when necessary. Let projects grow.**

## Design principles

- **Local-first** — keep repository and future session data local by default.
- **Evidence-first** — every candidate points back to inspectable evidence.
- **Abstention-first** — insufficient evidence is a valid result.
- **Tool-neutral** — integrate with existing IP/prior-art tools instead of rebuilding them without cause.
- **Global-ready** — language and jurisdiction concerns stay outside the core provenance model.
- **Non-disruptive** — discovery should not turn normal development into an approval queue.

## PoC scope

1. Order ordinary development artifacts into a temporal evidence graph.
2. Reconstruct related observations as lineages instead of duplicated "inventions".
3. Keep evidence, counter-evidence, missing evidence, and uncertainty explicit.
4. Avoid escalating routine fixes and conventional engineering work.

Initial inputs are GitHub commits, issues, pull requests, tests, experiments, and documentation. ADR/PDDR is optional enrichment, not a requirement.

## Out of scope for the first PoC

Patentability/legal conclusions, patent drafting/filing, a proprietary prior-art engine, publication blocking, AI-session ingestion, jurisdiction-specific legal rules, and SaaS/team features.

## Research

The original "AI invention discovery" idea was deliberately challenged before this repository was created. The surviving hypothesis is narrower: **retroactive temporal provenance and candidate-lineage reconstruction from development artifacts that were not originally recorded for IP purposes**.

See [Phase 0 research](docs/research/phase-0.md).

## Decisions

Durable decisions live under [docs/records/](docs/records/). PDDR is evidence-backed decision context, not unconditional policy.

## Status

**Experimental / PoC.** This repository exists to test the hypothesis, not to claim it has already been proven.
