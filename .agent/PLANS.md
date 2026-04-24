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
- `2026-04-21 — ExecPlan: Editorial archetype taxonomy v1 — done (PR #4 merged) — agent`
- `2026-04-21 — ExecPlan: Gold set index (v1 contract) — done (PR #5 merged) — agent`
- `2026-04-21 — ExecPlan: piece_brief v1 + brief stage wiring — done (PR #6 merged) — agent`
- `2026-04-21 — ExecPlan: Framing + retrieval artifacts (v1 schemas) — done (PR #7 merged) — agent`
- `2026-04-21 — ExecPlan: Stage + artifact writer pytest coverage — done (PR #8 merged) — agent`
- `2026-04-21 — ExecPlan: critique_result v1 + critique stage wiring — done (PR #9) — agent`
- `2026-04-21 — ExecPlan: revision_result v1 + revision stage wiring — done (PR #11 merged) — agent`
- `2026-04-21 — ExecPlan: evaluation_result v1 + evaluation stage wiring — done (PR #12 merged) — agent`
- `2026-04-21 — ExecPlan: draft_result v1 + drafting stage wiring — done (PR #13 merged) — agent`
- `2026-04-21 — ExecPlan: final_deliverable v1 + final stage wiring — done (PR #14 merged) — agent`
- `2026-04-21 — ExecPlan: Intake stage v1 schemas (inputs, source_reading, topic_selection) — done (PR #15 merged) — agent`
- `2026-04-21 — ExecPlan: Stage schema registry + LLM client module — done (PR #16 merged) — agent`
- `2026-04-21 — ExecPlan: Phase 0 auto-topic skeleton (stub) — done (PR #17 merged) — agent`
- `2026-04-21 — ExecPlan: Assigned-topic skeleton run (mocked LLM) — done (PR #1 merged) — agent`
- `2026-04-24 — ExecPlan: Phase 0 skeleton LLM client probe — in_progress (PR #18) — agent`

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

Status: `done`

### Purpose / big picture

Deliver SPEC §21 step 5 and §8 “represented explicitly in code”: a versioned, schema-validated taxonomy with stable ids, library access, optional hooks on `piece_label`, and a small CLI for operators—without blocking corpus stubs or Phase 0 runs.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR #4 merged)

### Surprises & discoveries

- Observation: `piece_label` uses an inline enum under `$defs` so tests can assert it stays aligned with bundled taxonomy JSON without fragile cross-file `$ref` resolution — Evidence: `tests/unit/test_editorial_archetype_taxonomy.py::test_taxonomy_ids_match_piece_label_enum`

### Decision log

- Decision: Keep `labels.editorial` permissive (`additionalProperties: true`) but declare optional `primary_archetype_id` / `alternate_archetype_ids` with an inline enum matching bundled v1 ids — Rationale: validates known keys when present without breaking empty stub labels — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #4 (`https://github.com/john-e-moore/tlg-writer/pull/4`).

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

---

## ExecPlan: Gold set index (v1 contract) — 2026-04-21

Links: branch `feature/gold-set-index`; brief `.agent/features/2026-04-21-gold-set-index/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/5`.

Status: `done`

### Purpose / big picture

Deliver SPEC §21 step 6 as a **mergeable first slice**: a versioned JSON index contract for the manually curated gold set (§9.5), stable joins on `piece_relative_to_repo`, explicit roles, optional archetype ids checked against the bundled taxonomy, plus a validator CLI—without requiring full corpus curation in the same PR.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR #5 merged)

### Surprises & discoveries

- Observation: (none)

### Decision log

- Decision: Keep gold set as a **document** under operator control (path passed to CLI) rather than a fixed repo path under `data/` — Rationale: `data/processed/` trees are partly gitignored for generated outputs; an index file may live beside tooling or in a future committed subset — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #5 (`https://github.com/john-e-moore/tlg-writer/pull/5`).

### Context and orientation

Touch points: `schemas/json/gold_set_index.schema.json`, `src/tlg_writer/gold_set.py`, `scripts/validate_gold_set_index.py`, `tests/fixtures/corpus/gold_set_index_minimal.json`, `tests/unit/test_gold_set_index.py`, `.agent/SPEC.md` §9.5 / §21, bundled taxonomy in `src/tlg_writer/editorial_archetype_taxonomy.v1.json`.

### Plan of work

