# readme-i18n-kit archaeology fixture

The PR #3–#8 fixture is frozen for the first relationship-reconstruction experiment.

## Evaluation layers

1. **Artifact normalization** — preserve identity, time, title, and source provenance.
2. **Deterministic relationship signals** — explicit references, shared changed paths, and later other inspectable signals.
3. **Candidate-pair evaluation** — measure whether expected related PR pairs are surfaced.
4. **Semantic relationship inference** — future layer; classify relations such as `responds_to` or `refines` only when evidence supports them.
5. **Candidate lineage reconstruction** — future layer.

A deterministic signal is not itself proof of a semantic relationship. In particular, shared file paths are weak evidence and explicit references can mean many things.

The first experiment intentionally separates **pair recall** from **relationship-kind accuracy** so a high recall score cannot be mistaken for successful reasoning.
