# Feature: Corpus batch statistics (stub)

## Goal

Emit structured **batch_statistics** on `corpus_batch_manifest` and enrich `summary.md` so operators see skip reasons, metadata title coverage, `words_approx` rollups, and primary archetype histograms without ad-hoc JSON crunching.

## Scope

- Stub batch only (`run_corpus_batch_stub`); schema optional on manifest for backward compatibility, stub always writes `batch_statistics` when emitting a new manifest.
- No live labeling or new data paths.

## Acceptance

- `corpus_batch_manifest.batch_statistics` validates against extended schema.
- Integration tests cover skip breakdown and archetype histogram on a small fixture batch.