1. Add `gold_set_index` JSON Schema (roles enum, entries array).
2. Implement semantic validation (duplicate paths, archetype membership).
3. CLI + fixture + unit tests.
4. README / SPEC / PLANS / feature brief updates.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/validate_gold_set_index.py --help
python scripts/validate_gold_set_index.py
python scripts/extract_docx_metadata.py --help
```

### Validation and acceptance

- `pytest -q` passes (fixture load, duplicate path error, unknown archetype, bad role).
- Smoke: `validate_gold_set_index.py` with no args validates `tests/fixtures/corpus/gold_set_index_minimal.json`.
- `extract_docx_metadata.py --help` unchanged (repo health check from PR template).

### Idempotence and recovery

Validator is read-only. Operators edit JSON and re-run the script.

### Artifacts and notes

- No new `artifacts/runs/` paths in this slice (N/A).
- Canonical schema: `schemas/json/gold_set_index.schema.json`.

### Interfaces and dependencies

- **Library:** `tlg_writer.gold_set.load_gold_set_index`, `validate_gold_set_index_document`, `validate_gold_set_index_semantics`.
- **CLI:** `scripts/validate_gold_set_index.py` (`path`, `--no-semantics`).
- **External:** none.

---

## ExecPlan: piece_brief v1 + brief stage wiring — 2026-04-21

Links: branch `feature/piece-brief-schema`; brief `.agent/features/2026-04-21-piece-brief-schema/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/6`.

Status: `done`

### Purpose / big picture

Deliver SPEC §21 step 7 **first increment**: a versioned **`piece_brief`** JSON Schema (SPEC §7.6 / §13) and make the assigned-topic skeleton emit schema-valid `brief/output.json` while keeping other stages on the generic skeleton envelope until their schemas exist. Operators and tests can rely on a real brief contract without live LLMs.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR #6 evidence)

### Surprises & discoveries

- Observation: Framing stub used a non-taxonomy archetype string (`data-dissection`); aligned stub payload to taxonomy id `data_dissection` so optional `primary_archetype_id` on `piece_brief` validates.  
  Evidence: `src/tlg_writer/skeleton_pipeline.py` framing `payload`.
- Observation: `pytest -q` 33 passed; smoke skeleton run to `/tmp` then `validate(..., "piece_brief")` on `brief/output.json`.  
  Evidence: PR #6 checks.

### Decision log

- Decision: `brief/output.json` root **is** the `piece_brief` document (not `skeleton_stage_output`) — Rationale: matches `.agent/AGENTS.md` “schema-validated model output” per stage; other stages stay stub-wrapped — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #6 (`https://github.com/john-e-moore/tlg-writer/pull/6`).

### Context and orientation

Touch points: `schemas/json/piece_brief.schema.json`, `src/tlg_writer/piece_brief.py`, `src/tlg_writer/skeleton_pipeline.py`, `tests/unit/test_piece_brief_schema.py`, `tests/integration/test_skeleton_pipeline.py`, `tests/fixtures/pipeline/piece_brief_minimal.json`, `prompts/brief/system.md`, `.agent/SPEC.md` §13 / §21.

### Plan of work

1. Add `piece_brief` schema with taxonomy-aligned optional `primary_archetype_id`.
2. Builder for deterministic stub briefs; skeleton validates `brief/` with `piece_brief` and threads thesis into drafting.
3. Tests + README + SPEC + feature brief + this ExecPlan.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_assigned_skeleton.py --help
python scripts/extract_docx_metadata.py --help
```

### Validation and acceptance

- `pytest -q` passes (schema-only tests, enum alignment with `piece_label`, integration asserts `brief/output.json` validates as `piece_brief`).
- Smoke: `run_assigned_skeleton.py --help` unchanged.
- Spot-read: new run’s `brief/output.json` includes `schema_version` `v1`, `run_id`, `thesis`.

### Idempotence and recovery

Same as Phase 0 runner: new `run_id` each invocation; duplicate dir raises `FileExistsError`.

### Artifacts and notes

- Editorial runs: `artifacts/runs/<run_id>/brief/output.json` is now a `piece_brief` document (still stub content).
- Fixture: `tests/fixtures/pipeline/piece_brief_minimal.json`.

### Interfaces and dependencies

- **Library:** `tlg_writer.piece_brief.build_stub_piece_brief_assigned`.
- **Pipeline:** `tlg_writer.skeleton_pipeline.run_assigned_skeleton` (`output_schema` parameter on internal stage writer).
- **External:** none.

---

## ExecPlan: Framing + retrieval artifacts (v1 schemas) — 2026-04-21

Links: branch `feature/framing-retrieval-schemas`; brief `.agent/features/2026-04-21-framing-retrieval-schemas/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/7`.

Status: `done`

### Purpose / big picture

Ship SPEC §13 `framing_decision` and `retrieval_result` contracts plus assigned skeleton stages that emit schema-valid `framing/output.json` and `retrieval/output.json`, keeping Phase 0 stub behavior (no archive, no LLM) while tightening observability ahead of real framing and retrieval work.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR #7 evidence)

### Surprises & discoveries

- Observation: Full `pytest -q` is **42** tests after this slice; spot-read temp run validated `framing_decision` / `retrieval_result` on disk.  
  Evidence: PR #7 checks; local `pytest -q` + ad hoc `validate_file` on `/tmp` skeleton run.

### Decision log

- Decision: `brief/input.json` references `framing_decision` and `retrieval_result` keys holding the full v1 documents (replacing inner `payload` blobs from the old skeleton envelope) — Rationale: downstream stages should consume canonical artifacts — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #7 (`https://github.com/john-e-moore/tlg-writer/pull/7`).

### Context and orientation

Touch points: `schemas/json/framing_decision.schema.json`, `schemas/json/retrieval_result.schema.json`, `src/tlg_writer/framing_decision.py`, `src/tlg_writer/retrieval_result.py`, `src/tlg_writer/skeleton_pipeline.py`, `tests/unit/test_framing_retrieval_schemas.py`, `tests/integration/test_skeleton_pipeline.py`, `tests/fixtures/pipeline/`, `.agent/SPEC.md` §13 / §21.

### Plan of work

