# Feature: Validate corpus piece_label / piece_features directories

## Goal

Give operators a **read-only** way to confirm every `*.json` file in a labels or features directory validates against `piece_label` or `piece_features` before relying on those files in downstream work.

## Scope

- Library helper under `tlg_writer.corpus_piece_artifacts` and CLI `scripts/validate_corpus_piece_json.py`.
- Top-level `*.json` by default; optional `--recursive` for nested trees.
- No writes, no HTTP, no change to stub batch behavior.

## Acceptance

- `pytest` covers happy path, invalid JSON, schema failure, and CLI smoke.
- README documents usage (directories must contain only the expected per-piece artifacts, not mixed fixture types).
