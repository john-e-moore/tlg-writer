# Feature: Stage schema registry + LLM client module

**Date:** 2026-04-21  
**Slug:** `schema-registry-llm-client`

## Goal

- **Registry:** one mapping from `STAGE_DIRS` stage names to `output.json` schema stems, used by the assigned skeleton and tests.
- **LLM boundary:** `StubLLMClient`, env-based factory, and optional `OpenAIChatLLMClient` (stdlib `urllib`, no `openai` SDK dependency).

## Scope

- `tlg_writer/stage_schemas.py`, `tlg_writer/llm_client.py`, skeleton + integration test import updates, unit tests, README + SPEC + PLANS.

## Non-goals

- Wiring live LLM into the skeleton runner (still stub-only).
- OpenAI SDK or streaming.

## Acceptance

- `pytest -q` green; registry keys match `STAGE_DIRS`.
