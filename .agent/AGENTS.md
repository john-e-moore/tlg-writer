# AGENTS.md

How coding agents work in **tlg-writer**. Complements `README.md` and `.agent/SPEC.md` with execution behavior, delivery standards, and observability.

## Project context

- Purpose: an observable editorial system that produces macro advisory **pieces** in a fixed house style.
- Modes: `assigned-topic` and `auto-topic`.
- Corpus and batch outputs live under `data/`; treat them as canonical inputs for labeling, retrieval, evaluation, and voice work.
- Requirements baseline: `.agent/SPEC.md`.

## Instruction priority

1. Direct user request in the active session.
2. This file (`.agent/AGENTS.md`).
3. `.agent/SPEC.md`.
4. Other repo docs and local conventions.
5. Default toolchain habits.

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
3. Add or extend an ExecPlan in `.agent/PLANS.md` for multi-step or cross-cutting work (see `.agent/PLANS.md` for entry format).
4. Implement in small, testable slices.
5. Run tests; paste concise evidence into the PR / ExecPlan.
6. Update docs touched by behavior.
7. Confirm new artifacts stay readable and attributable (`run_id`, `stage`, `agent` in logs and metrics).

Do not stop at partial delivery unless blocked (credentials, missing inputs, network, or explicit user stop).

## Feature branch flow

1. Branch from `main`.
2. Feature brief: `.agent/features/<YYYY-MM-DD>-<feature-slug>/SPEC.md`.
3. ExecPlan in `.agent/PLANS.md` linking that brief.
4. Implement in reviewable chunks; keep the ExecPlan current.
5. PR body from `.agent/PR_TEMPLATE.md`.

Feature briefs stay local to the feature; they do not duplicate the whole spec.

## When to use an ExecPlan

Default for work that touches multiple pipeline stages, schemas, artifact contracts, run layout, agent orchestration, retrieval/labeling/evaluation, observability, or ingestion. Skip for typos, one-off test tweaks, or single-file fixes.

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
- [ ] `.agent/PLANS.md` updated if scope warrants it.
- [ ] Code, prompts, schemas, tests, docs aligned.
- [ ] Artifacts remain inspectable.
- [ ] No secrets.
- [ ] Validation evidence noted.
