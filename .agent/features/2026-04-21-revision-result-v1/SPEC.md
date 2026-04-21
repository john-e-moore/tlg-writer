# Feature: revision_result v1 + revision stage wiring

**Date:** 2026-04-21  
**Slug:** `revision-result-v1`

## Goal

Introduce a versioned **`revision_result`** JSON contract (SPEC §7.9) and emit schema-valid `revision/output.json` from the assigned-topic Phase 0 skeleton, without live models.

## Scope

- `schemas/json/revision_result.schema.json` (v1).
- Deterministic stub builder and skeleton wiring; `evaluation/input.json` references the canonical revision document.
- Unit and integration tests; README / SPEC / PLANS pointers.

## Non-goals

- `evaluation_result` schema or real evaluators.
- Substantive revision logic or LLM calls.

## Acceptance

- `pytest -q` green; temp skeleton run `revision/output.json` validates as `revision_result`.
