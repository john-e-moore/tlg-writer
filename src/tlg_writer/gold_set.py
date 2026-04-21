"""Gold set index (SPEC §9.5, §21 step 6): schema + semantic checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tlg_writer.editorial_archetypes import load_editorial_archetype_taxonomy
from tlg_writer.json_schema import validate


def validate_gold_set_index_document(obj: dict[str, Any]) -> None:
    """Raise jsonschema.ValidationError if the document shape is invalid."""
    validate(obj, "gold_set_index")


def validate_gold_set_index_semantics(
    obj: dict[str, Any], *, taxonomy_version: str | None = None
) -> None:
    """
    Additional checks: duplicate piece paths, archetype ids when present.

    Call after ``validate_gold_set_index_document``.
    """
    tax_ver = taxonomy_version if taxonomy_version is not None else obj.get("taxonomy_version") or "v1"
    entries = obj["entries"]
    paths: list[str] = []
    for i, row in enumerate(entries):
        p = row["piece_relative_to_repo"]
        if p in paths:
            raise ValueError(
                f"Duplicate piece_relative_to_repo {p!r} (entries[{i}] duplicates an earlier row)"
            )
        paths.append(p)
        aid = row.get("primary_archetype_id")
        if aid is None:
            continue
        tax = load_editorial_archetype_taxonomy(tax_ver)
        if aid not in tax.by_id():
            raise ValueError(
                f"entries[{i}].primary_archetype_id {aid!r} is not in taxonomy {tax_ver}"
            )


def load_gold_set_index(
    path: Path, *, check_semantics: bool = True, taxonomy_version: str | None = None
) -> dict[str, Any]:
    """Read JSON from path, validate schema, then optional semantic checks."""
    with path.open(encoding="utf-8") as f:
        doc: dict[str, Any] = json.load(f)
    validate_gold_set_index_document(doc)
    if check_semantics:
        validate_gold_set_index_semantics(doc, taxonomy_version=taxonomy_version)
    return doc
