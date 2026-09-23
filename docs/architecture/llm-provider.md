# LLM semantic provider

The first LLM provider is intentionally transport-injected.

IP Radar owns:

- the semantic request boundary;
- conservative system instructions;
- the allowed relationship vocabulary;
- response decoding;
- `ReasoningResult` validation.

IP Radar does not yet own:

- a vendor SDK;
- API credentials;
- retries or billing policy;
- arbitrary network access;
- agent actions.

A caller supplies a transport function. This keeps unit tests offline and allows the same semantic contract to be exercised against different providers later.

## Prompt boundary

The provider is explicitly told:

- use only supplied evidence;
- explicit references and shared paths alone are insufficient;
- return `unknown` when a direct relationship is not established;
- do not infer patentability or legal novelty;
- non-`unknown` answers require concrete evidence.

The model output is not trusted merely because it matches the schema. It must also pass the same `ReasoningResult.validate()` contract used by non-LLM providers.

## First live evaluation

The next step is a deliberately small live run against the existing rich, related-only, and sparse cases. Live model output should be recorded as evaluation evidence, not silently converted into product behavior.
