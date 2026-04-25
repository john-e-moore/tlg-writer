"""Small LLM HTTP boundary (see ``.agent/AGENTS.md`` module boundaries).

Phase 0 defaults to :class:`StubLLMClient` (no network). Optional OpenAI Chat
Completions via stdlib ``urllib`` when ``TLG_LLM_BACKEND=openai`` and
``OPENAI_API_KEY`` are set (tests should keep the stub).
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True)
class ChatCompletionResult:
    """Normalized completion metadata for metrics / logging."""

    text: str
    model: str
    input_tokens: int | None
    output_tokens: int | None
    latency_ms: float


@runtime_checkable
class LLMClient(Protocol):
    def complete_chat(
        self,
        *,
        messages: list[ChatMessage],
        model: str,
        temperature: float = 0.0,
        max_tokens: int = 1024,
    ) -> ChatCompletionResult:
        """Run a single chat completion. Implementations must not log secrets."""


class StubLLMClient:
    """Deterministic no-network client for tests and Phase 0 pipelines."""

    def __init__(self, *, reply: str = "") -> None:
        self._reply = reply or "stub: no LLM call was made."

    def complete_chat(
        self,
        *,
        messages: list[ChatMessage],
        model: str,
        temperature: float = 0.0,
        max_tokens: int = 1024,
    ) -> ChatCompletionResult:
        _ = messages, temperature, max_tokens
        return ChatCompletionResult(
            text=self._reply,
            model=model or "stub",
            input_tokens=0,
            output_tokens=0,
            latency_ms=0.0,
        )


class OpenAIChatLLMClient:
    """Minimal OpenAI Chat Completions client (stdlib only; no ``openai`` SDK)."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        timeout_s: float = 120.0,
    ) -> None:
        if not api_key:
            raise ValueError("api_key must be non-empty")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_s = timeout_s

    def complete_chat(
        self,
        *,
        messages: list[ChatMessage],
        model: str,
        temperature: float = 0.0,
        max_tokens: int = 1024,
    ) -> ChatCompletionResult:
        url = f"{self._base_url}/chat/completions"
        body = {
            "model": model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
            "max_tokens": max_tokens,
        }
        started = time.perf_counter()
        try:
            raw = self._post_chat(url=url, body=body)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:2000]
            if (
                e.code == 400
                and "max_tokens" in detail
                and "max_completion_tokens" in detail
            ):
                # Some newer OpenAI models reject ``max_tokens`` in chat/completions.
                fallback_body = dict(body)
                fallback_body.pop("max_tokens", None)
                fallback_body["max_completion_tokens"] = max_tokens
                try:
                    raw = self._post_chat(url=url, body=fallback_body)
                except urllib.error.HTTPError as e2:
                    detail2 = e2.read().decode("utf-8", errors="replace")[:2000]
                    raise RuntimeError(f"OpenAI HTTP {e2.code}: {detail2}") from e2
            else:
                raise RuntimeError(f"OpenAI HTTP {e.code}: {detail}") from e
        latency_ms = (time.perf_counter() - started) * 1000.0
        payload = json.loads(raw)
        try:
            text = str(payload["choices"][0]["message"]["content"] or "")
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"unexpected OpenAI response shape: {raw[:2000]}") from e
        usage = payload.get("usage") or {}
        return ChatCompletionResult(
            text=text,
            model=str(payload.get("model") or model),
            input_tokens=_as_int(usage.get("prompt_tokens")),
            output_tokens=_as_int(usage.get("completion_tokens")),
            latency_ms=latency_ms,
        )

    def _post_chat(self, *, url: str, body: dict[str, object]) -> str:
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            method="POST",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=self._timeout_s) as resp:
            return resp.read().decode("utf-8")


def _as_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    return None


def llm_client_from_env() -> LLMClient:
    """
    Resolve an :class:`LLMClient` from environment (no secrets in code).

    - ``TLG_LLM_BACKEND`` (optional): ``stub`` (default) or ``openai``.
    - ``OPENAI_API_KEY``: required when backend is ``openai``.
    """
    backend = os.environ.get("TLG_LLM_BACKEND", "stub").strip().lower()
    if backend in ("", "stub", "none", "off"):
        return StubLLMClient()
    if backend == "openai":
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not key:
            raise RuntimeError("TLG_LLM_BACKEND=openai requires OPENAI_API_KEY")
        return OpenAIChatLLMClient(api_key=key)
    raise ValueError(f"unsupported TLG_LLM_BACKEND: {backend!r}")
