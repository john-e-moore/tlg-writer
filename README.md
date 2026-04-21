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

```bash
python scripts/extract_docx_metadata.py --help
```
