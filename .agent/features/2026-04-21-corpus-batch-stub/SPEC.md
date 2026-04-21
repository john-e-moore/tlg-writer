# Feature: Corpus batch stub (labels + features + run manifest)

**Date:** 2026-04-21  
**Tracks:** `.agent/SPEC.md` §9, §21 steps 3–4.

## Goal

Give operators a **deterministic** path from an extracted metadata batch to:

- per-piece `piece_label` and `piece_features` files under `data/processed/pieces/labeled/` and `data/processed/pieces/extracted_features/`, and
- an inspectable `artifacts/runs/<run_id>/` folder with `corpus_batch_manifest`, `summary.md`, and `logs/run.log`.

## In scope

- `schemas/json/corpus_batch_manifest.schema.json` and validation on write.
- Library `tlg_writer.corpus_batch_stub` + CLI `scripts/run_corpus_batch_stub.py`.
- `pytest` integration tests (tmp dirs; no live APIs).
- Skip metadata rows that carry per-file `error` (counted in manifest).

## Out of scope

- Real LLM labeling, human review workflows, or archetype taxonomy.
- Changing metadata extraction behavior.

## Acceptance

- CLI prints the absolute run directory path; `manifest.json` validates.
- Outputs validate as `piece_label` / `piece_features`.
- Re-using the same `--run-id` on an existing run directory fails with `FileExistsError` (documented).
