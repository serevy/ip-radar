# Security model

IP Radar processes development history as **untrusted input**. A repository, pull request, issue, document, or future AI-session record may contain malicious instructions, secrets, sensitive information, or misleading evidence.

Security is therefore a layered boundary, not a prompt convention.

## Principles

1. **Prevent / sanitize** — inspect untrusted artifacts before model disclosure.
2. **Deny capabilities** — semantic providers are read-only and tool-less.
3. **Minimize disclosure** — send only bounded evidence required for the comparison.
4. **Protect secrets** — credentials belong to the transport/secret store, never the prompt.
5. **Control egress** — live transports must restrict destinations, verify TLS, and avoid arbitrary redirects.
6. **Validate output** — schema-valid model output is still untrusted.
7. **Ground evidence** — semantic claims must refer to evidence actually supplied.
8. **Detect and audit** — security signals are recorded separately from technical candidate evidence.
9. **Notify appropriately** — informational redaction/minimization, warnings, blocked results, and critical boundary violations should remain distinguishable.

## Boundary

```text
Untrusted artifacts
  -> minimization / redaction / injection inspection
  -> evidence envelope
  -> semantic provider (no tools, no arbitrary network, no repo write)
  -> schema + reasoning validation
  -> evidence grounding
  -> semantic result

Security events -> separate audit/notification stream
```

Security events must not become candidate-lineage evidence merely because they occurred.

## Guardrail integrations

IP Radar should prefer established guardrail/governance components over implementing a standalone security product.

Planned adapter targets:

- NVIDIA NeMo Guardrails (Apache-2.0) for input/output/retrieval guardrails where appropriate;
- Microsoft Agent Governance Toolkit (MIT) when IP Radar crosses the future Governance Gate and gains action-capable agents.

Neither dependency is required by the current Core. Integrations should remain optional and replaceable.

## Transport requirements for a live external provider

A live transport is not approved merely because it implements the Python callable interface. Before use with private or sensitive evidence it must define and test:

- HTTPS/TLS certificate verification;
- endpoint allowlisting;
- redirect policy;
- timeout and response-size limits;
- secret isolation;
- logging/redaction policy;
- data-retention/provider policy appropriate to the deployment.

The current PoC does not claim these properties for an arbitrary injected transport.

## Prompt injection

Repository text is data, never authority. Prompt-based instructions are defense in depth only. The primary control is capability denial: the semantic provider receives prepared evidence and cannot execute shell commands, read arbitrary files, call tools, mutate repositories, or follow model-requested URLs.

## Supply chain

Dependencies and GitHub Actions should be pinned and monitored. Untrusted repository or generated code must not be executed as part of semantic reasoning. Introducing such execution crosses the separate Sandbox Gate and requires a new security decision.

## Performance boundary

Security controls must protect the trust boundary without turning the normal path into a high-latency pipeline.

**Spend latency on reasoning, not guarding.**

The intended architecture is:

- fast path: cached verdicts, deterministic secret/type/size/endpoint checks, and lightweight local inspection;
- suspicious path: deeper guardrail inspection only when signals justify it;
- incremental rescanning: unchanged artifact content should reuse a verdict keyed by content/config version where safe;
- parallel work: independent security checks and evidence preparation should run concurrently where possible;
- final gate: no semantic result is released until required output validation and grounding complete.

Initial PoC performance hypothesis: normal-path security overhead should target p95 below 100 ms on representative local fixtures, excluding semantic model latency. This is an evaluation target, not a current performance claim.

Security evaluation should report three separate dimensions: protection effectiveness, information retention, and added latency. A slower guard is not automatically safer, and a faster guard is not acceptable if it weakens the boundary.
