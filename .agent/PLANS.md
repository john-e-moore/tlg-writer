# PLANS.md

ExecPlan standard for **tlg-writer**. An **ExecPlan** is a living execution document stored **in this file** as a dated section (not a separate file unless agreed otherwise).

## When to use one

Create or update an ExecPlan before or during implementation when work is complex, cross-cutting, or operationally visible—especially multi-stage pipeline changes, schema or artifact contract changes, agent routing, observability, labeling/retrieval/evaluation, or ingestion.

Optional for tiny fixes (typos, single-test edits, comment-only changes).

## Early vertical slices (pipeline work)

When adding or extending the editorial pipeline, treat **operator-visible feedback** as the default first milestone: a command that produces a new `artifacts/runs/<run_id>/` tree through `final/` (see `.agent/SPEC.md` §18 Phase 0 and `.agent/AGENTS.md` **Early feedback loops**). Stubs, fixtures, and **mocked** LLM responses are encouraged until contracts stabilize; do not block this on exhaustive archive labeling or gold-set completion.

**First** ExecPlan for greenfield pipeline work should usually be titled like: `ExecPlan: Assigned-topic skeleton run (mocked LLM) — <YYYY-MM-DD>`, with acceptance criteria that name concrete paths under `artifacts/runs/…` and the tests that lock them.

## Links to other docs

- Baseline requirements: `.agent/SPEC.md`
- Agent behavior and path conventions: `.agent/AGENTS.md`
- Feature brief (optional but recommended for substantial features): `.agent/features/<YYYY-MM-DD>-<feature-slug>/SPEC.md`

## ExecPlan entry format

Append a new top-level section per plan:

```markdown
## ExecPlan: <short title> — <YYYY-MM-DD>

Links: branch `<name>`; brief `.agent/features/.../SPEC.md` or `N/A`; PR `<url>` or `pending`.

Status: `planned` | `in_progress` | `blocked` | `done`
```

Keep **Progress**, **Surprises & Discoveries**, **Decision Log**, and **Outcomes** updated as you go.

## Principles

- **Self-contained**: executable with this section + current repo.
- **Outcome-focused**: observable behavior and artifacts when done.
- **Executable**: concrete steps, commands, expected signals.
- **Observable**: names `artifacts/runs/<run_id>/` paths and any new `data/` outputs.
- **Feedback-friendly**: where pipeline work is involved, the plan’s first “done” slice should be inspectable under `artifacts/runs/…` (mocks OK) before large quality investments.
- **Living**: edit in place; do not fork duplicate plans.
- **Safe**: idempotence and recovery spelled out.

## Required sections

Each ExecPlan section must contain (headings may be `###` under the plan `##`):

1. Purpose / big picture  
2. Progress (dated checkboxes)  
3. Surprises & discoveries (with evidence pointers)  
4. Decision log  
5. Outcomes & retrospective  
6. Context and orientation (key paths: scripts, `data/`, `prompts/`, `schemas/json/`, `src/`)  
7. Plan of work  
8. Concrete steps (commands from repo root, e.g. `pytest -q`, `python scripts/extract_docx_metadata.py --help`)  
9. Validation and acceptance  
10. Idempotence and recovery  
11. Artifacts and notes (files and dirs that must exist)  
12. Interfaces and dependencies (modules, schemas, external services)

## Style

- Prose first; short lists where they help.
- Repository-relative paths only.
- Evidence: one log snippet, test name, or artifact path—not walls of output.
- Easy to `git diff`.

## Acceptance bar (this repo)

Done means: scoped behavior works end-to-end (or end-to-end **with mocks** when that is the declared scope), emitted artifacts under `artifacts/runs/…` are inspectable, tests cover important new logic, rerun behavior is known, and `.agent/SPEC.md` / `.agent/AGENTS.md` stay accurate if contracts changed.

If live models or APIs are unavailable: document mocks used and list follow-up checks when keys exist.

## Template (copy inside a new `## ExecPlan: …` section)

### Purpose / big picture

Operator-visible outcome; how we know it succeeded.

### Progress

- [ ] (YYYY-MM-DD) Planning
- [ ] Implementation
- [ ] Validation + docs

### Surprises & discoveries

- Observation: …  
  Evidence: artifact path, test name, or command one-liner

### Decision log

- Decision: … — Rationale: … — Date:

