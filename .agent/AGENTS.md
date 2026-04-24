# AGENTS.md

How coding agents work in **tlg-writer**. Complements `README.md` and `.agent/SPEC.md` with execution behavior, delivery standards, and observability.

## Project context

- Purpose: an observable editorial system that produces macro advisory **pieces** in a fixed house style.
- Modes: `assigned-topic` and `auto-topic`.
- Corpus and batch outputs live under `data/`; treat them as canonical inputs for labeling, retrieval, evaluation, and voice work.
- Requirements baseline: `.agent/SPEC.md`.
- **Where we are:** `.agent/PROGRESS.md` (phase checkboxes; keep in sync after merges).

## Instruction priority

1. Direct user request in the active session.
2. This file (`.agent/AGENTS.md`).
3. `.agent/SPEC.md`.
4. `.agent/PROGRESS.md` — human-readable phase checklist; **update it when substantive work completes** (see **Progress tracking** below). It does not replace SPEC.
5. Other repo docs and local conventions.
6. Default toolchain habits.

If something is missing, choose the safest assumption, record it in the active plan, and continue.

## Repository conventions (tlg-writer)

Use these paths and names unless a feature brief or ExecPlan explicitly supersedes them.

### Data (historical pieces)

| Role | Path |
|------|------|
| Raw `.docx` inputs | `data/raw/pieces/unlabeled/` |
| Per-file / batch metadata JSON | `data/raw/pieces/metadata/` |
| Duplicate manifests, quarantine | `data/raw/pieces/dups/` |
| Extracted features (batch or per-piece) | `data/processed/pieces/extracted_features/` |
| Editorial labels | `data/processed/pieces/labeled/` |

- **Metadata batches**: `data/raw/pieces/metadata/pieces_metadata_<YYYYMMDDHHMM>.json` (UTC), one array of records per run. Stable field for joining: prefer `relative_to_repo` when present.
- **Do not** reshape `data/` casually; extend with new subdirs or schemas rather than renaming existing trees.
- Large or private blobs under `data/` stay out of git per `.gitignore`; scripts must still write predictable relative paths into manifests.

### Pipeline run artifacts

Root: `artifacts/runs/<run_id>/`.

- **run_id**: `<UTC-timestamp>__<mode>__<short-slug>` where timestamp is `YYYY-MM-DDTHH-MM-SSZ`, mode is `assigned` or `auto`, slug is lowercase ASCII with hyphens (e.g. `2026-04-17T14-32-10Z__assigned__jobs-report`).
- **Stage directories** (exact names): `inputs/`, `source_reading/`, `topic_selection/`, `framing/`, `retrieval/`, `brief/`, `drafting/`, `critique/`, `revision/`, `evaluation/`, `final/`, plus `logs/` and top-level `manifest.json` (and `config.json` when used).

### Per-stage files

Within each stage directory, prefer this stem pattern:

| File | Role |
|------|------|
| `input.json` | Normalized inputs passed into the stage |
| `output.json` | Parsed, schema-validated model output |
| `summary.md` | Short human-readable recap |
| `metrics.json` | Tokens, latency, retries, validation outcomes |
| `debug.json` | Optional; redacted raw provider payloads if policy allows |

If multiple agents share a stage, use `output_<agent_role>.json` (snake_case role, e.g. `output_voice_critic.json`) instead of a single `output.json`.

### Prompts

- **Location**: `prompts/<stage>/` where `<stage>` matches the stage directory name (e.g. `prompts/framing/`, `prompts/drafting/`).
- **Files**: `system.md` and `user.md` (or `user.jinja` when templating). Optional `schema_hint.md` for human-facing output rules.
- **Versioning**: Git history is primary; if you need explicit versions, suffix `user_v002.md` and record `prompt_versions: { "user": "v002" }` in that stage’s `metrics.json` or `input.json`.

### JSON Schemas

- **Location**: `schemas/json/`.
- **Filenames**: `<artifact_type>.schema.json`, snake_case artifact type matching the object root (e.g. `piece_brief.schema.json`, `run_manifest.schema.json`).
- **Usage**: validate `output.json` (and batch JSON under `data/` when applicable); mirror shapes in tests under `tests/fixtures/`.

### Code layout (target)

Until modules land, keep scripts in `scripts/` (`extract_docx_metadata.py` is the reference). New pipeline code should move toward `src/` with thin CLI wrappers in `scripts/`. Do not scatter OpenAI calls; use one module boundary for the HTTP client.

## Working agreement

- Build an **editorial system**, not a generic chatbot.
- Prefer plain, explicit Python over heavy frameworks unless complexity pays off.
- Observable at every step: deterministic artifacts, stable schemas, rerunnable steps.
- No secrets in code, commits, or emitted JSON.

## Early feedback loops (pipeline work)

When implementing the editorial pipeline (not one-off corpus scripts), optimize for **early, inspectable runs**:

