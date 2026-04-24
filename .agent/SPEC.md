# SPEC.md

Agent execution details and path tables: **`.agent/AGENTS.md`**. This document is the product/requirements baseline; keep the two in sync when contracts change. For **early feedback loops** (runnable, inspectable `artifacts/runs/` before exhaustive archive work), see **§18 Phase 0**, **§19**, and **§21**.

## Project
Build an editorial system that produces high-quality macroeconomic advisory **pieces** in a recognizable house style, with strong observability, reproducible runs, and clear intermediate artifacts.

The system must support two entry modes:

1. **Assigned-topic mode**: a user provides the topic, thesis, report, article, prompt, or source materials.
2. **Auto-topic mode**: the system searches available inputs, decides what is worth writing about, proposes candidate topics, chooses one, and develops a piece.

This system is not a generic writing chatbot. It is an observable, testable editorial pipeline that:
- reads source material,
- identifies what matters,
- selects an appropriate framing,
- retrieves relevant historical pieces,
- drafts in the house voice,
- critiques itself through specialized agents,
- revises with explicit standards,
- emits artifacts at every stage so a human can inspect what happened.

---

## 1. Goals

### Primary goals
- Produce client-facing pieces that sound recognizably like the firm.
- Improve not only surface style, but **editorial judgment**.
- Decide whether a topic should become a historical-analog piece, future-implications piece, data-dissection piece, or another editorial form.
- Support both system-generated topics and user-assigned topics.
- Make every run easy to inspect with high-quality artifacts.
- Keep the architecture modular enough to evolve from a simple pipeline into a more advanced multi-agent system.

### Secondary goals
- Build reusable datasets from historical pieces.
- Create labeled and extracted-feature datasets that improve retrieval, evaluation, and orchestration.
- Make failures easy to diagnose.
- Keep API usage efficient by giving each agent only the context it actually needs.

---

## 2. Non-goals
- A fully autonomous publishing system in v1.
- A generic finance-news summarizer.
- A monolithic prompt that tries to solve the whole task in one model call.
- An opaque agent loop that cannot be inspected or debugged.
- Replacing human editorial review immediately.

---

## 3. Success criteria

A generated piece is successful if it:
- sounds like the firm’s writing rather than generic AI finance prose,
- chooses a fitting editorial frame,
- uses historical analogs when appropriate,
- explores future implications when appropriate,
- remains economically coherent,
- does more than summarize headlines,
- is supported by inspectable artifacts showing why the system made its decisions.

### Initial qualitative success bar
For a controlled evaluation set, reviewers should be able to say:
- “This sounds like us.”
- “This picked the right angle.”
- “This says something interesting.”
- “This is economically defensible.”
- “This feels like a real piece we could plausibly send after editing.”

### Initial quantitative success bar
For internal evaluation rubrics, target:
- no critical factual or reasoning failures,
- no rubric dimension below a defined minimum threshold,
- strong observability coverage for every pipeline step,
- deterministic persistence of all run artifacts.

Exact thresholds can be tightened later, but the initial design should assume rubric scoring for:
- voice match,
- framing quality,
- originality,
- macro soundness,
- evidence usage,
- conversational quality,
- overall sendability.

---

## 4. Entry modes

### 4.1 Assigned-topic mode
A user supplies one or more of:
- a topic,
- a thesis,
- a prompt,
- a report,
- data tables,
- a news item,
- an article to cite,
- or a set of instructions.

Examples:
- “A new jobs report came out. Read the report and data tables and identify trends and oddities. Tie something in the report to a recent news item and write a piece.”
- “I think AI agent proliferation will eventually force all software to harden against model-level hacking capabilities. Write a piece and cite this WSJ article.”

In this mode, the system does **not** choose the topic, but it must still choose:
- the best editorial frame,
- the structure of the piece,
- the most relevant analogs,
- the supporting evidence,
- and the final presentation style.

### 4.2 Auto-topic mode
The system inspects a configurable set of inputs and proposes candidate topics worth writing about.

Potential inputs may include:
- recent news,
- reports and data releases,
- market developments,
- internal priority themes,
- recent pieces already published by the firm,
- other relevant research inputs.

In this mode, the system must:
1. identify candidate topics,
2. explain why each is worth a piece,
3. pick a promising candidate,
4. choose an editorial frame,
5. continue through the same downstream pipeline used for assigned-topic mode.