1. Add v1 JSON Schemas mirroring SPEC §7.4 / §7.5 / §14.3.
2. Deterministic stub builders + skeleton wiring + `ranked_piece_references` helper for the brief stage.
3. Fixtures, pytest, README and SPEC pointers; feature brief; this ExecPlan.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_assigned_skeleton.py --help
python scripts/extract_docx_metadata.py --help
```

### Validation and acceptance

- `pytest -q` passes (schema unit tests, integration asserts `framing/output.json` and `retrieval/output.json` validate).
- Smoke: CLI `--help` for skeleton and metadata scripts.
- Spot-read: new run’s `framing/output.json` has `schema_version` `v1`, `run_id`, `primary_archetype_id`; `retrieval/output.json` has empty `ranked_hits` with honest `rationale`.

### Idempotence and recovery

Same as Phase 0 runner: new `run_id` each invocation; duplicate dir raises `FileExistsError`.

### Artifacts and notes

- Editorial runs: `artifacts/runs/<run_id>/framing/output.json` is a `framing_decision` document; `retrieval/output.json` is a `retrieval_result` document (stub content).
- Fixtures: `tests/fixtures/pipeline/framing_decision_minimal.json`, `tests/fixtures/pipeline/retrieval_result_minimal.json`.

### Interfaces and dependencies

- **Library:** `tlg_writer.framing_decision.build_stub_framing_decision_assigned`, `tlg_writer.retrieval_result.build_stub_retrieval_result_assigned`, `tlg_writer.retrieval_result.ranked_piece_references`.
- **Pipeline:** `tlg_writer.skeleton_pipeline.run_assigned_skeleton`.
- **External:** none.

---

## ExecPlan: Stage + artifact writer pytest coverage — 2026-04-21

Links: branch `feature/stage-pytest-coverage`; brief `.agent/features/2026-04-21-stage-pytest-coverage/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/8`.

Status: `done`

### Purpose / big picture

Deliver `.agent/SPEC.md` §21 step 8 as an operator-safe **test-only** slice: every Phase 0 skeleton stage’s `output.json` and `metrics.json` is asserted against the correct JSON Schema in integration tests; corpus stub gets deterministic stem coverage and an empty-batch path so artifact writers stay regression-locked without changing runtime behavior.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs

### Surprises & discoveries

- Observation: Full `pytest -q` is **46** tests after this slice (was 42 after framing/retrieval).  
  Evidence: `pytest -q` on branch `feature/stage-pytest-coverage`.

### Decision log

- Decision: Keep schema-per-stage mapping in tests (not a new production registry) — Rationale: avoids duplicating contract source of truth in `src/` until a shared helper is needed — Date: 2026-04-21

### Outcomes & retrospective

Shipped test-only coverage for SPEC §21 step 8: per-stage schema validation on assigned skeleton runs; corpus `piece_artifact_stem` unit tests; empty-batch manifest path; `run.log` smoke. Merged via PR #8 (`https://github.com/john-e-moore/tlg-writer/pull/8`).

### Context and orientation

Touch points: `tests/integration/test_skeleton_pipeline.py`, `tests/integration/test_corpus_batch_stub.py`, `tests/unit/test_corpus_batch_artifacts.py` (new), `src/tlg_writer/skeleton_pipeline.py`, `src/tlg_writer/corpus_batch_stub.py`, `schemas/json/`, `.agent/SPEC.md` §21.

### Plan of work

1. Add per-stage `validate_file` loop for assigned skeleton runs (domain vs `skeleton_stage_output`).
2. Assert manifest `stages_executed` matches `STAGE_DIRS` and `config.json` shape.
3. Corpus: `piece_artifact_stem` unit tests; empty batch integration test; run log assertions.
4. SPEC §21 step 8 shipped note; finalize this ExecPlan + optional index.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_assigned_skeleton.py --help
python scripts/extract_docx_metadata.py --help
```

### Validation and acceptance

- `pytest -q` passes with new tests (note total count in PR).
- Smoke: `--help` for skeleton and metadata CLIs unchanged.

### Idempotence and recovery

Tests only; no artifact contract changes.

### Artifacts and notes

- N/A for new `artifacts/runs/` paths (tests use `tmp_path`).

### Interfaces and dependencies

- **External:** none.

---

## ExecPlan: critique_result v1 + critique stage wiring — 2026-04-21

Links: branch `feature/critique-result-v1`; brief `.agent/features/2026-04-21-critique-result-v1/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/9`.

Status: `done`

### Purpose / big picture

Ship SPEC §21 step 9: a versioned **`critique_result`** JSON Schema (SPEC §7.8 / §15.1) and make the assigned-topic skeleton emit schema-valid `critique/output.json` while keeping drafting on the generic skeleton envelope. Operators and tests gain a real critique contract without live models.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (pre-PR evidence)

### Surprises & discoveries

- Observation: Full `pytest -q` is **50** tests on this branch (was 46 on `main`).  
  Evidence: `pytest -q` on `feature/critique-result-v1`.
- Observation: Smoke run under `/tmp/tlg-critique-smoke/…/critique/output.json` validates as `critique_result`.  
  Evidence: `validate_file` one-liner after `run_assigned_skeleton.py`.

### Decision log

- Decision: Encode §15.1 rubric as a fixed-key object with `null` or `0..1` scores — Rationale: explicit dimensions without optional-key drift; `null` marks Phase 0 “not evaluated” — Date: 2026-04-21

### Outcomes & retrospective

Opened PR #9 (`https://github.com/john-e-moore/tlg-writer/pull/9`): `critique_result` v1 schema, stub builder, skeleton wiring, 50 `pytest` tests, smoke validation on `/tmp` skeleton run.

