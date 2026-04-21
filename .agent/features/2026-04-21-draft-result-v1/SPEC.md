# Feature: draft_result v1 + drafting stage wiring

**Date:** 2026-04-21  
**Slug:** `draft-result-v1`

## Goal

Introduce a versioned **`draft_result`** JSON contract (SPEC §7.7) and emit schema-valid `drafting/output.json` from the assigned-topic Phase 0 skeleton, without live models.

## Scope

- `schemas/json/draft_result.schema.json` (v1).
- Deterministic stub builder; critique and revision `input.json` reference the canonical `draft_result` document.
- Unit and integration tests; README / SPEC / PLANS pointers.

## Non-goals

- Real drafting LLM; `final/` packaging schema.

## Acceptance

- `pytest -q` green; `drafting/output.json` validates as `draft_result`.
