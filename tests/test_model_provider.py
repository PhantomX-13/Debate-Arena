import json
import os
import unittest
from unittest.mock import patch

from tools.model_provider import (
    OpenAICompatibleProvider,
    ProviderConfig,
    ProviderError,
)


class FakeResponse:
    def __init__(self, data):
        self.data = json.dumps(data).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.data


class ModelProviderTests(unittest.TestCase):
    def test_openai_compatible_request_and_reply(self):
        response = {"choices": [{"message": {"content": "Ready"}}]}

        def fake_open(request, timeout):
            self.assertEqual(request.full_url, "http://localhost:11434/v1/chat/completions")
            self.assertEqual(request.get_header("Authorization"), "Bearer local-secret")
            payload = json.loads(request.data)
            self.assertEqual(payload["model"], "local-model")
            self.assertEqual(payload["messages"][0]["content"], "Hi")
            self.assertEqual(payload["temperature"], 0.2)
            self.assertEqual(timeout, 12)
            return FakeResponse(response)

        provider = OpenAICompatibleProvider(ProviderConfig(
            "http://localhost:11434/v1", "local-model", "local-secret", 12
        ))
        with patch("urllib.request.urlopen", side_effect=fake_open):
            self.assertEqual(provider.chat([{"role": "user", "content": "Hi"}], temperature=0.2), "Ready")

    def test_accepts_full_endpoint_url_and_optional_key(self):
        provider = OpenAICompatibleProvider(ProviderConfig(
            "http://127.0.0.1:1234/v1/chat/completions", "test"
        ))
        self.assertEqual(provider.endpoint, "http://127.0.0.1:1234/v1/chat/completions")

        def fake_open(request, timeout):
            self.assertIsNone(request.get_header("Authorization"))
            return FakeResponse({"choices": [{"message": {"content": "local"}}]})

        with patch("urllib.request.urlopen", side_effect=fake_open):
            self.assertEqual(provider.chat([{"role": "user", "content": "Hi"}]), "local")

    def test_rejects_malformed_provider_reply(self):
        provider = OpenAICompatibleProvider(ProviderConfig("http://localhost/v1", "test"))
        with patch("urllib.request.urlopen", return_value=FakeResponse({"unexpected": []})):
            with self.assertRaisesRegex(ProviderError, "chat-completions schema"):
                provider.chat([{"role": "user", "content": "Hi"}])

    def test_requires_endpoint_and_model_environment(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "BASE_URL and DEBATE_ARENA_MODEL"):
                ProviderConfig.from_env()


if __name__ == "__main__":
    unittest.main()
