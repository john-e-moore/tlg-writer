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

## Phase 0: auto-topic skeleton run (stub)

Same full stage layout and stub downstream stages as the assigned runner, but `run_id` uses `__auto__`, manifest/config `mode` is `auto`, `inputs/output.json` is an **`inputs_result`** with `topic.source: auto_stub`, and `topic_selection/output.json` is a **`topic_selection_result`** **completed** stub (empty `candidates_considered`; no search, no LLM):

```bash
python scripts/run_auto_skeleton.py --slug macro-stub
# optional: --topic "Override label"  --artifacts-root path  --run-id …  --utc YYYY-MM-DDTHH:MM:SS
```

## Tests

Every pipeline stage directory under a Phase 0 skeleton run writes **schema-valid `output.json`**: intake uses **`inputs_result`**, **`source_reading_result`**, and **`topic_selection_result`** (v1; assigned = skip, auto stub = completed); downstream stages use **`framing_decision`**, **`retrieval_result`**, **`piece_brief`**, **`draft_result`**, **`critique_result`**, **`revision_result`**, **`evaluation_result`**, and **`final_deliverable`** (all v1 contracts under `schemas/json/`).

```bash
pytest -q
```

Pull requests (and pushes to `main`) run the same suite in GitHub Actions; see `.github/workflows/ci.yml`.

## Library notes

- **Stage → output schema:** `tlg_writer.stage_schemas.OUTPUT_SCHEMA_BY_STAGE` is the single registry for pipeline `output.json` validation (used by Phase 0 skeleton runners and integration tests).
- **LLM calls:** use `tlg_writer.llm_client` (`StubLLMClient` by default; `llm_client_from_env()` reads `TLG_LLM_BACKEND` / `OPENAI_API_KEY`). Do not scatter raw HTTP across the codebase.

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

## Editorial archetype taxonomy (v1)

SPEC §8 archetypes are bundled as validated JSON (`src/tlg_writer/editorial_archetype_taxonomy.v1.json`, schema `schemas/json/editorial_archetype_taxonomy.schema.json`). List them:

```bash
python scripts/list_editorial_archetypes.py
python scripts/list_editorial_archetypes.py --json
```

Optional `piece_label` fields `labels.editorial.primary_archetype_id` and `alternate_archetype_ids` reference the same stable ids (`schemas/json/piece_label.schema.json`).

## Gold set index (SPEC §9.5 / §21)

Curated “gold” pieces are listed in a single JSON document validated by `schemas/json/gold_set_index.schema.json`. Each entry uses `piece_relative_to_repo` (same join key as metadata batches) plus one or more roles (`canonical_voice_example`, historical/future/data archetype examples, or `contrast_weak_or_atypical`). Optional `primary_archetype_id` must match a bundled taxonomy id.

```bash
python scripts/validate_gold_set_index.py path/to/gold_set_index.json
python scripts/validate_gold_set_index.py
```

The no-argument form validates `tests/fixtures/corpus/gold_set_index_minimal.json`. Use `--no-semantics` for JSON Schema only (skips duplicate-path and archetype checks).