### Outcomes & retrospective

What shipped, what is deferred, lessons.

### Context and orientation

Touch points: `scripts/`, `data/raw/pieces/…`, `prompts/…`, `schemas/json/…`, tests.

### Plan of work

Ordered edits and why.

### Concrete steps

```bash
cd /path/to/tlg-writer
pytest -q
python scripts/extract_docx_metadata.py --help
```

### Validation and acceptance

Observable checks (schemas, files under run dir, test filters).

### Idempotence and recovery

Re-run scripts; partial failure cleanup; git revert notes.

### Artifacts and notes

Expected paths, e.g. `artifacts/runs/<run_id>/manifest.json`, new schema files.

### Interfaces and dependencies

Public functions, CLIs, env vars, external APIs.

## Optional index

Maintain a bullet list here for in-flight work:

- `2026-04-21 — ExecPlan: Corpus JSON schemas (metadata + label/feature contracts) — done (PR #2 merged) — agent`
- `2026-04-21 — ExecPlan: Corpus batch stub (labels + features + manifest) — done (PR #3 merged) — agent`
- `2026-04-21 — ExecPlan: Editorial archetype taxonomy v1 — in_progress (PR #4) — agent`
- `2026-04-21 — ExecPlan: Assigned-topic skeleton run (mocked LLM) — done (PR #1 merged) — agent`

---

## ExecPlan: Corpus JSON schemas (metadata + label/feature contracts) — 2026-04-21

Links: branch `feature/corpus-json-schemas`; brief `.agent/features/2026-04-21-corpus-json-schemas/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/2`.

Status: `done`

### Purpose / big picture

Ship SPEC §21 step 2: explicit `schemas/json/` contracts for `pieces_metadata_*.json` batches (today’s extraction script), plus minimal `piece_label` and `piece_features` envelopes aligned with SPEC §9 and §13. Extraction writes only schema-valid JSON; tests lock the contracts.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR evidence)

### Surprises & discoveries

- Observation: Sibling-file ``$ref`` between batch and record schemas failed with default `jsonschema` resolution unless every schema is registered with stable file URIs; embedding the record under `pieces_metadata_batch` `$defs` avoided that coupling.  
  Evidence: local `python -c` ref-resolution attempts before the final layout.

### Decision log

- Decision: Embed `piece_docx_metadata_record` under `pieces_metadata_batch` `$defs` (no sibling `$ref` file) — Rationale: default `jsonschema` ref resolution to local files was brittle without a custom registry — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #2 (`https://github.com/john-e-moore/tlg-writer/pull/2`). Validation: `pytest -q` on branch before merge.

### Context and orientation

Touch points: `scripts/extract_docx_metadata.py`, `schemas/json/`, `src/tlg_writer/json_schema.py`, `tests/`, `.agent/SPEC.md` §13.

### Plan of work

1. Add JSON Schemas (batch + record + label + features stubs).
2. Validate in `extract_docx_metadata.py` before writing the batch file.
3. Tests: fixtures + synthetic `.docx` smoke.
4. README and SPEC index line for batch schema.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/extract_docx_metadata.py --help
```

### Validation and acceptance

- `pytest -q` passes.
- `extract_docx_metadata.py` writes only after successful validation (empty input dir still emits valid `[]`).
- Fixture JSON validates against `piece_label` and `piece_features`.

### Idempotence and recovery

Metadata script still writes a new timestamped filename each run; validation failure exits before any file write.

### Artifacts and notes

- New: `schemas/json/pieces_metadata_batch.schema.json` (includes `$defs.piece_docx_metadata_record`), `piece_label.schema.json`, `piece_features.schema.json`.

### Interfaces and dependencies

- **CLI:** `extract_docx_metadata.py` unchanged flags; behavior adds validation pre-write.
- **Library:** `tlg_writer.json_schema.validate`.

---

## ExecPlan: Corpus batch stub (labels + features + manifest) — 2026-04-21

Links: branch `feature/corpus-batch-stub`; brief `.agent/features/2026-04-21-corpus-batch-stub/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/3`.

Status: `done`

### Purpose / big picture

Deliver SPEC §21 steps 3–4 as an operator-visible **stub** slice: read a validated metadata batch, write schema-valid `piece_label` / `piece_features` JSON under `data/processed/pieces/{labeled,extracted_features}/`, and emit `artifacts/runs/<run_id>/` with `corpus_batch_manifest`, `summary.md`, and `logs/run.log`. No LLM calls.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR #3 evidence)

### Surprises & discoveries

- Observation: Editorial `run_manifest` enums (`assigned`/`auto`) do not fit corpus tooling; introduced `corpus_batch_manifest` instead of overloading `run_manifest`.  
  Evidence: `schemas/json/corpus_batch_manifest.schema.json`.

### Decision log

- Decision: `run_id` pattern `…__corpus__<slug>` via `build_corpus_batch_run_id` — Rationale: keeps editorial id rules intact while matching timestamped run folders in `.agent/AGENTS.md` spirit — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #3 (`https://github.com/john-e-moore/tlg-writer/pull/3`).

