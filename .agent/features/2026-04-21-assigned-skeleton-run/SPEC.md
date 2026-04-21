# Feature: Phase 0 assigned-topic skeleton run

**Date:** 2026-04-21  
**Branch:** `feature/assigned-skeleton-run`

## Intent

Ship the first vertical slice from `.agent/SPEC.md` §18 Phase 0: a runnable **assigned-topic** path that materializes the full `artifacts/runs/<run_id>/` tree (stage dirs, `manifest.json`, `config.json`, per-stage `input.json` / `output.json` / `summary.md` / `metrics.json`, readable `final/piece.md`) using **stubs only**—no live LLM calls, no blocking on corpus labeling.

## Operator entry

- CLI: `python scripts/run_assigned_skeleton.py --topic "…" --slug <kebab-case>`
- Default output root: `artifacts/runs/` (ignored by git for ad-hoc runs; tests use `tmp_path`).

## Acceptance

- `topic_selection/` exists and records an explicit **skipped** outcome for assigned mode (not a silent empty dir).
- `pytest` validates layout and JSON Schemas without API keys.
- `schemas/json/run_manifest.schema.json` and stub stage/metrics schemas cover emitted contracts.

## Out of scope (this PR)

- Auto-topic mode execution (manifest must still allow `mode: auto` in future; run harness here is assigned-only).
- Real prompts, retrieval, rubric scoring, or `piece_brief` / `critique_result` schema wiring.