### Context and orientation

Touch points: `schemas/json/critique_result.schema.json`, `src/tlg_writer/critique_result.py`, `src/tlg_writer/skeleton_pipeline.py`, `tests/unit/test_critique_result_schema.py`, `tests/integration/test_skeleton_pipeline.py`, `tests/fixtures/pipeline/critique_result_minimal.json`, `prompts/critique/system.md`, `.agent/SPEC.md` §13 / §21.

### Plan of work

1. Add `critique_result` schema + deterministic stub builder + unit tests and fixture.
2. Wire skeleton critique stage + `revision/input.json` to reference the canonical document.
3. Update README, SPEC §21 step 9, feature brief, PLANS index, and this ExecPlan with validation evidence.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_assigned_skeleton.py --topic "smoke" --slug critique-smoke
```

### Validation and acceptance

- `pytest -q` passes (schema unit tests; integration maps `critique` to `critique_result`).
- Smoke: skeleton CLI creates a run whose `critique/output.json` validates as `critique_result` (spot-check under `artifacts/runs/` or `/tmp` redirect if used).
- `--help` for `run_assigned_skeleton.py` and `extract_docx_metadata.py` unchanged.

### Idempotence and recovery

Same as Phase 0 runner: new `run_id` each invocation; duplicate dir raises `FileExistsError`.

### Artifacts and notes

- Editorial runs: `artifacts/runs/<run_id>/critique/output.json` is a `critique_result` document (stub content).
- Fixture: `tests/fixtures/pipeline/critique_result_minimal.json`.

### Interfaces and dependencies

- **Library:** `tlg_writer.critique_result.build_stub_critique_result_assigned`.
- **Pipeline:** `tlg_writer.skeleton_pipeline.run_assigned_skeleton`.
- **External:** none.

---

## ExecPlan: revision_result v1 + revision stage wiring — 2026-04-21

Links: branch `feature/revision-result-v1`; brief `.agent/features/2026-04-21-revision-result-v1/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/11`.

Status: `done`

### Purpose / big picture

Ship SPEC §21 step 10: a versioned **`revision_result`** JSON Schema (SPEC §7.9) and make the assigned-topic skeleton emit schema-valid `revision/output.json` while keeping drafting on the generic skeleton envelope (evaluation/final were still generic stubs at this milestone). No live models.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR #11 evidence)

### Surprises & discoveries

- Observation: Full `pytest -q` is **54** tests after this slice (was 50 on prior `main`).  
  Evidence: `pytest -q` on `feature/revision-result-v1`.
- Observation: Smoke `validate_file` on `/tmp/…/revision/output.json` after skeleton run.  
  Evidence: local one-liner post-`run_assigned_skeleton`.

### Decision log

- Decision: `evaluation/input.json` holds `revision_result` as the full v1 document (replacing the prior inner `revision` payload blob) — Rationale: aligns with downstream consuming canonical artifacts — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #11 (`https://github.com/john-e-moore/tlg-writer/pull/11`). Validation: `pytest -q` (54 passed) on branch before merge; smoke `revision_result` validation on temp run dir.

### Context and orientation

Touch points: `schemas/json/revision_result.schema.json`, `src/tlg_writer/revision_result.py`, `src/tlg_writer/skeleton_pipeline.py`, `tests/unit/test_revision_result_schema.py`, `tests/integration/test_skeleton_pipeline.py`, `tests/fixtures/pipeline/revision_result_minimal.json`, `prompts/revision/system.md`, `.agent/SPEC.md` §13 / §21.

### Plan of work

1. Add `revision_result` schema + deterministic stub builder + unit tests and fixture.
2. Wire skeleton revision stage; thread `revised_markdown` into `final/piece.md`; point evaluation input at the canonical document.
3. Update README, SPEC §21 step 10 + §13 list, feature brief, PLANS index, and this ExecPlan with validation evidence.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_assigned_skeleton.py --topic "smoke" --slug revision-smoke
```

### Validation and acceptance

- `pytest -q` passes (schema unit tests; integration maps `revision` to `revision_result`).
- Smoke: skeleton CLI run; `revision/output.json` validates as `revision_result`.
- `--help` for `run_assigned_skeleton.py` and `extract_docx_metadata.py` unchanged.

### Idempotence and recovery

Same as Phase 0 runner: new `run_id` each invocation; duplicate dir raises `FileExistsError`.

### Artifacts and notes

- Editorial runs: `artifacts/runs/<run_id>/revision/output.json` is a `revision_result` document (stub content).
- Fixture: `tests/fixtures/pipeline/revision_result_minimal.json`.

### Interfaces and dependencies

- **Library:** `tlg_writer.revision_result.build_stub_revision_result_assigned`.
- **Pipeline:** `tlg_writer.skeleton_pipeline.run_assigned_skeleton`.
- **External:** none.

---

## ExecPlan: evaluation_result v1 + evaluation stage wiring — 2026-04-21

Links: branch `feature/evaluation-result-v1`; brief `.agent/features/2026-04-21-evaluation-result-v1/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/12`.

Status: `done`

### Purpose / big picture

Ship SPEC §21 step 11: a versioned **`evaluation_result`** JSON Schema (SPEC §7.10 / §15.1 scorecard shape, §15.3 explicit operator summary) and make the assigned-topic skeleton emit schema-valid `evaluation/output.json` (null scorecard = not evaluated in Phase 0). No live models.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR #12 evidence)

### Surprises & discoveries

- Observation: Full `pytest -q` is **58** tests after this slice (was 54 on prior `main`).  
  Evidence: `pytest -q` on `feature/evaluation-result-v1`.
- Observation: Smoke `validate_file` on `/tmp/…/evaluation/output.json` after skeleton run.  
  Evidence: local one-liner post-`run_assigned_skeleton`.

### Decision log

- Decision: `final/input.json` holds `evaluation_result` as the full v1 document (replacing the prior `evaluation` payload blob) — Rationale: canonical downstream artifact for packaging — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #12 (`https://github.com/john-e-moore/tlg-writer/pull/12`). Validation: `pytest -q` (58 passed) on branch before merge; smoke `evaluation_result` validation on temp run dir.