### 4.3 Shared downstream pipeline
Both entry modes should converge into a common editorial workflow after topic selection / topic receipt.

---

## 5. Existing repository constraints and working assumptions

Canonical layout for this repository (historical **pieces** live under `data/raw/pieces/`):

```text
data/
  processed/
    pieces/
      extracted_features/
      labeled/
  raw/
    pieces/
      dups/
      metadata/          # e.g. pieces_metadata_<YYYYMMDDHHMM>.json (UTC batch runs)
      unlabeled/         # source .docx (and similar) not yet downstream-processed
```

Additional assumptions:
- Historical `.docx` inputs and derived metadata already live under `data/raw/pieces/`.
- Metadata extraction script: `scripts/extract_docx_metadata.py` (defaults: read `data/raw/pieces/unlabeled/`, write `data/raw/pieces/metadata/`).
- Future extraction and labeling scripts also live in `scripts/` with explicit `--input-dir` / `--output-dir`.
- Tests should be written with `pytest`.
- The system should be designed for development in a local project / GitHub repo and worked on in Cursor.

### 5.1 Principle: extend, do not disrupt
Preserve the existing structure unless changes materially improve clarity, observability, or run management.

### 5.2 Recommended extension
To support observability and repeatable run artifacts, add a dedicated runs directory:

```text
artifacts/
  runs/
    <timestamped_run_id>/
```

This is the one structural extension strongly recommended in v1.

Reason:
- per-run artifacts should not be mixed into long-lived canonical datasets,
- each run should be inspectable in one place,
- downstream debugging and evaluation become much easier.

---

## 6. Core system concept

The system should be built as an **editorial pipeline with explicit gates**, not an unbounded free-form multi-agent debate.

The high-level flow:
1. ingest request and sources,
2. normalize inputs,
3. summarize source material,
4. select framing,
5. retrieve historical analogs / comparable pieces,
6. produce a structured brief,
7. draft a piece,
8. critique with specialized agents,
9. revise,
10. evaluate,
11. emit all intermediate and final artifacts.

A later version may add richer loops or more agents, but v1 should prioritize:
- observability,
- determinism,
- inspectability,
- and measurable evaluation.

---

## 7. Editorial pipeline stages

### 7.1 Intake
Purpose:
- receive user prompt or auto-selected topic inputs,
- register a run,
- snapshot relevant settings,
- write initial inputs to disk.

Outputs:
- normalized request payload,
- run manifest,
- source inventory,
- mode (`assigned` or `auto`).

### 7.2 Source reading and extraction
Purpose:
- read reports, articles, notes, tables, transcripts, metadata, and other source materials,
- extract salient facts, trends, anomalies, tensions, and open questions.

Outputs:
- source summaries,
- extracted claims,
- extracted anomalies,
- extracted themes,
- tables / structured notes as applicable.

### 7.3 Topic proposal (auto mode only)
Purpose:
- identify candidate topics worth writing about,
- justify why they matter now,
- rank them.

Outputs:
- topic candidates,
- importance rationale,
- candidate frames per topic,
- selected topic decision artifact.

### 7.4 Framing selection
Purpose:
- decide what kind of piece this should be.

This is one of the highest-leverage steps.

Outputs:
- chosen editorial archetype,
- rejected alternative archetypes,
- rationale for the chosen frame,
- candidate analogs,
- key implications to explore,
- proposed piece structure.

### 7.5 Historical retrieval
Purpose:
- retrieve relevant historical pieces from the archive for style, framing, and topic guidance.

Retrieval should not be topic-only. It should support retrieval by:
- topic similarity,
- editorial archetype similarity,
- voice similarity,
- analog usage,
- structural similarity,
- opening / hook similarity where available.

Outputs:
- ranked retrieval set,
- retrieval rationale,
- references to source pieces,
- retrieved feature summaries.

### 7.6 Piece brief construction
Purpose:
- convert inputs, source findings, framing decisions, and retrieved examples into a single structured brief for the writer.

Outputs:
- canonical brief object,
- thesis,
- audience assumptions,
- constraints,
- required citations,
- candidate analogs,
- implications to explore,
- tone target.

### 7.7 Drafting
Purpose:
- produce a first draft using only the necessary context.

Outputs:
- first draft,
- writer notes,
- optional uncertainty flags.

