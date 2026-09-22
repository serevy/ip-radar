# Semantic rule baseline

Before connecting an LLM, IP Radar uses a deliberately small rule baseline.

The baseline requires an explicit reference to the earlier artifact and explicit causal language in the later artifact before emitting a semantic relationship. Shared paths never suffice.

This baseline is intentionally limited. A change can both respond to a failure and refine an earlier mechanism, so rule labels are not treated as ground truth. Its job is to provide an auditable lower bound for later provider comparisons and to protect the `unknown` behavior.

A future semantic provider should beat this baseline on relationship-kind accuracy without degrading abstention or evidence traceability.
