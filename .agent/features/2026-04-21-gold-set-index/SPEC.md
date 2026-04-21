# Feature: Gold set index (v1 contract)

## Goal

Ship SPEC §21 step 6 as an operator- and test-friendly **index contract** before large-scale manual curation: a JSON document listing gold-set pieces with stable `piece_relative_to_repo` keys (aligned with metadata extraction), editorial roles from §9.5, and optional `primary_archetype_id` validated against the bundled taxonomy.

## Out of scope (this PR)

- Populating a real corpus-wide gold list or ingesting `.docx` content.
- Retrieval or pipeline stages consuming the index (follow-up).

## Acceptance

- `schemas/json/gold_set_index.schema.json` documents the shape.
- `tlg_writer.gold_set` validates schema plus duplicate-path and archetype-id semantics.
- `scripts/validate_gold_set_index.py` validates a path (defaults to the repo fixture for smoke).
- `pytest` covers happy path, duplicate paths, bad roles, and unknown archetype ids.