### 7.8 Critique
Purpose:
- evaluate the draft using specialized critics and explicit rubrics.

Outputs:
- voice critique,
- macro critique,
- evidence critique,
- framing critique,
- combined rubric scores,
- actionable revision notes.

### 7.9 Revision
Purpose:
- improve the draft using critique outputs.

Outputs:
- revised draft,
- change summary,
- unresolved concerns if any remain.

### 7.10 Final evaluation
Purpose:
- determine whether the piece meets the acceptance threshold for this run.

Outputs:
- final scorecard,
- pass / fail decision,
- recommendation for human review,
- final deliverable piece.

---

## 8. Editorial archetypes

The system should not treat all pieces as the same genre. It should work from a defined set of editorial archetypes that can evolve over time.

Initial candidate archetypes:
- **Historical analog piece**: the current setup resembles a prior period or episode, and the analogy is central.
- **Future-implications piece**: current developments imply important downstream effects or structural changes.
- **Data-dissection piece**: a report or dataset contains non-obvious trends, oddities, or internal tensions worth unpacking.
- **Narrative-challenge piece**: consensus framing is wrong, shallow, or incomplete.
- **Regime-shift piece**: a structural change is underway and old assumptions may no longer hold.
- **Second-order-effects piece**: the headline is not the real story; downstream consequences matter more.
- **Scenario piece**: multiple plausible paths are outlined with implications and validation conditions.
- **Misread / mispricing piece**: markets or commentators are interpreting a development incorrectly.

This taxonomy should be represented explicitly in code and artifacts, and refined through labeling and evaluation.

**Repository v1:** stable ids and copy live in `src/tlg_writer/editorial_archetype_taxonomy.v1.json`, validated by `schemas/json/editorial_archetype_taxonomy.schema.json`, and loaded via `tlg_writer.editorial_archetypes`. Optional `piece_label.labels.editorial.primary_archetype_id` (and `alternate_archetype_ids`) use the same id strings (`schemas/json/piece_label.schema.json`).

---

## 9. Historical piece labeling and feature extraction

### 9.1 Why this comes first
Labeling the historical archive is a foundational phase because the core challenge is not just stylistic imitation; it is understanding **how the firm chooses to write pieces**.

The system needs structured knowledge of:
- what kinds of pieces the firm writes,
- when it uses analogs,
- when it emphasizes future implications,
- how conversational or formal it tends to be,
- how strong its point of view tends to be,
- what structural moves recur.

### 9.2 Existing locations
Use:
- `data/raw/pieces/unlabeled/` for source historical pieces (e.g. `.docx`) not yet structurally annotated,
- `data/raw/pieces/metadata/` for batch metadata JSON (`pieces_metadata_<YYYYMMDDHHMM>.json`),
- `data/processed/pieces/extracted_features/` for extracted features,
- `data/processed/pieces/labeled/` for labeling outputs.

### 9.3 Label categories
Initial labels should include:

#### Basic metadata labels
- piece id,
- title,
- date,
- author if available and useful,
- primary topic,
- secondary topics,
- referenced source types.

#### Editorial labels
- editorial archetype,
- whether historical analog is used,
- strength of analog usage,
- whether future implications are emphasized,
- whether the piece is explanatory / predictive / skeptical / contrarian / scenario-based,
- conviction level,
- time horizon.

#### Voice labels
- degree of conversationality,
- degree of formality,
- point-of-view sharpness,
- metaphor / analogy usage,
- rhetorical-question usage,
- jargon density,
- sentence rhythm proxies if feasible.

#### Structural labels
- hook type,
- thesis location,
- paragraph pattern,
- whether it pivots from event to broader implication,
- whether it argues that consensus is missing the real story.

#### Quality labels
- canonical voice example,
- canonical analog example,
- canonical future-implications example,
- likely exclude from training / retrieval,
- reviewer confidence in the labels.

### 9.4 Extracted features vs labels
Maintain a distinction between:
- **extracted features**: model-generated or programmatic measurements and summaries,
- **labels**: editorially meaningful annotations used for training, retrieval, and evaluation.

Example:
- extracted feature: average sentence length,
- label: “conversational but sharp.”

### 9.5 Gold set
Create a manually reviewed gold set of strong historical pieces. The gold set should include:
- canonical voice examples,
- canonical historical-analog examples,
- canonical future-implications examples,
- canonical data-dissection examples,
- representative weaker / atypical examples if useful for contrast.

