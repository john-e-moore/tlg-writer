"""LLM client protocol, stub, optional OpenAI (mocked), and env factory."""

from __future__ import annotations

import json
import os
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from tlg_writer.llm_client import (
    ChatMessage,
    OpenAIChatLLMClient,
    StubLLMClient,
    llm_client_from_env,
)


def test_stub_llm_client_returns_reply() -> None:
    c = StubLLMClient(reply="hello")
    r = c.complete_chat(messages=[ChatMessage(role="user", content="x")], model="m")
    assert r.text == "hello"
    assert r.input_tokens == 0


def test_llm_client_from_env_defaults_to_stub() -> None:
    with patch.dict(os.environ, {"TLG_LLM_BACKEND": "stub"}, clear=False):
        c = llm_client_from_env()
    assert isinstance(c, StubLLMClient)


def test_llm_client_from_env_openai_requires_key() -> None:
    with patch.dict(
        os.environ,
        {"TLG_LLM_BACKEND": "openai", "OPENAI_API_KEY": ""},
        clear=False,
    ):
        with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
            llm_client_from_env()


def test_llm_client_from_env_rejects_unknown_backend() -> None:
    with patch.dict(os.environ, {"TLG_LLM_BACKEND": "wat"}, clear=False):
        with pytest.raises(ValueError, match="unsupported"):
            llm_client_from_env()


def test_openai_client_parses_chat_completion() -> None:
    payload = {
        "choices": [{"message": {"content": "done"}}],
        "model": "gpt-test",
        "usage": {"prompt_tokens": 2, "completion_tokens": 1},
    }
    inner = MagicMock()
    inner.read.return_value = json.dumps(payload).encode("utf-8")
    cm = MagicMock()
    cm.__enter__.return_value = inner
    cm.__exit__.return_value = None

    with patch("tlg_writer.llm_client.urllib.request.urlopen", return_value=cm):
        client = OpenAIChatLLMClient(api_key="sk-test")
        r = client.complete_chat(
            messages=[ChatMessage(role="user", content="hi")],
            model="gpt-test",
        )
    assert r.text == "done"
    assert r.model == "gpt-test"
    assert r.input_tokens == 2
    assert r.output_tokens == 1
    assert r.latency_ms >= 0.0


def test_openai_client_retries_with_max_completion_tokens() -> None:
    payload = {
        "choices": [{"message": {"content": "done"}}],
        "model": "gpt-test",
        "usage": {"prompt_tokens": 2, "completion_tokens": 1},
    }

    first_err = urllib.error.HTTPError(
        url="https://api.openai.com/v1/chat/completions",
        code=400,
        msg="Bad Request",
        hdrs=None,
        fp=MagicMock(),
    )
    first_err.fp.read.return_value = (
        b'{"error":{"message":"Unsupported parameter: \'max_tokens\' is not supported with this '
        b'model. Use \'max_completion_tokens\' instead."}}'
    )

    second_inner = MagicMock()
    second_inner.read.return_value = json.dumps(payload).encode("utf-8")
    second_cm = MagicMock()
    second_cm.__enter__.return_value = second_inner
    second_cm.__exit__.return_value = None

    sent_bodies: list[dict[str, object]] = []

    def _urlopen_side_effect(req, timeout=None):  # type: ignore[no-untyped-def]
        sent_bodies.append(json.loads(req.data.decode("utf-8")))
        if len(sent_bodies) == 1:
            raise first_err
        return second_cm

    with patch("tlg_writer.llm_client.urllib.request.urlopen", side_effect=_urlopen_side_effect):
        client = OpenAIChatLLMClient(api_key="sk-test")
        r = client.complete_chat(
            messages=[ChatMessage(role="user", content="hi")],
            model="gpt-test",
            max_tokens=321,
        )

    assert r.text == "done"
    assert len(sent_bodies) == 2
    assert sent_bodies[0]["max_tokens"] == 321
    assert "max_completion_tokens" not in sent_bodies[0]
    assert "max_tokens" not in sent_bodies[1]
    assert sent_bodies[1]["max_completion_tokens"] == 321