### Context and orientation

Touch points: `scripts/run_corpus_batch_stub.py`, `src/tlg_writer/corpus_batch_stub.py`, `src/tlg_writer/run_id.py`, `schemas/json/corpus_batch_manifest.schema.json`, `tests/integration/test_corpus_batch_stub.py`, `.agent/SPEC.md` §21.

### Plan of work

1. Add `corpus_batch_manifest` schema + `build_corpus_batch_run_id`.
2. Implement batch reader + stub writers + run tree.
3. CLI + integration tests + README/SPEC/PLANS updates.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_corpus_batch_stub.py --help
```

### Validation and acceptance

- `pytest -q` passes (manifest schema, skip-on-error row, `FileExistsError` on duplicate run dir).
- Smoke: CLI with absolute `--labels-dir` / `--features-dir` / `--artifacts-root` under `/tmp` writes `manifest.json` that validates.

### Idempotence and recovery

Re-run allocates a new `run_id` unless `--run-id` is passed; duplicate existing run directory raises `FileExistsError`. Per-piece JSON filenames are deterministic from `piece_id` hash; re-running the stub overwrites same stems (documented limitation until real pipelines version outputs).

### Artifacts and notes

- Under `artifacts/runs/<run_id>/`: `manifest.json`, `summary.md`, `logs/run.log`.
- Data outputs: `data/processed/pieces/labeled/piece_<hash16>.json` and `…/extracted_features/…` (gitignored by default).

### Interfaces and dependencies

- **CLI:** `scripts/run_corpus_batch_stub.py` (`--metadata-batch`, `--slug`, optional dirs, `--run-id`, `--utc`).
- **Library:** `tlg_writer.corpus_batch_stub.run_corpus_batch_stub`.
- **External:** none.

---

## ExecPlan: Assigned-topic skeleton run (mocked LLM) — 2026-04-21

Links: branch `feature/assigned-skeleton-run`; brief `.agent/features/2026-04-21-assigned-skeleton-run/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/1`.

Status: `done`

### Purpose / big picture

Deliver Phase 0 from `.agent/SPEC.md` §18: operators can run one command and open a complete `artifacts/runs/<run_id>/` tree through `final/`, with honest stubs, explicit **assigned** `topic_selection` skip, schema-validated `manifest.json`, and tests that lock layout and contracts without live models.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR evidence; merge will flip status to done)

### Surprises & discoveries

- Observation: `pytest` initially created `__pycache__` under `tests/` that were almost committed; added standard Python bytecode ignores.  
  Evidence: `.gitignore` (`__pycache__/`, `*.py[cod]`).

### Decision log

- Decision: Keep stub stage `output.json` shapes under `skeleton_stage_output` until per-stage domains (e.g. `piece_brief`) are implemented — Rationale: one schema stabilizes Phase 0 tests without pretending brief/critique are final — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #1; deferred: auto-topic runner, real LLM wrappers, archive retrieval.

### Context and orientation

Touch points: `scripts/run_assigned_skeleton.py`, `src/tlg_writer/skeleton_pipeline.py`, `schemas/json/`, `prompts/<stage>/`, `tests/integration/test_skeleton_pipeline.py`, `.agent/SPEC.md` §12 / §18.

### Plan of work

1. Add packaging + `jsonschema` dependency.
2. Add `run_manifest` + stub stage schemas.
3. Implement skeleton runner + CLI.
4. Placeholder prompts per stage dir naming in `.agent/AGENTS.md`.
5. Integration tests on `tmp_path`; `.gitignore` `artifacts/runs/`.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_assigned_skeleton.py --topic "smoke" --slug smoke-test
```