The gold set will support:
- retrieval benchmarking,
- rubric design,
- evaluation prompts,
- future preference data collection.

---

## 10. Agents

The system should use specialized agents with narrow responsibilities and structured outputs.

### 10.1 Design principle
Each agent should receive only the context needed for its task.

This implies:
- smaller prompts,
- lower cost,
- better reliability,
- easier debugging,
- cleaner observability.

### 10.2 Initial agent set

#### Intake / coordinator
Responsibilities:
- register the run,
- normalize inputs,
- decide which pipeline stages are required,
- persist shared config for the run.

#### Source reader
Responsibilities:
- read reports, tables, articles, and notes,
- extract key facts, anomalies, tensions, and unresolved questions.

#### Topic selector
Responsibilities:
- in auto mode, propose candidate topics,
- score and rank them,
- choose one or hand choices to a later selector.

#### Framing editor
Responsibilities:
- choose the best editorial archetype,
- define the core claim,
- identify rejected alternatives,
- suggest analogs and structure.

#### Retrieval planner / retriever
Responsibilities:
- select relevant historical pieces,
- justify why each retrieved piece matters.

#### Economist critic
Responsibilities:
- audit macro logic,
- detect overstatement,
- identify missing variables,
- challenge weak analogs.

#### Writer
Responsibilities:
- draft the piece from the structured brief and curated context.

#### Voice critic
Responsibilities:
- judge style against the archive,
- detect stiffness, genericity, or mismatch with the house voice.

#### Evidence / framing critic
Responsibilities:
- determine whether the draft supports its own thesis and uses evidence well.

#### Reviser
Responsibilities:
- improve the piece using critic outputs,
- preserve the best parts while addressing the most important weaknesses.

#### Evaluator
Responsibilities:
- produce final rubric scores,
- determine pass / fail,
- recommend whether the piece is ready for human review.

### 10.3 Agent output discipline
Every agent should produce structured outputs that are easy to inspect and save. JSON is preferred for machine-readable artifacts, optionally paired with a human-readable markdown summary.

---

## 11. API strategy

### 11.1 Initial recommendation
Use direct OpenAI API calls to instantiate agents, with one call per agent-stage and carefully scoped context.

Reasoning:
- simple to implement,
- easy to observe,
- flexible for experimentation,
- no need to over-engineer orchestration on day one,
- aligns with the need to feed each agent only what it needs.

### 11.2 Initial pattern
For each stage:
1. construct a stage-specific input payload,
2. call the model with a tightly scoped prompt and expected output schema,
3. validate the output,
4. persist both normalized inputs and outputs,
5. continue to the next stage.

### 11.3 Strong recommendations for API use
- Use structured outputs or schema-constrained outputs wherever practical.
- Log prompt version, model name, and parameters per stage.
- Save token usage and latency per call.
- Save the exact inputs passed to each agent after any truncation or selection.
- Prefer deterministic settings where feasible for non-creative evaluation steps.
- Allow more creative settings only in drafting / revision steps where justified.

### 11.4 Avoid in v1
- deeply nested autonomous agent loops,
- hidden shared state between agents,
- uncontrolled reflection chains,
- large prompts with irrelevant archive context.

---

## 12. Observability and artifacts

Observability is a first-class requirement.

Every run should emit artifacts that make it easy to answer:
- what the system saw,
- what it decided,
- why it made that decision,
- what changed between stages,
- where failures came from.

### 12.1 Run directory
Each run should write to a single timestamped folder:

**run_id** convention: `<UTC-YYYY-MM-DDTHH-MM-SSZ>__<assigned|auto>__<kebab-case-slug>` (example: `2026-04-17T14-32-10Z__assigned__jobs-report`).

```text
artifacts/
  runs/
    2026-04-17T14-32-10Z__assigned__jobs-report/
      manifest.json
      config.json
      logs/
      inputs/
      source_reading/
      topic_selection/
      framing/
      retrieval/
      brief/
      drafting/
      critique/
      revision/
      evaluation/
      final/
```

This can be adjusted slightly, but the principle should hold: one run, one directory, stage subdirectories.

