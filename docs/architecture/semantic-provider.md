# Semantic provider interface

Semantic providers are interchangeable implementations behind one read-only contract.

A provider receives a `SemanticRequest` containing the artifact pair, available target text, and deterministic relationship signals. It returns a validated `ReasoningResult`.

The rule baseline is the first provider. A future LLM implementation must use the same request/result boundary so it can be compared rather than silently replacing the baseline.

## Evaluation dimensions

Provider comparison must keep at least these concerns separate:

- accepted relationship-kind rate;
- false-positive semantic edges on abstention cases;
- abstention count/rate;
- evidence traceability enforced by `ReasoningResult.validate()`.

A provider is not better merely because it emits fewer `unknown` results.

## Provider boundary

Providers are read-only semantic classifiers. They receive prepared evidence and return reasoning results. They do not fetch arbitrary URLs, mutate repositories, execute project code, or take publication/legal actions.

This keeps the current PoC below the future Governance Gate.
