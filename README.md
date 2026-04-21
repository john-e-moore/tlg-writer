# tlg-writer

Observable editorial pipeline for macro advisory **pieces** (see `.agent/SPEC.md`).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Phase 0: assigned-topic skeleton run

Creates a full timestamped run directory under `artifacts/runs/` with stub stages (no API keys required):

```bash
python scripts/run_assigned_skeleton.py --topic "US payrolls and Fed cuts" --slug jobs-payrolls
```

The command prints the absolute path to the new run folder. Re-running always uses a new `run_id` (UTC timestamp in the id); a second run never overwrites the first.

## Tests

```bash
pytest -q
```

## Corpus metadata (existing)

Writes `data/raw/pieces/metadata/pieces_metadata_<YYYYMMDDHHMM>.json` (UTC). Output is validated against `schemas/json/pieces_metadata_batch.schema.json` before the file is written.

```bash
python scripts/extract_docx_metadata.py --help
```

Label and extracted-feature envelopes for future pipelines: `piece_label.schema.json`, `piece_features.schema.json` (see `tests/fixtures/corpus/` for minimal examples).

## Corpus batch (stub)

From a validated `pieces_metadata_*.json` batch, emit schema-valid stub labels and features plus a timestamped run under `artifacts/runs/` (see `schemas/json/corpus_batch_manifest.schema.json`):

```bash
python scripts/run_corpus_batch_stub.py \
  --metadata-batch data/raw/pieces/metadata/pieces_metadata_<stamp>.json \
  --slug my-batch
```

Use `--labels-dir` / `--features-dir` / `--artifacts-root` to redirect outputs (defaults write under `data/processed/pieces/…` and `artifacts/runs/`). Same `--run-id` twice errors if the run folder already exists.
