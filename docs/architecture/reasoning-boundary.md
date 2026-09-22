# Semantic reasoning boundary

The first reasoning layer is deliberately a contract, not an agent.

## Inputs

A reasoner may receive normalized artifacts, deterministic relationship signals, and inspectable evidence extracted from available development history.

## Outputs

Every result must return:

- a relationship: `refines`, `responds_to`, `contradicts`, `validates`, or `unknown`;
- supporting evidence;
- counter-evidence when present;
- missing evidence when the conclusion is uncertain;
- a human-readable rationale.

A non-`unknown` semantic relationship without explicit evidence is invalid. `unknown` is a first-class successful result when the available history does not support a stronger conclusion.

## Authority boundary

Reasoning is read-only. A reasoner does not:

- mutate repositories;
- create or merge pull requests;
- change visibility or publication state;
- file or draft legal submissions;
- execute untrusted repository code;
- convert a relationship inference into a legal or patentability conclusion.

This boundary is intentional preparation for future governance integration. If IP Radar later gains an action-capable agent, that transition requires a separate governance decision and policy-enforcement layer. If it later executes untrusted project or generated code, that requires a separate execution-sandbox decision.

## Why not add an agent-governance framework now?

There is no action-capable agent in the current PoC. Adding a full governance runtime now would increase complexity without protecting an existing authority boundary. The contract keeps the insertion point explicit without pretending the current read-only reasoner needs agent infrastructure.
