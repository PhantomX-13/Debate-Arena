#!/usr/bin/env python3
"""Small provider-neutral client for OpenAI-compatible chat-completions endpoints.

This utility is a connection layer, not the Debate Arena/Switch orchestrator.
Configure DEBATE_ARENA_BASE_URL, DEBATE_ARENA_MODEL, and optionally
DEBATE_ARENA_API_KEY, then run: python3 tools/model_provider.py "Hello".
"""
from dataclasses import dataclass
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Protocol


class ProviderError(RuntimeError):
    """A sanitized endpoint, transport, or response error."""


class ChatProvider(Protocol):
    def chat(self, messages, *, temperature=None):
        """Return the assistant's text for a chat message list."""


@dataclass(frozen=True)
class ProviderConfig:
    base_url: str
    model: str
    api_key: str = ""
    timeout: int = 60

    @classmethod
    def from_env(cls, prefix="DEBATE_ARENA"):
        base_url = os.getenv(f"{prefix}_BASE_URL", "").strip()
        model = os.getenv(f"{prefix}_MODEL", "").strip()
        if not base_url or not model:
            raise ValueError(
                f"Set {prefix}_BASE_URL and {prefix}_MODEL; API keys are optional for local servers."
            )
        try:
            timeout = int(os.getenv(f"{prefix}_TIMEOUT", "60"))
        except ValueError as exc:
            raise ValueError(f"{prefix}_TIMEOUT must be an integer number of seconds.") from exc
        if timeout <= 0:
            raise ValueError(f"{prefix}_TIMEOUT must be greater than zero.")
        return cls(base_url, model, os.getenv(f"{prefix}_API_KEY", ""), timeout)


class OpenAICompatibleProvider:
    """Use the common POST /chat/completions JSON request/response shape."""

    def __init__(self, config: ProviderConfig):
        self.config = config

    @property
    def endpoint(self):
        base = self.config.base_url.rstrip("/")
        if base.endswith("/chat/completions"):
            return base
        return f"{base}/chat/completions"

    def chat(self, messages, *, temperature=None):
        if not isinstance(messages, list) or not messages:
            raise ValueError("messages must be a non-empty list of chat messages.")
        payload = {"model": self.config.model, "messages": messages}
        if temperature is not None:
            payload["temperature"] = temperature
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            # Do not echo the response body: some gateways include request metadata.
            raise ProviderError(f"Provider returned HTTP {exc.code}.") from None
        except (urllib.error.URLError, TimeoutError) as exc:
            reason = getattr(exc, "reason", None)
            label = type(reason).__name__ if reason is not None else type(exc).__name__
            raise ProviderError(f"Could not reach the configured provider ({label}).") from None
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ProviderError("Provider returned a response that was not valid JSON.") from None
        try:
            content = result["choices"][0]["message"]["content"]
        except (TypeError, KeyError, IndexError):
            raise ProviderError("Provider response did not match the chat-completions schema.") from None
        if not isinstance(content, str):
            raise ProviderError("Provider returned non-text content; this client supports text replies only.")
        return content


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(__doc__.splitlines()[0], file=sys.stderr)
        print('Usage: python3 tools/model_provider.py "Your prompt"', file=sys.stderr)
        return 2
    try:
        provider = OpenAICompatibleProvider(ProviderConfig.from_env())
        answer = provider.chat([{"role": "user", "content": " ".join(args)}])
    except (ValueError, ProviderError) as exc:
        print(f"Provider check failed: {exc}", file=sys.stderr)
        return 1
    print(answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
