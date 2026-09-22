---
id: PDDR-0001
title: Focus IP Radar on provenance reconstruction rather than patent automation
decision_date: 2026-09-22
recorded_date: 2026-09-22
decision_status: accepted
delivery_status: implemented
scope:
  - project
  - product
  - process
owners:
  - serevy
evidence:
  - docs/research/phase-0.md
related: []
supersedes: []
superseded_by: null
---

# PDDR-0001: Focus IP Radar on provenance reconstruction rather than patent automation

## Summary

Build the first IP Radar PoC around retroactive temporal provenance and candidate-lineage reconstruction. Do not build a new end-to-end patent automation platform.

## Context and observations

Phase 0 found strong existing capabilities for invention discovery, prior-art workflows, candidate tracking, disclosure generation, explicit decision DAGs, and publication awareness.

Retrospective review still suggested a narrower unresolved question: ordinary development artifacts can contain fragments of a technical idea's history even when nobody recorded that history for IP purposes.

## Options considered

### End-to-end patent AI
- Benefits: broad product surface.
- Costs: duplicates substantial existing work before the core hypothesis is validated.
- Status: rejected.

### Another invention detector
- Benefits: simple story.
- Costs: strong existing implementations already cover this area.
- Status: rejected.

### Require PDDR
- Benefits: dense structured evidence.
- Costs: excludes ordinary repositories and confuses enrichment with the core.
- Status: rejected.

### Provenance-reconstruction PoC with optional enrichment
- Benefits: directly tests the surviving hypothesis and can integrate with existing IP tools later.
- Costs: value remains uncertain until evaluated.
- Status: accepted.

## Decision

Focus the first PoC on temporal evidence graphs, candidate-family/lineage reconstruction, explicit uncertainty and abstention, and human-readable evidence reports. The core must not depend on one language, jurisdiction, tracker, AI provider, or PDDR.

## Delivery and validation

The bootstrap documents the scope and creates an evaluation skeleton. The archaeology hypothesis is not yet validated; repository setup only implements the decision.

## Consequences

Existing invention-detection, prior-art, disclosure, and publication-awareness tools are potential integrations rather than features to rebuild by default. AI development sessions remain out of scope pending a separate privacy/security decision. Candidate count is not a success metric.

## Revisit when

Revisit if evaluation shows no meaningful information gain over existing artifact mining, or an existing tool provides equivalent reconstruction with acceptable integration and licensing.

## Evidence

- [Phase 0 research summary](../research/phase-0.md)

## Related records

None.
