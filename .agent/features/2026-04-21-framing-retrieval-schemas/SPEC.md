# Feature: Framing + retrieval v1 schemas (2026-04-21)

## Summary

Add `framing_decision` and `retrieval_result` JSON Schemas (SPEC §13, §7.4–7.5) and teach the assigned-topic Phase 0 skeleton to write schema-valid `framing/output.json` and `retrieval/output.json` using deterministic stubs (no LLM, no archive).

## Requirements trace

- `.agent/SPEC.md` §7.4 (framing outputs), §7.5 / §14.3 (retrieval outputs), §13 schema list.

## Non-goals

- Live retrieval, embeddings, or gold-set wiring.
- Changing drafting/critique envelopes beyond what the brief stage already consumes from retrieval.

## Acceptance

- `pytest` locks schema validation and integration layout for the two new stage outputs.
- A normal skeleton run produces inspectable JSON that validates against the new schemas.
