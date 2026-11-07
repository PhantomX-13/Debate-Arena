# Model and provider setup

Debate Arena's role prompts, handoff flow, and rubrics are separate from the model. Switch is the agent runner and Discord is the shared room. This repository contains two deployment templates: the live-verified Codex setup and an alternate OpenCode setup for choosing from OpenCode's provider catalog, local model servers, and compatible custom endpoints.

## Templates

- `switch/templates/debate-arena.template.yaml` uses `provider: codex` and matches the live team deployment.
- `switch/templates/debate-arena-opencode.template.yaml` uses `provider: opencode` for all seven roles. Install OpenCode and its Switch connector, then import this template. Configure the default model in OpenCode; this template leaves model selection to the operator's OpenCode configuration.

OpenCode documents built-in integrations for many hosted providers and local Ollama, LM Studio, and vLLM models. It also supports adding a custom provider when an endpoint uses a supported protocol. Availability, model IDs, credentials, API limits, and tool support depend on the installed OpenCode version and chosen provider. See [OpenCode provider setup](https://opencode.ai/docs/providers/) and [Switch's supported agent-provider model](https://www.switchagents.ai/blog-posts/switch-getting-started).

To switch the model, configure or authenticate it in OpenCode (for example with `/connect` and `/models`), then run a small Switch handoff and a complete case. All seven Debate Arena roles use the selected OpenCode runtime and its configured default model unless you specifically configure OpenCode agents differently. The checked live workflow still uses Codex; the alternate OpenCode template has not yet been tested in the team's Discord room.

## Local models and costs

There is no Debate Arena API subscription. With a local model server such as Ollama, a user can avoid per-request model API charges, but must install the server, download a model, and have sufficient hardware. Hosted free tiers or trials are controlled by each provider and may change; this project does not promise free hosted inference. Model licenses and acceptable-use terms still apply.

## Custom endpoints and native providers

OpenCode can configure custom endpoints, including OpenAI-compatible APIs. This provides a practical route for many services (for example OpenRouter, Ollama-compatible servers, and self-hosted vLLM/LM Studio endpoints) when the selected model supports the needed tools. OpenCode also has native provider integrations. Do not assume all services share the same API key format, endpoint path, tool-calling behavior, context length, or browsing support.

For a no-model-API-key local setup, install Ollama and OpenCode, pull a model that supports tool use (for example `ollama pull qwen3:4b`), and configure the model in OpenCode. Model capabilities vary: `gemma3:4b` generated text in our local check but OpenCode reported that it does not support tools. Before importing the full OpenCode Debate Arena template, import `switch/templates/opencode-ollama-smoke.template.yaml`, attach its single agent to the existing Discord room, and check that a direct `DA-OPENCODE-SMOKE` request produces a visible reply. Then test a named handoff before running a full case. OpenCode documents Ollama discovery and custom endpoint configuration in its [provider guide](https://opencode.ai/docs/providers/). These checks are not yet verified in the team's live Switch room.

This route supports broad provider choice through OpenCode; Debate Arena does not maintain and test a separate native API adapter for every named vendor. The OpenAI-compatible standalone client in `tools/model_provider.py` is only a text-completion smoke check; it does not run roles or integrate with Switch.

Browser Transformers.js/ONNX inference is not directly wired into the Discord/Switch execution path. To use such a model with these agents, it would need to run behind a compatible local inference server or be integrated as a separate Switch agent runtime.

## Run the standalone endpoint smoke check

This optional check is independent of Switch. It sends one text prompt and reads the common chat-completions schema. A local server usually needs no API key; hosted endpoints often do.

```sh
export DEBATE_ARENA_BASE_URL="http://localhost:11434/v1"
export DEBATE_ARENA_MODEL="your-installed-model-id"
# For a remote endpoint only:
export DEBATE_ARENA_API_KEY="your-key"
python3 tools/model_provider.py "Reply with one sentence."
```

The client reads credentials from environment variables, does not print them, and uses only Python's standard library. Use HTTPS for remote endpoints that require credentials. Never commit API keys or personal tokens.

## Provider verification checklist

For every selected OpenCode/provider/model combination:

1. Confirm Switch Console detects and starts OpenCode.
2. Confirm OpenCode can authenticate or reach the configured local endpoint.
3. Run `DA-GATE` and confirm a named Scout → Checker handoff reaches Discord.
4. Run one complete case and check the actual model's research/tool use, handoffs, ballot, and report writing.
5. Record model name, provider, runtime version, failures, and any fallback in `docs/RESULTS.md`.

Never describe an untested provider as verified. For security, do not broaden the Moderator's Discord access rule on a public channel.