### Context and orientation

Touch points: `schemas/json/evaluation_result.schema.json`, `src/tlg_writer/evaluation_result.py`, `src/tlg_writer/skeleton_pipeline.py`, `tests/unit/test_evaluation_result_schema.py`, `tests/integration/test_skeleton_pipeline.py`, `tests/fixtures/pipeline/evaluation_result_minimal.json`, `prompts/evaluation/system.md`, `.agent/SPEC.md` §13 / §21.

### Plan of work

1. Add `evaluation_result` schema + deterministic stub builder + unit tests and fixture.
2. Wire skeleton evaluation stage; point `final/input.json` at the canonical document.
3. Update README, SPEC §21 step 11 + §13 list, feature brief, PLANS index, and this ExecPlan with validation evidence.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_assigned_skeleton.py --topic "smoke" --slug eval-smoke
```

### Validation and acceptance

- `pytest -q` passes (schema unit tests; integration maps `evaluation` to `evaluation_result`).
- Smoke: skeleton CLI run; `evaluation/output.json` validates as `evaluation_result`.
- `--help` for `run_assigned_skeleton.py` and `extract_docx_metadata.py` unchanged.

### Idempotence and recovery

Same as Phase 0 runner: new `run_id` each invocation; duplicate dir raises `FileExistsError`.

### Artifacts and notes

- Editorial runs: `artifacts/runs/<run_id>/evaluation/output.json` is an `evaluation_result` document (stub content).
- Fixture: `tests/fixtures/pipeline/evaluation_result_minimal.json`.

### Interfaces and dependencies

- **Library:** `tlg_writer.evaluation_result.build_stub_evaluation_result_assigned`.
- **Pipeline:** `tlg_writer.skeleton_pipeline.run_assigned_skeleton`.
- **External:** none.

---

## ExecPlan: draft_result v1 + drafting stage wiring — 2026-04-21

Links: branch `feature/draft-result-v1`; brief `.agent/features/2026-04-21-draft-result-v1/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/13`.

Status: `done`

### Purpose / big picture

Ship SPEC §21 step 12: a versioned **`draft_result`** JSON Schema (SPEC §7.7) and make the assigned-topic skeleton emit schema-valid `drafting/output.json` while keeping inputs, source_reading, and topic_selection on Phase 0 generic stubs (`final/` gained `final_deliverable` in a later PR). Critique and revision consume the canonical draft document. No live models.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR #13 evidence)

### Surprises & discoveries

- Observation: Full `pytest -q` is **62** tests after this slice (was 58 on prior `main`).  
  Evidence: `pytest -q` on `feature/draft-result-v1`.
- Observation: Smoke `validate_file` on `/tmp/…/drafting/output.json` after skeleton run.  
  Evidence: local one-liner post-`run_assigned_skeleton`.

### Decision log

- Decision: `critique/input.json` and `revision/input.json` use `draft_result` as the full v1 document (replacing the prior inner `draft` payload blob) — Rationale: consistent canonical artifacts — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #13 (`https://github.com/john-e-moore/tlg-writer/pull/13`). Validation: `pytest -q` (62 passed) on branch before merge; smoke `draft_result` validation on temp run dir.

### Context and orientation

Touch points: `schemas/json/draft_result.schema.json`, `src/tlg_writer/draft_result.py`, `src/tlg_writer/skeleton_pipeline.py`, `tests/unit/test_draft_result_schema.py`, `tests/integration/test_skeleton_pipeline.py`, `tests/fixtures/pipeline/draft_result_minimal.json`, `prompts/drafting/system.md`, `.agent/SPEC.md` §13 / §21.

### Plan of work

