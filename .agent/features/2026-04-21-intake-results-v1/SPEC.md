# Feature: Intake stage v1 schemas (inputs, source_reading, topic_selection)

**Date:** 2026-04-21  
**Slug:** `intake-results-v1`

## Goal

Replace generic `skeleton_stage_output` for the first three pipeline stages with versioned **`inputs_result`**, **`source_reading_result`**, and **`topic_selection_result`** contracts on assigned-topic runs, and thread canonical documents into downstream `input.json` files.

## Scope

- Three JSON Schemas + stub builders + fixtures + `tests/unit/test_intake_results_schema.py`.
- Skeleton wiring; **`framing/input.json`** references `source_reading_result` and `topic_selection_result`.
- `prompts/inputs/`; prompt notes for source_reading and topic_selection; README / SPEC §13 + §21 step 14 / PLANS.

## Non-goals

- Auto-topic selection completed-state schema (separate slice when auto runner exists).

## Acceptance

- `pytest -q` green; all stage `output.json` files validate in integration sweep.