### 12.2 Global run manifest
Each run should include a top-level manifest with:
- run id,
- timestamp,
- git commit if available,
- mode,
- requested topic / selected topic,
- model configuration per stage,
- pipeline stages executed,
- status,
- artifact index.

### 12.3 Stage artifact design
Each stage should emit both:
- machine-readable structured output,
- human-readable summary.

Example pattern per stage:
- `input.json`
- `output.json` (or `output_<agent_role>.json` when several agents share one stage directory)
- `summary.md`
- `metrics.json`
- `debug.json` (optional)

### 12.4 Diff and comparison artifacts
Where useful, save:
- draft-to-revision diffs,
- score changes across iterations,
- retrieval changes,
- alternative frame comparisons.

### 12.5 Logging and metrics
Track per stage:
- start / end timestamps,
- duration,
- model name,
- token usage,
- retries,
- validation failures,
- artifact paths,
- pass / fail outcomes.

### 12.6 Human inspectability
Artifacts should be easy to open directly in the repo or editor.
Prefer:
- concise markdown summaries for humans,
- JSON for structured data,
- predictable file names,
- stable schemas.

### 12.7 Prompts on disk

Stage prompts live under **`prompts/<stage>/`** using the same `<stage>` directory names as the pipeline (e.g. `prompts/framing/system.md`, `prompts/framing/user.md` or `user.jinja`). When explicit versioning beyond git is required, record the effective prompt revision in that stage’s `metrics.json` or `input.json`.

---

## 13. Schemas and canonical objects

Define explicit JSON Schemas for core objects under **`schemas/json/`**, named **`<artifact_type>.schema.json`** in **snake_case** (example: `piece_brief.schema.json`). Use them for API output validation, on-disk `output.json` validation, fixtures, and tests.

Initial schema set (extend as needed):
- `pieces_metadata_batch.schema.json` (batch arrays from `scripts/extract_docx_metadata.py`; per-row record shape lives under this file’s `$defs.piece_docx_metadata_record`)
- `piece_label.schema.json`
- `piece_features.schema.json`
- `source_summary.schema.json`
- `topic_candidate.schema.json`
- `inputs_result.schema.json` (**v1 minimal, shipped:** assigned skeleton writes schema-valid `inputs/output.json`; see §21 step 14)
- `source_reading_result.schema.json` (**v1 minimal, shipped:** assigned skeleton writes schema-valid `source_reading/output.json`; see §21 step 14)
- `topic_selection_result.schema.json` (**v1 minimal, shipped:** assigned skeleton writes schema-valid `topic_selection/output.json` for assigned skip; see §21 step 14)
- `framing_decision.schema.json` (**v1 minimal, shipped:** assigned skeleton writes schema-valid `framing/output.json`; see §21 step 7)
- `retrieval_result.schema.json` (**v1 minimal, shipped:** assigned skeleton writes schema-valid `retrieval/output.json`; see §21 step 7)
- `piece_brief.schema.json` (**v1 minimal, shipped:** assigned skeleton writes schema-valid `brief/output.json`; see §21 step 7)
- `draft_result.schema.json` (**v1 minimal, shipped:** assigned skeleton writes schema-valid `drafting/output.json`; see §21 step 12)
- `critique_result.schema.json` (**v1 minimal, shipped:** assigned skeleton writes schema-valid `critique/output.json`; see §21 step 9)
- `revision_result.schema.json` (**v1 minimal, shipped:** assigned skeleton writes schema-valid `revision/output.json`; see §21 step 10)
- `evaluation_result.schema.json` (**v1 minimal, shipped:** assigned skeleton writes schema-valid `evaluation/output.json`; see §21 step 11)
- `final_deliverable.schema.json` (**v1 minimal, shipped:** assigned skeleton writes schema-valid `final/output.json`; see §21 step 13)
- `run_manifest.schema.json`

---

## 14. Retrieval requirements

Retrieval must support more than semantic topic matching.

### 14.1 Retrieval goals
For a given run, the system should be able to retrieve historical pieces relevant by:
- topic,
- editorial archetype,
- voice,
- structural move,
- analog usage,
- data-dissection similarity,
- future-implications similarity.

### 14.2 Retrieval inputs
Use:
- raw historical piece text,
- metadata,
- labels,
- extracted features,
- manually curated gold-set tags where available.