1. Add `draft_result` schema + deterministic stub builder + unit tests and fixture.
2. Wire skeleton drafting stage; thread `body_markdown` into revision stub; point critique/revision inputs at the canonical document.
3. Update README, SPEC §21 step 12 + §13 list, feature brief, PLANS index, and this ExecPlan with validation evidence.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_assigned_skeleton.py --topic "smoke" --slug draft-smoke
```

### Validation and acceptance

- `pytest -q` passes (schema unit tests; integration maps `drafting` to `draft_result`).
- Smoke: skeleton CLI run; `drafting/output.json` validates as `draft_result`.
- `--help` for `run_assigned_skeleton.py` and `extract_docx_metadata.py` unchanged.

### Idempotence and recovery

Same as Phase 0 runner: new `run_id` each invocation; duplicate dir raises `FileExistsError`.

### Artifacts and notes

- Editorial runs: `artifacts/runs/<run_id>/drafting/output.json` is a `draft_result` document (stub content).
- Fixture: `tests/fixtures/pipeline/draft_result_minimal.json`.

### Interfaces and dependencies

- **Library:** `tlg_writer.draft_result.build_stub_draft_result_assigned`.
- **Pipeline:** `tlg_writer.skeleton_pipeline.run_assigned_skeleton`.
- **External:** none.

---

## ExecPlan: final_deliverable v1 + final stage wiring — 2026-04-21

Links: branch `feature/final-deliverable-v1`; brief `.agent/features/2026-04-21-final-deliverable-v1/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/14`.

Status: `done`

### Purpose / big picture

Ship SPEC §21 step 13: a versioned **`final_deliverable`** JSON Schema and make the assigned-topic skeleton emit schema-valid `final/output.json` with `body_markdown` aligned to `final/piece.md`, while intake stages remain generic stubs. No live models.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR #14 evidence)

### Surprises & discoveries

- Observation: Full `pytest -q` is **66** tests after this slice (was 62 on prior `main`).  
  Evidence: `pytest -q` on `feature/final-deliverable-v1`.
- Observation: Integration asserts `final/output.json` `body_markdown` equals `final/piece.md` bytes.  
  Evidence: `tests/integration/test_skeleton_pipeline.py`.

### Decision log

- Decision: Keep `format` as `const` `markdown` for v1 — Rationale: matches current `piece.md` contract; extend schema when other formats ship — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #14 (`https://github.com/john-e-moore/tlg-writer/pull/14`). Validation: `pytest -q` (66 passed) on branch before merge; smoke `final_deliverable` validation on temp run dir.

### Context and orientation

Touch points: `schemas/json/final_deliverable.schema.json`, `src/tlg_writer/final_deliverable.py`, `src/tlg_writer/skeleton_pipeline.py`, `tests/unit/test_final_deliverable_schema.py`, `tests/integration/test_skeleton_pipeline.py`, `tests/fixtures/pipeline/final_deliverable_minimal.json`, `prompts/final/`, `.agent/SPEC.md` §13 / §21.

### Plan of work

1. Add `final_deliverable` schema + deterministic stub builder + unit tests and fixture.
2. Wire skeleton final stage; add `prompts/final/` placeholders.
3. Update README, SPEC §21 step 13 + §13 list, feature brief, PLANS index, and this ExecPlan with validation evidence.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_assigned_skeleton.py --topic "smoke" --slug final-smoke
```

### Validation and acceptance

- `pytest -q` passes (schema unit tests; integration maps `final` to `final_deliverable`).
- Smoke: skeleton CLI run; `final/output.json` validates as `final_deliverable`.
- `--help` for `run_assigned_skeleton.py` and `extract_docx_metadata.py` unchanged.

### Idempotence and recovery

Same as Phase 0 runner: new `run_id` each invocation; duplicate dir raises `FileExistsError`.

### Artifacts and notes

- Editorial runs: `artifacts/runs/<run_id>/final/output.json` is a `final_deliverable` document; `final/piece.md` mirrors `body_markdown`.
- Fixture: `tests/fixtures/pipeline/final_deliverable_minimal.json`.

### Interfaces and dependencies

- **Library:** `tlg_writer.final_deliverable.build_stub_final_deliverable_assigned`.
- **Pipeline:** `tlg_writer.skeleton_pipeline.run_assigned_skeleton`.
- **External:** none.

---

## ExecPlan: Intake stage v1 schemas (inputs, source_reading, topic_selection) — 2026-04-21

Links: branch `feature/intake-results-v1`; brief `.agent/features/2026-04-21-intake-results-v1/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/15`.

Status: `done`

### Purpose / big picture

Ship SPEC §21 step 14: **`inputs_result`**, **`source_reading_result`**, and **`topic_selection_result`** v1 JSON Schemas so assigned skeleton runs have schema-valid intake `output.json` files and framing consumes canonical intake artifacts. No live models.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR #15 evidence)

### Surprises & discoveries

- Observation: Full `pytest -q` is **71** tests after this slice (was 66 on prior `main`).  
  Evidence: `pytest -q` on `feature/intake-results-v1`.
- Observation: Smoke validation of all three intake `output.json` on a temp skeleton run.  
  Evidence: local one-liner post-`run_assigned_skeleton`.

### Decision log

- Decision: `topic_selection_result` v1 encodes **assigned skip only** (`selection_status` const `skipped`) — Rationale: auto-topic completed shape ships with auto runner — Date: 2026-04-21
- Decision: `framing/input.json` carries `source_reading_result` and `topic_selection_result` full documents — Rationale: consistent with other stages — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #15 (`https://github.com/john-e-moore/tlg-writer/pull/15`). Validation: `pytest -q` (71 passed) on branch before merge; smoke intake validation on temp run dir.

### Context and orientation