### Validation and acceptance

- `pytest -q` passes (layout, manifest + key `output.json` schema, topic_selection skip text, `final/piece.md`).
- Smoke: CLI creates a new directory under `artifacts/runs/` and prints its path.
- Idempotence: same `--run-id` twice errors with `FileExistsError`; normal CLI uses fresh UTC ids.

### Idempotence and recovery

Re-running the CLI always allocates a new `run_id` unless `--run-id` is passed (tests). Partial failure before completion: not supported mid-run; delete the folder and retry.

### Artifacts and notes

Expected under `artifacts/runs/<run_id>/`: `manifest.json`, `config.json`, `logs/run.log`, stage dirs per `.agent/AGENTS.md`, each with `input.json`, `output.json`, `summary.md`, `metrics.json`, plus `final/piece.md`.

### Interfaces and dependencies

- **CLI:** `scripts/run_assigned_skeleton.py` (`--topic`, `--slug`, optional `--artifacts-root`, `--run-id`, `--utc`).
- **Library:** `tlg_writer.skeleton_pipeline.run_assigned_skeleton`.
- **Env:** none required for Phase 0.
- **External:** none (no HTTP).

---

## ExecPlan: Editorial archetype taxonomy v1 — 2026-04-21

Links: branch `feature/editorial-archetype-taxonomy`; brief `.agent/features/2026-04-21-editorial-archetype-taxonomy/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/4`.

Status: `in_progress`

### Purpose / big picture

Deliver SPEC §21 step 5 and §8 “represented explicitly in code”: a versioned, schema-validated taxonomy with stable ids, library access, optional hooks on `piece_label`, and a small CLI for operators—without blocking corpus stubs or Phase 0 runs.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR evidence; link PR when opened)

### Surprises & discoveries

- Observation: `piece_label` uses an inline enum under `$defs` so tests can assert it stays aligned with bundled taxonomy JSON without fragile cross-file `$ref` resolution — Evidence: `tests/unit/test_editorial_archetype_taxonomy.py::test_taxonomy_ids_match_piece_label_enum`

### Decision log

- Decision: Keep `labels.editorial` permissive (`additionalProperties: true`) but declare optional `primary_archetype_id` / `alternate_archetype_ids` with an inline enum matching bundled v1 ids — Rationale: validates known keys when present without breaking empty stub labels — Date: 2026-04-21

### Outcomes & retrospective

Opened as PR #4 (`https://github.com/john-e-moore/tlg-writer/pull/4`); merge will flip Status to `done`.

### Context and orientation

Touch points: `schemas/json/editorial_archetype_taxonomy.schema.json`, `src/tlg_writer/editorial_archetype_taxonomy.v1.json`, `src/tlg_writer/editorial_archetypes.py`, `schemas/json/piece_label.schema.json`, `scripts/list_editorial_archetypes.py`, `tests/unit/test_editorial_archetype_taxonomy.py`, `.agent/SPEC.md` §8 / §21.

### Plan of work

1. Add taxonomy schema + bundled v1 JSON + setuptools package data.
2. Extend `piece_label` with optional archetype fields referencing stable ids.
3. Tests: schema validation, enum alignment, bad-id rejection.
4. CLI + README + SPEC pointer + feature brief + this ExecPlan.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/list_editorial_archetypes.py --help
python scripts/list_editorial_archetypes.py
```

### Validation and acceptance

- `pytest -q` passes (including taxonomy file validates against `editorial_archetype_taxonomy` and ids match `piece_label` enum).
- Smoke: `list_editorial_archetypes.py` prints eight rows; `--json` round-trips valid document.

### Idempotence and recovery

Read-only taxonomy; no run directories. Re-install `pip install -e ".[dev]"` after changing packaged JSON.

### Artifacts and notes

- Bundled: `src/tlg_writer/editorial_archetype_taxonomy.v1.json` (canonical v1 list).
- No new `artifacts/runs/` contract in this slice (N/A for PR template checklist).

### Interfaces and dependencies

- **Library:** `tlg_writer.editorial_archetypes.load_editorial_archetype_taxonomy`, `raw_taxonomy_document`.
- **CLI:** `scripts/list_editorial_archetypes.py` (`--json`, `--version`).
- **External:** none.