### 14.3 Retrieval outputs
Each retrieval stage should emit:
- ranked candidates,
- selection rationale,
- why each retrieved piece was selected,
- why key candidates were excluded if necessary.

---

## 15. Revision and stopping logic

The system should use explicit critique thresholds rather than vague iterative dissatisfaction.

### 15.1 Rubric dimensions
At minimum:
- voice match,
- framing quality,
- originality,
- macro soundness,
- evidence usage,
- conversational quality,
- sendability.

### 15.2 Stop conditions
The initial pipeline can use a simple rule such as:
- one draft,
- one critique pass,
- one revision,
- one final evaluation.

Later, thresholds may support additional loops, but v1 should avoid uncontrolled revision churn.

### 15.3 Unresolved issue reporting
If the final piece still has material weaknesses, the evaluator should say so explicitly in an artifact rather than silently passing it through.

---

## 16. Testing strategy

Tests are required for everything practical to test with `pytest`.

### 16.1 Test categories

#### Unit tests
Test:
- parsers,
- schema validators,
- path builders,
- artifact writers,
- config loading,
- prompt / payload builders,
- diff utilities,
- scoring helpers.

#### Integration tests
Test:
- stage orchestration,
- stage artifact creation,
- end-to-end run setup,
- retrieval flow,
- validation failures,
- run manifest completion.

#### Fixture-based tests
Use fixed sample inputs and mocked model outputs to ensure:
- stable behavior,
- reproducible artifacts,
- schema compliance.

#### Contract tests
For each agent stage, validate:
- required inputs are present,
- outputs conform to schema,
- errors are surfaced cleanly.

### 16.2 API testing approach
Mock API responses by default in automated tests. Reserve live-call tests for explicit opt-in workflows.

### 16.3 Artifact assertions
Tests should assert that runs generate the expected files and subdirectories. Observability should itself be tested.

---

## 17. Target repository layout (beyond current `data/`)

Keep **`data/raw/pieces/`** and **`data/processed/pieces/`** as the long-lived corpus roots (see §5). Add:

```text
artifacts/runs/<run_id>/          # per §12; gitignored bulk if needed
prompts/<stage>/                  # per §12.7
schemas/json/*.schema.json        # per §13
scripts/                          # CLIs; today includes extract_docx_metadata.py
src/                              # library code as the pipeline grows
tests/unit/ | tests/integration/ | tests/fixtures/
```

JSON Schemas stay in **`schemas/json/`** (not inside `src/`) so scripts and tests can validate without importing application code. Python modules may wrap or load those schemas from `src/`.

---

## 18. Phased implementation plan

Phases below are ordered by **dependency for eventual quality**, not by mandatory calendar sequence. For **early feedback loops**, land **Phase 0** as soon as manifests, artifact I/O, and minimal schemas exist so operators can run something, open `artifacts/runs/<run_id>/`, and debug stage boundaries **before** archive labeling (Phase 1) or retrieval quality work is exhaustive. Phase 0 and Phase 1 may proceed **in parallel** once the run harness is real.

### Phase 0: runnable assigned-topic skeleton (vertical slice)

Goal:

Exercise run registration, stage boundaries, artifact writers, schemas, and tests **without** blocking on full corpus labeling, gold sets, or high-quality retrieval.

Deliverables:

- A documented entry point (CLI under `scripts/` and/or library in `src/` as the repo evolves) that creates a timestamped `artifacts/runs/<run_id>/` with top-level `manifest.json` (and `config.json` when used) and the stage directories named in §12 and `.agent/AGENTS.md`.
- **`assigned` mode path**: `topic_selection/` may contain only a stub or skip artifact, with the manifest and/or stage `summary.md` stating that auto-topic selection did not run—never silent omission of a stage directory when the pipeline claims it ran.
- Stages may use **fixtures, stubs, or mocked LLM responses**; CI must not require live API keys for the default test path.
- A human-openable deliverable under `final/` (quality may be intentionally low; stage summaries should state limitations honestly).

Acceptance criteria:

- From repo root, a documented command produces a new run directory with predictable layout (fresh `run_id` or a documented fixture run id for tests).
- Failures surface in `logs/`, `metrics.json`, and/or manifest status without dropping stages silently.
- `pytest` asserts expected paths, manifest fields, and schema validation for fixture outputs—**mocked** provider tests by default (see §16.2).