Touch points: `schemas/json/inputs_result.schema.json`, `schemas/json/source_reading_result.schema.json`, `schemas/json/topic_selection_result.schema.json`, `src/tlg_writer/inputs_result.py`, `src/tlg_writer/source_reading_result.py`, `src/tlg_writer/topic_selection_result.py`, `src/tlg_writer/skeleton_pipeline.py`, `tests/unit/test_intake_results_schema.py`, `tests/integration/test_skeleton_pipeline.py`, `tests/fixtures/pipeline/`, `prompts/inputs/`, `prompts/source_reading/system.md`, `prompts/topic_selection/system.md`, `.agent/SPEC.md` §13 / §21.

### Plan of work

1. Add three v1 schemas + stub builders + fixtures + unit tests.
2. Wire skeleton intake stages; update framing intake `input.json`; add `prompts/inputs/`.
3. Update README, SPEC §21 step 14 + §13 list, feature brief, PLANS index, and this ExecPlan with validation evidence.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_assigned_skeleton.py --topic "smoke" --slug intake-smoke
```

### Validation and acceptance

- `pytest -q` passes (intake unit tests; integration maps all stages to named schemas).
- Smoke: skeleton run; `inputs`, `source_reading`, `topic_selection` `output.json` validate.
- `--help` for `run_assigned_skeleton.py` and `extract_docx_metadata.py` unchanged.

### Idempotence and recovery

Same as Phase 0 runner: new `run_id` each invocation; duplicate dir raises `FileExistsError`.

### Artifacts and notes

- Editorial runs: `inputs/output.json`, `source_reading/output.json`, `topic_selection/output.json` are v1 intake documents (stub content).
- Fixtures: `tests/fixtures/pipeline/inputs_result_minimal.json`, `source_reading_result_minimal.json`, `topic_selection_result_minimal.json`.

### Interfaces and dependencies

- **Library:** `build_stub_inputs_result_assigned`, `build_stub_source_reading_result_assigned`, `build_stub_topic_selection_result_assigned_skipped`.
- **Pipeline:** `tlg_writer.skeleton_pipeline.run_assigned_skeleton`.
- **External:** none.

---

## ExecPlan: Stage schema registry + LLM client module — 2026-04-21

Links: branch `feature/schema-registry-llm-client`; brief `.agent/features/2026-04-21-schema-registry-llm-client/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/16`.

Status: `done`

### Purpose / big picture

Centralize pipeline **stage → output JSON Schema** mapping in `tlg_writer.stage_schemas` and introduce a small **LLM HTTP boundary** in `tlg_writer.llm_client` (stub default; optional OpenAI Chat Completions via stdlib when env is set). No change to emitted artifact shapes beyond using the registry for validation.

### Progress

- [x] (2026-04-21) Planning
- [x] (2026-04-21) Implementation
- [x] (2026-04-21) Validation + docs (PR #16 evidence)

### Surprises & discoveries

- Observation: Full `pytest -q` is **79** tests after this slice (was 71 on prior `main`).  
  Evidence: `pytest -q` on `feature/schema-registry-llm-client`.

### Decision log

- Decision: OpenAI path uses **stdlib urllib** (no `openai` package) — Rationale: keeps default install lean; callers can add SDK later if needed — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #16 (`https://github.com/john-e-moore/tlg-writer/pull/16`). Validation: `pytest -q` (79 passed) on branch before merge.

### Context and orientation

Touch points: `src/tlg_writer/stage_schemas.py`, `src/tlg_writer/llm_client.py`, `src/tlg_writer/skeleton_pipeline.py`, `tests/integration/test_skeleton_pipeline.py`, `tests/unit/test_stage_schemas.py`, `tests/unit/test_llm_client.py`, `README.md`, `.agent/SPEC.md` §13 / §21.

### Plan of work

1. Add `stage_schemas` registry + `validate_pipeline_stage_output`; refactor skeleton and integration tests to consume it.
2. Add `llm_client` module (Protocol, stub, OpenAI urllib implementation, `llm_client_from_env`) + unit tests (mocked HTTP).
3. Update README, SPEC §21 step 15 + §13 note, feature brief, PLANS index, and this ExecPlan with validation evidence.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

### Validation and acceptance

- `pytest -q` passes (registry alignment with `STAGE_DIRS`; LLM stub + mocked OpenAI).
- Skeleton behavior unchanged aside from registry imports.

### Idempotence and recovery

N/A (library-only refactor plus new modules).

### Artifacts and notes

- N/A for new `artifacts/runs/` paths.

### Interfaces and dependencies

- **Library:** `tlg_writer.stage_schemas`, `tlg_writer.llm_client`.
- **External:** optional `OPENAI_API_KEY` when `TLG_LLM_BACKEND=openai` (not used in CI).

## ExecPlan: Phase 0 auto-topic skeleton (stub) — 2026-04-21

Links: branch `feature/auto-skeleton-phase0`; brief `N/A`; PR `https://github.com/john-e-moore/tlg-writer/pull/17`.

Status: `done`

### Purpose / big picture

Ship SPEC §21 step 16: a second Phase 0 runner for **`auto`** mode that reuses the full stage directory layout, writes schema-valid **`inputs_result`** (auto stub) and **`topic_selection_result`** (**completed** stub, empty candidates), and exposes `scripts/run_auto_skeleton.py` — no live topic search and no LLM calls.

### Progress

