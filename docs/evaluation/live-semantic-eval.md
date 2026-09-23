# Live semantic evaluation

Live semantic evaluation is manual and isolated from normal pull-request/push CI.

## GitHub setup

Create a GitHub Environment named `live-evaluation` and add the repository/environment secret:

- `OPENAI_API_KEY`

Prefer an environment-scoped secret over a repository-wide secret. Environment protection rules may be added if desired.

The workflow is `workflow_dispatch` only, so normal pushes and pull requests do not spend API budget or disclose fixture text to an external provider.

## Transport controls

The current OpenAI evaluation transport:

- only permits `https://api.openai.com/v1/responses`;
- uses the platform TLS certificate validation;
- rejects redirects;
- has a 30 second timeout;
- caps response bodies at 256 KB;
- keeps the API key in the Authorization header and out of prompts/artifacts;
- requests `store: false`;
- enables no model tools.

The transport is intentionally specific to this evaluation and is not a general-purpose HTTP client.

## Model

The workflow defaults to `gpt-5.6-luna` for a low-cost first evaluation. The model ID is a manual workflow input so later comparisons can use the same harness.

## Result

The workflow uploads `live-semantic-eval.json` for 14 days. The report contains semantic results and latency, never the API key.

A live run is evaluation evidence only. It does not automatically change product policy or mark PDDR-0002 as validated.
