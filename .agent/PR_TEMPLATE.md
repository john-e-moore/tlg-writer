# Pull request template

Use for features and substantial refactors. Keep it short, evidence-based, and aligned with `.agent/SPEC.md` and `.agent/AGENTS.md`.

## Summary

- What changed for readers/operators?
- Why now?

## Links

- Branch: `<name>`
- Feature brief: `.agent/features/<YYYY-MM-DD>-<feature-slug>/SPEC.md` or `N/A`
- ExecPlan: section in `.agent/PLANS.md` titled `ExecPlan: …` or `N/A`

## Scope

- In scope:
- Explicitly not in scope:

## Acceptance criteria

- [ ] …
- [ ] …
- [ ] If this PR adds or changes editorial **pipeline** stages: a sample `artifacts/runs/<run_id>/` exists (real run or **test fixture path** under `tests/fixtures/`) demonstrating the new layout or behavior—or N/A with one-line reason

## Validation evidence

- [ ] Lint/format (if configured)
- [ ] `pytest` (note scope: full / subset / skipped)
- [ ] Sample `artifacts/runs/<run_id>/` inspected (or fixture path; or N/A)
- [ ] Smoke: pipeline or script path (or documented skip); note if run used **mocked** LLM only
- [ ] Re-run idempotence checked where outputs are written

Commands (from repo root):

```bash
pytest -q
python scripts/extract_docx_metadata.py --input-dir data/raw/pieces/unlabeled --output-dir data/raw/pieces/metadata
# add pipeline or other commands when they exist
```

## Artifact and observability

- New or changed paths under `artifacts/runs/` (stage dirs, `manifest.json`, per-stage `metrics.json`, etc.):
- Changes to `schemas/json/*.schema.json`:
- Logging / tracing changes:
- Operator-facing summaries (`summary.md`, etc.):

## Data and contracts

- Changes under `data/raw/pieces/` or `data/processed/pieces/` (layout, filenames, manifest fields):
- Schema or JSON shape changes (downstream compatibility):

## Prompts and models

- `prompts/<stage>/` files added/changed:
- Model or parameter changes per stage:
- Cost/latency notes:

## Ops and rollback

- Docs updated (`README.md`, `.agent/*`, inline docstrings where behavior changed):
- Rollback / recovery:
- Known risks:

## Security and privacy

- [ ] No secrets committed
- [ ] Sensitive corpus handling respected (PII masking, `.gitignore` paths)
- [ ] Prompt/response retention policy followed for new logging

## Risks and follow-ups

- Risks:
- Follow-ups (issues or later PRs):
