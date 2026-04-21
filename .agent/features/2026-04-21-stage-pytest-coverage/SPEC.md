# Feature: Stage and artifact writer pytest coverage (2026-04-21)

## Goal

Satisfy `.agent/SPEC.md` §21 step 8: extend automated tests so **every** editorial skeleton stage emits schema-valid `output.json` and `stage_metrics`-valid `metrics.json`, and corpus batch stub artifact helpers / edge cases are covered without live APIs.

## Scope

- Integration assertions on a full assigned skeleton run (tmp_path).
- Corpus stub: deterministic `piece_artifact_stem`, empty metadata batch, run log smoke.
- Docs: `.agent/SPEC.md` §21 step 8 shipped note; ExecPlan in `.agent/PLANS.md`.

## Out of scope

- New JSON Schemas or pipeline behavior changes.
- Live LLM or retrieval tests.
