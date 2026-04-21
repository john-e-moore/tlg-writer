# Feature: critique_result v1 (2026-04-21)

## Summary

Add `critique_result` JSON Schema (SPEC §13, §7.8, §15.1 rubric dimensions) and teach the assigned-topic Phase 0 skeleton to write schema-valid `critique/output.json` using a deterministic stub (no LLM).

## Requirements trace

- `.agent/SPEC.md` §7.8 (critique outputs), §13 schema list, §15.1 (rubric dimensions).

## Non-goals

- Live critic agents, threshold loops, or `evaluation_result` in the same slice.
- Replacing the drafting-stage skeleton envelope (still generic `skeleton_stage_output`).

## Acceptance

- `pytest` locks schema validation, stub builder, and integration mapping for `critique/output.json`.
- A normal skeleton run produces inspectable JSON that validates as `critique_result`.