### Phase 1: archive understanding and taxonomy
Goal:
Create a structured understanding of historical pieces and how the firm writes them.

Deliverables:
- stable labeling schema,
- feature extraction pipeline,
- labeled subset of pieces,
- extracted feature artifacts,
- initial archetype taxonomy,
- gold set,
- tests for labeling and feature extraction,
- observability for batch processing runs.

Acceptance criteria:
- historical pieces can be processed into extracted features and labels,
- outputs are saved to existing processed directories,
- artifacts are generated for runs,
- schemas validate,
- tests pass.

### Phase 2: assigned-topic pipeline
Goal:
Build a first end-to-end editorial workflow for user-specified topics and sources—**deepening Phase 0** from mocked or stub stages toward real prompts, retrieval integration, and rubric-worthy outputs where applicable.

Deliverables:
- intake flow,
- source reader,
- framing editor,
- retrieval,
- brief builder,
- writer,
- critics,
- reviser,
- evaluator,
- run artifacts for every stage,
- end-to-end tests with mocks.

Acceptance criteria:
- a full assigned-topic run can execute locally,
- every stage writes structured and human-readable artifacts,
- final outputs can be manually reviewed against rubrics.

### Phase 3: evaluation harness
Goal:
Build a robust evaluation workflow for comparing outputs, diagnosing failures, and collecting human judgment.

Deliverables:
- rubric definitions,
- evaluator outputs,
- comparison utilities,
- draft vs revision diffs,
- fixed evaluation prompts,
- fixtures and baseline reports.

Acceptance criteria:
- generated pieces can be scored consistently,
- changes in system behavior can be compared run to run.

### Phase 4: auto-topic pipeline
Goal:
Allow the system to propose worthwhile topics and choose which piece to write.

Deliverables:
- topic selector,
- topic-ranking artifacts,
- selected-topic rationale,
- integration with the downstream pipeline.

Acceptance criteria:
- auto mode produces inspectable topic candidates,
- topic selection is explainable,
- downstream generation works from the selected topic.

### Phase 5: thresholded multi-agent improvement
Goal:
Expand critique and revision into a stronger threshold-based editorial loop.

Deliverables:
- richer critics,
- stop rules,
- candidate comparison support,
- optional multi-draft tournament flow.

Acceptance criteria:
- the system improves quality without becoming opaque or unbounded.

---

## 19. Initial implementation philosophy

Start with the smallest architecture that can reveal real failure modes.

That means prioritizing:
- a thin **assigned-topic vertical slice** (Phase 0): full run directory shape, mocked or stubbed stages, readable `final/`, so the **piece-creation loop is runnable and inspectable early**,
- **in parallel** (once the run harness exists): labeling and feature extraction,
- explicit archetypes,
- assigned-topic mode before auto-topic mode,
- direct API calls with narrow prompts (live calls optional locally; tests stay mocked by default per §16.2),
- heavy observability,
- schema validation,
- testability.

Do **not** start with a sprawling autonomous council.

The first useful version is a disciplined editorial pipeline, not an agent free-for-all.

---

## 20. Open questions to refine next

- Field-level JSON Schema definitions and required vs optional fields per stage.
- Rubric scales, weights, and pass/fail thresholds.
- Canonical **piece id**: stable key across `pieces_metadata_*.json`, labels, features, and retrieval index (today: prefer `relative_to_repo` from metadata extraction; confirm when duplicates or renames exist).
- Model routing table per stage (vendor, model id, temperature, max tokens).
- Citations / quote-grounding format for client-facing drafts.
- Default redaction policy for `debug.json` and full raw completions.
- Tables and structured numeric extraction from PDFs and reports.
- Whether v1 drafting emits a single candidate or a small tournament of drafts.

---

## 21. Immediate next steps

