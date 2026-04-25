# Feature: Assigned source-file ingestion (Phase 0 deterministic)

## Purpose

Deepen assigned-topic runs so `source_reading` can ingest explicit local files and emit non-stub highlights/claims without requiring live models.

## Behavior

- CLI: `scripts/run_assigned_skeleton.py --source-path <path>` (repeatable).
- Library: `run_assigned_skeleton(..., source_paths=[Path(...), ...])`.
- Supported source extensions: `.txt`, `.md`, `.json`, `.docx`.
- `source_reading/output.json` switches `reading_status` to `completed` when source files are provided.
- `source_reading/input.json` records deterministic `source_notes` including path and preview.
- `config.json` records `source_ingestion` (`count`, `paths`) for operator traceability.

## Out of scope (this slice)

- URL fetching.
- Live LLM source summarization.
- Auto mode source ingestion.