1. **Vertical slice first:** before investing heavily in retrieval quality or full labeling coverage, ship a path that creates `artifacts/runs/<run_id>/` with the stage directories in this file, top-level `manifest.json`, and something readable under `final/`. Stubs and fixture-driven `output.json` files are valid; quality can come later. See `.agent/SPEC.md` §18 Phase 0.
2. **`assigned` mode:** `topic_selection/` may record an explicit skip or stub (summarized in `summary.md` / manifest) rather than pretending auto-topic ran.
3. **Tests default to mocks:** integration tests prove directory layout, manifest fields, and schema validation without live API calls unless explicitly opt-in (see `.agent/SPEC.md` §16.2).
4. **Parallel work:** archive labeling, feature extraction, and gold-set curation can proceed alongside the skeleton; they must not be treated as a prerequisite to having a runnable, debuggable run directory.

## Non-negotiables

- Every meaningful pipeline step writes inspectable files under a single **timestamped** `artifacts/runs/<run_id>/`.
- Respect the `data/raw/pieces/*` and `data/processed/pieces/*` layout above.
- Substantive behavior gets `pytest` coverage.
- LLM usage goes through explicit wrappers; agents get minimal context.
- Both `assigned` and `auto` modes must remain representable in manifests and configs.

## Delivery workflow

For non-trivial work:

1. Read `.agent/SPEC.md`.
2. Add `.agent/features/<YYYY-MM-DD>-<feature-slug>/SPEC.md` when behavior is net-new.
3. Add or extend an ExecPlan in `.agent/PLANS.md` for multi-step or cross-cutting work (see `.agent/PLANS.md` for entry format). For **new pipeline behavior**, the first merged slice should usually satisfy **Early feedback loops** (inspectable `artifacts/runs/…`, mocks OK) before large quality expansions.
4. Implement in small, testable slices—each slice should leave **traces** (files, manifest updates, or explicit skip records) an operator can open.
5. Run tests; paste concise evidence into the PR / ExecPlan.
6. Update docs touched by behavior.
7. Confirm new artifacts stay readable and attributable (`run_id`, `stage`, `agent` in logs and metrics).
8. **Update `.agent/PROGRESS.md`** when the merge completes substantive scope (tick boxes, adjust **Current focus** if priorities shifted, bump **Last updated**). Skip for typos, comment-only edits, or test-only tweaks with no behavior change.

Do not stop at partial delivery unless blocked (credentials, missing inputs, network, or explicit user stop). Partial **pipeline** delivery is acceptable when the ExecPlan scope is explicitly “skeleton + mocks”; it is not acceptable when stages claim to run but omit outputs without documentation. When a merged slice introduces or changes **emitters** for `artifacts/runs/…` or `data/processed/pieces/…`, run the documented command(s) so concrete paths exist, **then** apply the human pause rule in **Infra and contracts phase** below—not earlier.

## Progress tracking (`.agent/PROGRESS.md`)

- **Who:** Any agent (or human) completing work that changes **operator-visible** capability, corpus tooling, pipeline stages, or phase status.
- **When:** After implementation is merged or handed off as “done” for the slice—not before tests pass / scope is agreed.
- **What:** Check or uncheck the relevant items; edit **Current focus** if the next priority changed; update **Last updated**. Keep entries short—ExecPlans in `.agent/PLANS.md` hold detail and evidence.
- **Why:** `.agent/PLANS.md` is long and ExecPlan-centric; SPEC is normative but not a checklist. **PROGRESS** is the fast answer to “what shipped / what’s next?”

## Feature branch flow

Target flow: **new branch → implement in logical commits → test → open PR when the scoped work is done** (not a standing pile of uncommitted work).

1. Branch from `main`.
2. Feature brief: `.agent/features/<YYYY-MM-DD>-<feature-slug>/SPEC.md`.
3. ExecPlan in `.agent/PLANS.md` linking that brief (include **branch name** and **PR** in the plan header when known).
4. Implement in reviewable chunks; keep the ExecPlan current.
5. PR body from `.agent/PR_TEMPLATE.md`.

**Branch naming:** prefer `feature/<short-slug>` (kebab-case slug, tied to the feature brief slug when practical). Use another prefix only if the team standard differs.

**Branches and PRs:** one **topic branch** per **mergeable unit of review**—typically one open PR per branch. Do not stack unrelated work on the same branch. If the user explicitly asks for stacked or dependent PRs, follow that session instruction.

**Merge bar:** merge to `main` only when CI (if present) is green and the checks in **Before “done”** and the ExecPlan’s validation section have been run (or skips documented). Record concise evidence in the PR and ExecPlan.

**GitHub CI:** pull requests and pushes to `main` run `pytest` via `.github/workflows/ci.yml` (job **Tests**). Enable **Require status checks to pass before merging** on `main` and select that job if you want the merge gate enforced in GitHub.

### Infra and contracts phase: auto-merge and when to stop

