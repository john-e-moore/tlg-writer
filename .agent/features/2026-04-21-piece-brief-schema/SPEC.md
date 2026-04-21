# Feature: piece_brief v1 + brief stage wiring

**Date:** 2026-04-21  
**Branch:** `feature/piece-brief-schema`

## Intent

Ship SPEC §21 step 7 **first increment**: canonical **`piece_brief`** JSON Schema (SPEC §7.6 / §13) and assigned-topic skeleton runs that write schema-valid `brief/output.json`, without live LLMs or changing downstream stage schemas beyond drafting consuming the brief thesis.

## Acceptance

- `schemas/json/piece_brief.schema.json` validates minimal fixture and stub builder output.
- Optional `primary_archetype_id` enum stays aligned with `piece_label` / bundled taxonomy ids.
- Integration test locks `brief/output.json` to `piece_brief` validation.

## Out of scope

- Real brief LLM agent, `framing_decision` / `retrieval_result` domain schemas, or critique/evaluation domain objects.
