# Feature: Phase 0 skeleton LLM client probe (observability)

## Goal

Invoke `tlg_writer.llm_client` once per Phase 0 skeleton run so manifests/config/metrics reflect the **LLM boundary** without changing v1 `output.json` shapes or requiring live APIs.

## Behavior

- `run_assigned_skeleton` / `run_auto_skeleton` accept optional `llm_client` (defaults to `StubLLMClient()`).
- Before writing stages, the runner performs a single `complete_chat` probe (fixed system/user messages; no secrets).
- Each stage `metrics.json` includes a small `llm` object with probe token/latency/model fields; `config.json` records the same summary.
- Default remains stub-only; callers must pass a non-stub client explicitly (live calls stay opt-in and out of CI).

## Out of scope

- Using completion text to build any `output.json`.
- CLI flags for `TLG_LLM_BACKEND` (library parameter only in this slice).