While building **schemas, layout, stubs/mocks, tests, and docs**—and slices that **emit** operator-visible trees—it is reasonable to **minimize manual merge toil**:

1. Open the PR as usual; confirm **Tests** is green on GitHub (same suite as local `pytest -q`).
2. Either enable **Auto-merge** (squash or merge) on the PR in the GitHub UI, or from a trusted machine with `gh` and permissions: `gh pr merge <n> --auto --squash` (merges when required checks pass).
3. After merge: `git checkout main && git pull`, then start the next `feature/<short-slug>` from updated `main`.

**Default for agents:** keep **implementing and merging** scoped work. Roadmap bullets that mention “human review,” “operator rubric,” or “HITL” describe **who owns quality of the outputs**, not a reason to defer merges or skip running the pipeline. Ship the PR when CI is green, then **run** the CLIs or library entry points needed so **concrete paths on disk** exist for inspection (stub runs, fixtures under `tests/fixtures/`, env-gated **live** calls when the slice scope and credentials allow—document mocks or skips when they do not).

**Pause and wait for the human** when **both** are true:

1. **Artifacts to inspect exist**—for example a completed `artifacts/runs/<run_id>/`, new files under `data/processed/pieces/…`, or other outputs the ExecPlan / acceptance criteria name (including a **fixture path** under `tests/fixtures/` when the slice is intentionally test-only and no new run dir is required), **and**
2. The meaningful **next** step is for the human to read, judge, or curate those outputs (or otherwise continue outside the agent loop).

When you pause: list **exact repository-relative paths** (and how to reproduce the run). Do **not** start a **new unrelated** slice until the user continues.

**Also pause** (artifacts optional) when **blocked**: missing credentials or network where the slice requires them, merge/`gh` permissions, an ExecPlan marked **`blocked`**, a genuinely **ambiguous** next step after reading `.agent/PLANS.md` and `.agent/PROGRESS.md`, or the user explicitly requests **review before merge** on a specific PR.

**Do not pause** merely because upcoming roadmap work will eventually need human judgment—**merge, run, materialize outputs first**, then pause with paths when something is actually on disk (or explicitly declared N/A in the ExecPlan) for the human to open.

**Phased / roadmap work:** align branches with **vertical slices** you would merge independently (see **Early feedback loops**), not necessarily one git branch per numbered subsection of `.agent/SPEC.md`. Split a large spec phase across **multiple PRs** when review or rollback boundaries warrant it; prefer **frequent small merges** to `main` over one long-lived mega-branch or bulk unreviewed work on `main`.

**Communicating to the agent:** defaults live in this file (**Instruction priority**). Each session should still name the **branch**, **PR link** (if updating an existing PR), and **scope** (what is in/out) so the active request can override safely—no need to repeat full branching policy every prompt if this section stays current.

Feature briefs stay local to the feature; they do not duplicate the whole spec.

## When to use an ExecPlan

Default for work that touches multiple pipeline stages, schemas, artifact contracts, run layout, agent orchestration, retrieval/labeling/evaluation, observability, or ingestion. Skip for typos, one-off test tweaks, or single-file fixes.

For **new editorial pipeline work**, the first ExecPlan should typically cover **Phase 0** (skeleton run, mocks, inspectable `artifacts/runs/…`) per `.agent/SPEC.md` §18 and `.agent/PLANS.md` **Early vertical slices**.

## Module boundaries (keep separated)

Intake, ingestion/normalization, feature extraction, labeling, retrieval, brief construction, framing, drafting, critique, revision, evaluation, artifact I/O, and API clients—avoid gluing prompts, orchestration, persistence, and HTTP into one module.

## LLM usage

- OpenAI (or successor) behind a small internal API.
- Structured outputs validated against `schemas/json/*.schema.json` where possible.
- Record model id, temperature, max tokens, token usage, and latency in `metrics.json`.
- Prefer cheaper models for classification/extraction; reserve stronger models for framing, drafting, and revision.

## Before “done”

Run the mix that fits the change: unit tests, schema/contract tests, artifact layout tests, smoke CLI, idempotent re-run checks, and spot-read of JSON/markdown under `artifacts/runs/…`. If something could not run, say exactly what was skipped and why.

## Security and cost

- No API keys in repo or artifacts.
- Store full prompts/responses only when needed; redact PII; align with team policy in manifests.
- Tight contexts; no duplicate calls when upstream artifacts already hold the answer.

## Completion checklist

- [ ] Requirements trace to `.agent/SPEC.md`.
- [ ] `.agent/PROGRESS.md` updated if the change completes or reopens phase-level work (checkboxes / current focus / date).
- [ ] `.agent/PLANS.md` updated if scope warrants it.
- [ ] Code, prompts, schemas, tests, docs aligned.
- [ ] Artifacts remain inspectable.
- [ ] No secrets.
- [ ] Validation evidence noted.
