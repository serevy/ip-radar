---
id: PDDR-0002
title: Put untrusted semantic reasoning behind a layered security boundary
decision_date: 2026-09-23
recorded_date: 2026-09-23
decision_status: accepted
delivery_status: in-progress
scope:
  - product
  - process
owners:
  - serevy
evidence:
  - docs/security.md
  - docs/architecture/llm-provider.md
related:
  - PDDR-0001
supersedes: []
superseded_by: null
---

# PDDR-0002: Put untrusted semantic reasoning behind a layered security boundary

## Summary

Treat development artifacts and model outputs as untrusted. External semantic reasoning must cross an explicit, layered security boundary that minimizes disclosure, denies unnecessary capabilities, validates and grounds outputs, separates security events from candidate evidence, and preserves a low-latency normal path.

## Context and observations

IP Radar is intended to inspect development history that may contain unpublished technical information, secrets, sensitive data, or malicious instructions. Introducing an external semantic model creates a new trust boundary.

Prompt instructions alone are not an adequate security control. At the same time, aggressive blocking or redaction can remove the very technical evidence IP Radar needs to evaluate, and heavy guardrails can make normal development workflows unacceptably slow.

Existing open-source guardrail/governance projects cover substantial parts of this problem, so IP Radar should not create a standalone security framework without evidence that a missing reusable layer exists.

## Options considered

### Rely on prompt instructions only

- Benefits: minimal implementation cost and latency.
- Costs / constraints: does not provide a meaningful capability, disclosure, transport, or output-trust boundary.
- Status: rejected.

### Block or heavily redact all sensitive-looking content

- Benefits: conservative external disclosure.
- Costs / constraints: can destroy high-value unpublished technical evidence and reduce archaeology quality.
- Status: rejected as a universal policy.

### Build a complete security framework inside IP Radar

- Benefits: full local control.
- Costs / constraints: duplicates mature security/guardrail work and expands scope before requirements are validated.
- Status: rejected for the current PoC.

### Layer a thin IP Radar security boundary around replaceable guardrail components

- Benefits: keeps IP-specific minimization, grounding, audit separation, and disclosure policy local while reusing established detection/governance components.
- Costs / constraints: adapter design and integration testing are required; external guardrails still need independent evaluation.
- Status: accepted.

## Decision

IP Radar semantic reasoning will use a layered trust boundary:

1. classify development artifacts as untrusted;
2. minimize evidence before external disclosure;
3. keep semantic providers read-only and tool-less;
4. isolate credentials and restrict live transport destinations;
5. validate structured model output;
6. ground semantic evidence against the evidence actually supplied;
7. keep security events separate from candidate-lineage evidence;
8. notify users according to severity;
9. prefer established optional guardrail/governance components over rebuilding them.

The normal security path must remain lightweight. Deeper inspection is reserved for suspicious inputs. Security evaluation will consider protection effectiveness, information retention, and added latency separately.

The initial performance hypothesis is a p95 normal-path security overhead below 100 ms on representative local fixtures, excluding semantic model latency. This is a target to validate, not a current performance claim.

## Delivery and validation

The LLM-provider branch introduces the initial EvidenceEnvelope, minimization, SecurityEvent, grounding validator, transport requirements, and documentation. The decision remains in-progress until a live transport and representative security fixtures validate the boundary.

Optional NeMo Guardrails and future Agent Governance Toolkit integrations remain adapter candidates rather than mandatory Core dependencies.

## Consequences

- Live external providers cannot be enabled safely by merely supplying an API key.
- Private/sensitive evidence may require local-only or explicit-consent disclosure policies in future work.
- Prompt-injection signals do not automatically prove an attack.
- Security events do not become technical candidate evidence.
- Introducing action-capable agents crosses a separate Governance Gate.
- Executing untrusted repository or generated code crosses a separate Sandbox Gate.
- Semantic Decision Lab can evaluate the tradeoff between security protection, information retention, and latency before policies are relaxed.

## Revisit when

Revisit after live security evaluation, when a local-only/consent disclosure mode is introduced, when an action-capable agent is added, when untrusted code execution is proposed, or when evidence shows the thin orchestration layer should become a reusable project.

## Evidence

- [Security model](../security.md)
- [LLM provider architecture](../architecture/llm-provider.md)

## Related records

- PDDR-0001
