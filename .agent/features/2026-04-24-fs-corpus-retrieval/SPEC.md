# Feature: Filesystem corpus retrieval (Phase 0)

## Goal

Optional `piece_label` directory scan so assigned/auto skeleton runs can emit **non-empty** `retrieval_result.ranked_hits` without live models, for operator-visible traces and brief downstream wiring tests.

## Scope

- In: `build_retrieval_result_from_labels_dir`, CLI flags, `config.json` `corpus_retrieval`, pytest + fixtures under `tests/fixtures/corpus/retrieval_labels/`.
- Out: embedding search, lexical index, framing LLM, changing default Phase 0 behavior without `corpus_labels_dir`.

## Acceptance

- `pytest -q` green; smoke command in `.agent/PLANS.md` ExecPlan produces schema-valid `retrieval/output.json` with three hits from fixtures.
