# Feature: Corpus JSON schemas (metadata batch, labels, features)

**Date:** 2026-04-21  
**Tracks:** `.agent/SPEC.md` §9, §13; `.agent/SPEC.md` §21 step 2.

## Goal

Formalize JSON Schemas for historical-corpus artifacts that downstream labeling, retrieval, and extraction will share:

- Batch output from `scripts/extract_docx_metadata.py` (`pieces_metadata_<YYYYMMDDHHMM>.json`).
- Per-piece editorial labels (`piece_label`) and extracted measurements (`piece_features`) as minimal, versioned envelopes so v1 scripts can extend fields without breaking validation.

## In scope

- New schemas under `schemas/json/` and validation of metadata batches before write.
- `pytest` proving schema validation and one end-to-end metadata extraction on a synthetic `.docx`.

## Out of scope

- Real labeling or feature-extraction pipelines (separate PR per §21 steps 3–4).
- Changes to on-disk `data/` corpus contents.

## Acceptance

- `extract_docx_metadata.py` refuses to write a batch that fails schema validation.
- `piece_label` and `piece_features` fixtures validate and document the intended v1 shape.
