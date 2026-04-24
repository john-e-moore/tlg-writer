# Progress (human-readable)

**Purpose:** A single page to see **what is done** and **what is next** without reading every ExecPlan in `.agent/PLANS.md` or every line of `.agent/SPEC.md`.  
**Normative requirements** still live in `.agent/SPEC.md`; **agent behavior** in `.agent/AGENTS.md`.

**Last updated:** 2026-04-24 (initial file; align checkboxes with reality after each substantive merge.)

---

## Current focus (optional; edit when priorities shift)

- [ ] **Product:** Replace corpus **stub** labeling with **real** batch labeling (or HITL), validate outputs, add **summary statistics** for a run.
- [ ] **Product:** First **assigned-topic** run that uses **live** (or env-gated) model work for **new piece generation**, with operator review of `artifacts/runs/…`.

---

## Phase 0 — Runnable editorial skeleton (SPEC §18)

*Full stage tree under `artifacts/runs/<run_id>/`, schema-valid artifacts, tests default to mocks.*

### Entry points and layout

- [x] Assigned-topic CLI: `scripts/run_assigned_skeleton.py` → `run_assigned_skeleton`
- [x] Auto-topic Phase 0 stub CLI: `scripts/run_auto_skeleton.py` → `run_auto_skeleton`
- [x] Timestamped `run_id`, stage dirs per `.agent/AGENTS.md`, `manifest.json`, `config.json`, `logs/run.log`
- [x] `final/piece.md` plus `final/output.json` (`final_deliverable` v1)

### Contracts (JSON Schemas + stub builders)

- [x] `run_manifest`, `corpus_batch_manifest` (corpus tooling; distinct from editorial manifest)
- [x] Intake: `inputs_result`, `source_reading_result`, `topic_selection_result` (assigned skip + auto completed stub)
- [x] `framing_decision`, `retrieval_result`, `piece_brief`, `draft_result`, `critique_result`, `revision_result`, `evaluation_result`, `final_deliverable`
- [x] Stage → schema registry: `tlg_writer.stage_schemas`
- [x] `tlg_writer.llm_client` (stub + optional OpenAI via stdlib); skeleton records a **per-run probe** in `metrics.json` / `config.json` / `run.log` (no completion text drives stages yet)

### Quality and tests

- [x] Integration tests: layout, manifest, per-stage `output.json` + `metrics.json` validation
- [x] CI: `pytest` via `.github/workflows/ci.yml`

### Not done yet (still Phase 0 / early Phase 2 depending on how you scope it)

- [ ] Editorial stages consume **real** LLM completions (beyond probe) for any stage
- [ ] Retrieval reads **real** archive / labeled corpus (non-empty `ranked_hits` path)

---

## Phase 1 — Archive understanding and taxonomy (SPEC §18)

*Labels, features, taxonomy, gold paths, batch observability.*

### Ingestion and metadata

- [x] `.docx` metadata extraction CLI: `scripts/extract_docx_metadata.py` → validated `pieces_metadata_*.json` batches

### Schemas and library contracts

- [x] `piece_label`, `piece_features` JSON Schemas (+ metadata batch schema)
- [x] Editorial archetype taxonomy v1 (bundled JSON, `piece_label` optional archetype fields)
- [x] Gold set **index** schema + validator CLI: `scripts/validate_gold_set_index.py`

### Batch processing (corpus)

- [x] **Stub** batch run: `scripts/run_corpus_batch_stub.py` → `piece_label` / `piece_features` files + `artifacts/runs/…` with `corpus_batch_manifest`, `summary.md`, `run.log`
- [ ] **Real** labeling pipeline (model or HITL) writing schema-valid `data/processed/pieces/labeled/`
- [ ] **Real** feature extraction pipeline writing schema-valid `data/processed/pieces/extracted_features/`
- [ ] **Summary statistics** for a labeling/feature batch (counts, errors, archetype distribution, etc.) in operator-facing artifacts
- [ ] Tests for real labeling/extraction paths (with mocks for HTTP where needed)

### Gold set

- [x] Gold set index **contract** and validator (curated list file is operator-owned)
- [ ] Committed or team-agreed **gold set JSON** covering representative pieces (ongoing curation)

---

## Phase 2 — Assigned-topic pipeline depth (SPEC §18)

*Real prompts, retrieval integration, rubric-worthy outputs where applicable.*

- [x] v1 schemas and stub-filled `output.json` for all editorial stages (observability-first)
- [ ] End-to-end **assigned** run with at least one stage using **real** structured LLM output (still inspectable under `artifacts/runs/…`)
- [ ] Source reading / intake tied to **real** inputs (files, URLs, or agreed scope)
- [ ] Retrieval integrated with **processed** corpus artifacts
- [ ] Operator can **manually review** final piece against house rubric (process + artifacts documented)

---

## Phase 3 — Evaluation harness (SPEC §18)

- [ ] Rubric definitions wired to repeatable scoring
- [ ] Comparison utilities and baseline reports

---

## Phase 4 — Auto-topic pipeline (SPEC §18)

- [ ] Real topic candidates and ranking artifacts (beyond Phase 0 `topic_selection` stub)

---

## Phase 5 — Thresholded multi-agent improvement (SPEC §18)

- [ ] Richer critics, stop rules, optional multi-draft flows

---

## How agents should update this file

After **completing** a substantive task or merge (especially anything that changes operator-visible capability):

1. Tick or untick the relevant **checkboxes** above.
2. Adjust **Current focus** if the team’s next priority changed.
3. Bump **Last updated** date.
4. Keep bullets **short**; put evidence and narrative in `.agent/PLANS.md` ExecPlans and PRs, not here.

Skip updates for typos, comment-only edits, or test-only tweaks that do not change delivered behavior.

See `.agent/AGENTS.md` (**Progress tracking**).
