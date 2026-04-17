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

- `<YYYY-MM-DD> — <title> — status — owner`