- [x] (2026-04-21) Schemas + builders + `run_auto_skeleton` / shared `_execute_phase0_run`
- [x] (2026-04-21) CLI `scripts/run_auto_skeleton.py`
- [x] (2026-04-21) Unit + integration tests; README / SPEC / prompts
- [x] (2026-04-21) PR #17 opened (`gh pr create`)
- [x] (2026-04-21) CI green + squash merge to `main` (PR #17)

### Surprises & discoveries

- Observation: `test_inputs_result_rejects_bad_mode` previously flipped `mode` to `"auto"` on an assigned-shaped doc; that is now schema-valid, so the test asserts an invalid enum instead.  
  Evidence: `pytest -q` (83 passed) after the change.
- Observation: `gh pr merge --auto` failed with “Auto merge is not allowed for this repository”; merged with `gh pr merge 17 --squash` after **Tests** passed.  
  Evidence: `gh pr checks 17 --watch` then successful squash merge.

### Decision log

- Decision: `topic_selection_result` uses JSON Schema **`oneOf`** for skipped vs completed branches — Rationale: one artifact type, two explicit shapes — Date: 2026-04-21

### Outcomes & retrospective

Merged via PR #17 (`https://github.com/john-e-moore/tlg-writer/pull/17`). GitHub Actions **Tests** job passed on the PR branch. Repository auto-merge was unavailable; merge completed with `gh pr merge 17 --squash`. Follow-up: real auto-topic search and non-stub `topic_selection` when Phase 4 work begins.

### Context and orientation

Touch points: `schemas/json/inputs_result.schema.json`, `schemas/json/topic_selection_result.schema.json`, `src/tlg_writer/inputs_result.py`, `src/tlg_writer/topic_selection_result.py`, `src/tlg_writer/skeleton_pipeline.py`, `scripts/run_auto_skeleton.py`, `tests/integration/test_skeleton_pipeline.py`, `tests/unit/test_intake_results_schema.py`, `tests/fixtures/pipeline/topic_selection_result_completed_minimal.json`, `README.md`, `.agent/SPEC.md` §13 / §18 / §21, `prompts/topic_selection/system.md`.

### Plan of work

1. Extend contracts and builders for auto stub intake and completed topic_selection.
2. Refactor skeleton execution so assigned and auto share one writer path.
3. CLI + tests + docs; open PR.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_auto_skeleton.py --help
python scripts/run_auto_skeleton.py --slug smoke-auto
```

### Validation and acceptance

- `pytest -q` passes.
- `run_auto_skeleton` produces `manifest.mode == "auto"`, `run_id` contains `__auto__`, and `topic_selection/output.json` validates as `topic_selection_result` (completed branch).

### Idempotence and recovery

Same as assigned skeleton: duplicate `run_id` directory raises `FileExistsError`.

### Artifacts and notes

New runs under `artifacts/runs/<run_id>/` when using default `--artifacts-root`.

### Interfaces and dependencies

- **Library:** `tlg_writer.skeleton_pipeline.run_auto_skeleton`
- **CLI:** `scripts/run_auto_skeleton.py`

---

## ExecPlan: Phase 0 skeleton LLM client probe — 2026-04-24

Links: branch `feature/skeleton-llm-probe`; brief `.agent/features/2026-04-24-skeleton-llm-probe/SPEC.md`; PR `https://github.com/john-e-moore/tlg-writer/pull/18`.

Status: `in_progress`

### Purpose / big picture

Connect the existing `tlg_writer.llm_client` boundary to Phase 0 skeleton runs with a **single observability probe** per run so operators see LLM metadata in `config.json`, `metrics.json`, and `run.log` while all stage `output.json` files remain stub-built (no paid API by default).

### Progress

- [x] (2026-04-24) Planning
- [x] (2026-04-24) Implementation
- [ ] (2026-04-24) Validation + docs (PR evidence)

### Surprises & discoveries

- (none yet)

### Decision log

- Decision: Default `llm_client` remains `StubLLMClient()` inside runners (not `llm_client_from_env()`) — Rationale: avoids accidental live calls when operators have `OPENAI_API_KEY` set — Date: 2026-04-24

### Outcomes & retrospective

Pending merge.

### Context and orientation

Touch points: `src/tlg_writer/skeleton_pipeline.py`, `src/tlg_writer/llm_client.py`, `tests/integration/test_skeleton_pipeline.py`, `.agent/SPEC.md` §21 step 17, `README.md`.

### Plan of work

1. Probe once in `_execute_phase0_run`; thread snapshot into `_write_stage` metrics and `config.json`.
2. Extend integration tests; document in README / SPEC / PLANS.

### Concrete steps

```bash
cd /path/to/tlg-writer
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/run_assigned_skeleton.py --help
```

### Validation and acceptance

- `pytest -q` passes; integration asserts `llm_client_probe` and per-stage `metrics.json` `llm.phase0_client_probe`.
- Smoke: assigned skeleton run; `run.log` contains `llm_probe_model=phase0-probe`.

### Idempotence and recovery

Unchanged: duplicate `run_id` directory raises `FileExistsError`.

### Artifacts and notes

- `artifacts/runs/<run_id>/config.json` gains `llm_client_probe`.
- Each `*/metrics.json` gains `llm.phase0_client_probe` (schema allows via `additionalProperties` on nested objects / stage_metrics).

### Interfaces and dependencies

- **Library:** `run_assigned_skeleton`, `run_auto_skeleton` optional `llm_client: LLMClient | None`.
- **External:** none in default configuration.

