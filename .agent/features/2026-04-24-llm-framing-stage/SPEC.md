# Feature: LLM framing stage (assigned Phase 0 opt-in)

## Purpose

Allow an **assigned-topic** Phase 0 skeleton run to produce a **real** `framing_decision` from a chat completion (JSON validated against `schemas/json/framing_decision.schema.json`) while keeping other stages stubbed—env-gated live OpenAI or an injected `llm_client` in tests.

## Behavior

- Library: `run_assigned_skeleton(..., llm_framing=True, framing_model=..., llm_client=...)`.
- CLI: `scripts/run_assigned_skeleton.py --llm-framing [--llm-framing-model ...]`.
- Default client resolution when `llm_framing` and `llm_client` is omitted: `llm_client_from_env()`. `StubLLMClient` is rejected with a clear error.
- Prompts: `prompts/framing/system.md`, `prompts/framing/user.md`.

## Out of scope (this slice)

- Auto-topic runner (`run_auto_skeleton`) wiring for `llm_framing`.
- Live LLM for drafting, brief, or other stages.