1. **Phase 0 — vertical slice:** minimal `schemas/json/` for `run_manifest` and any stub stage outputs the skeleton needs; runnable **assigned-topic** path that writes a complete `artifacts/runs/<run_id>/` tree through `final/` using mocks/fixtures; `pytest` for layout, manifest, and schema contracts without live models by default.
2. Formalize remaining `schemas/json/` for piece labels and extracted features as those scripts land.
3. Implement feature extraction and labeling scripts under `scripts/` (read/write under `data/processed/pieces/`). **Shipped (stub):** `scripts/run_corpus_batch_stub.py` reads a `pieces_metadata_*.json` batch and writes schema-valid `piece_label` / `piece_features` JSON; swap in real models or human-in-the-loop labeling when ready.
4. Add batch-run artifact output for those scripts under `artifacts/runs/<run_id>/` with manifests. **Shipped:** each stub batch run writes `manifest.json` validated as `corpus_batch_manifest`, plus `summary.md` and `logs/run.log` (distinct from editorial `run_manifest` until unified).
5. Define the first version of the editorial archetype taxonomy. **Shipped (v1):** bundled JSON + schema + `piece_label` optional fields; see §8 repository note.
6. Build the gold set. **Shipped (index contract):** `schemas/json/gold_set_index.schema.json` lists curated pieces by `piece_relative_to_repo`, §9.5 roles, optional `primary_archetype_id` checked against the bundled archetype taxonomy; `tlg_writer.gold_set` + `scripts/validate_gold_set_index.py` + fixture under `tests/fixtures/corpus/`. Full manual curation remains ongoing work.
7. **Deepen** the assigned-topic pipeline (real stages, prompts, retrieval) with observability—each increment still leaving inspectable artifacts per §12. **Shipped:** `schemas/json/piece_brief.schema.json` (v1) with assigned skeleton `brief/output.json` validated as `piece_brief`; `schemas/json/framing_decision.schema.json` and `schemas/json/retrieval_result.schema.json` (v1) with `framing/output.json` and `retrieval/output.json` validated accordingly (stub-filled fields; empty `ranked_hits` in Phase 0; no live LLM or archive queries).
8. Add and extend `pytest` coverage for each stage and artifact writer. **Shipped (first increment):** integration test validates every skeleton stage `output.json` / `metrics.json` against the correct schema; manifest `stages_executed` / `artifact_index` / `config.json` shape checks; corpus stub tests cover `piece_artifact_stem`, empty metadata batch, and `run.log` smoke (`tests/integration/test_skeleton_pipeline.py`, `tests/integration/test_corpus_batch_stub.py`, `tests/unit/test_corpus_batch_artifacts.py`).
9. **Deepen** critique observability: **`critique_result` v1** JSON Schema (SPEC §7.8 / §15.1 rubric dimensions) with assigned skeleton `critique/output.json` validated accordingly (null scores = not evaluated in Phase 0; no live critics).
10. **Deepen** revision observability: **`revision_result` v1** JSON Schema (SPEC §7.9: revised body, change summary, unresolved concerns) with assigned skeleton `revision/output.json` validated accordingly (Phase 0 cosmetic stub only).
11. **Deepen** final-evaluation observability: **`evaluation_result` v1** JSON Schema (SPEC §7.10: pass/fail, recommendation, scorecard; §15.3 explicit weaknesses in `summary`) with assigned skeleton `evaluation/output.json` validated accordingly (null scorecard = not evaluated in Phase 0).
12. **Deepen** drafting observability: **`draft_result` v1** JSON Schema (SPEC §7.7: body, writer notes, uncertainty flags) with assigned skeleton `drafting/output.json` validated accordingly (stub prose; critique/revision inputs reference the canonical `draft_result` document).
13. **Deepen** packaging observability: **`final_deliverable` v1** JSON Schema (markdown body, limitations, operator summary) with assigned skeleton `final/output.json` validated accordingly (`final/piece.md` mirrors `body_markdown`; Phase 0 quality by design).
14. **Deepen** intake observability: **`inputs_result`**, **`source_reading_result`**, and **`topic_selection_result`** v1 JSON Schemas with assigned skeleton `inputs/`, `source_reading/`, and `topic_selection/output.json` validated accordingly (`topic_selection` v1 models assigned skip only; framing consumes canonical intake artifacts on `input.json`).

---

## 22. Summary

This project should be treated as a system for producing high-quality editorial **pieces**, not a generic writing assistant.

Its core differentiators should be:
- explicit editorial framing,
- historical archive understanding,
- specialized agents with narrow contexts,
- strong observability,
- rigorous artifact writing,
- and a clean, testable pipeline architecture.

The immediate priority is not “make the smartest writer.”
The immediate priority is to build the structure that lets the system make better editorial decisions and makes those decisions legible to you—and to **run and inspect that structure end-to-end early** (Phase 0), then improve quality stage by stage rather than debugging everything at once after a big bang.
