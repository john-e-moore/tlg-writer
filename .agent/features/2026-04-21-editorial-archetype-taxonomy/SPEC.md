# Feature: Editorial archetype taxonomy v1

## Goal

Ship SPEC §21 step 5: a **first version** of the editorial archetype taxonomy as explicit, schema-validated artifacts and stable ids usable in `piece_label` and downstream pipeline code.

## Scope

- Bundled taxonomy document (`editorial_archetype_taxonomy.v1.json`) matching SPEC §8 candidate list.
- JSON Schema `editorial_archetype_taxonomy` plus optional `labels.editorial.primary_archetype_id` / `alternate_archetype_ids` on `piece_label` (enum aligned to taxonomy).
- Library loader (`tlg_writer.editorial_archetypes`) and operator CLI `scripts/list_editorial_archetypes.py`.

## Non-goals

- Gold set, retrieval, or auto-assignment of archetypes to new pieces.
- Tightening required fields on `piece_label` beyond optional archetype keys (stubs stay valid).

## Acceptance

- `pytest` covers taxonomy validation, id uniqueness, enum alignment with `piece_label`, and rejection of unknown ids.
- Operators can list ids and human summaries from the CLI.
