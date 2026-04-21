"""Editorial archetype taxonomy (SPEC §8): load, validate, and resolve stable ids."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from typing import Any, Mapping

from tlg_writer.json_schema import validate


@dataclass(frozen=True)
class EditorialArchetype:
    """One row from ``editorial_archetype_taxonomy.v*.json``."""

    id: str
    display_name: str
    summary: str


@dataclass(frozen=True)
class EditorialArchetypeTaxonomy:
    """Validated v1 taxonomy document."""

    version: str
    archetypes: tuple[EditorialArchetype, ...]

    def by_id(self) -> Mapping[str, EditorialArchetype]:
        return {a.id: a for a in self.archetypes}


def _taxonomy_bytes(version: str) -> bytes:
    if version != "v1":
        raise ValueError(f"Unsupported taxonomy version: {version!r} (only v1 is bundled)")
    return resources.files("tlg_writer").joinpath(f"editorial_archetype_taxonomy.{version}.json").read_bytes()


def raw_taxonomy_document(version: str = "v1") -> dict[str, Any]:
    """Return the bundled taxonomy JSON object after schema validation."""
    data: dict[str, Any] = json.loads(_taxonomy_bytes(version).decode("utf-8"))
    validate(data, "editorial_archetype_taxonomy")
    return data


@lru_cache(maxsize=4)
def load_editorial_archetype_taxonomy(version: str = "v1") -> EditorialArchetypeTaxonomy:
    """
    Load and schema-validate the bundled editorial archetype taxonomy.

    The on-disk JSON under ``src/tlg_writer/`` is the canonical v1 list from SPEC §8.
    """
    raw = raw_taxonomy_document(version)
    rows = raw["archetypes"]
    seen: set[str] = set()
    out: list[EditorialArchetype] = []
    for row in rows:
        aid = row["id"]
        if aid in seen:
            raise ValueError(f"Duplicate archetype id in taxonomy: {aid!r}")
        seen.add(aid)
        out.append(
            EditorialArchetype(
                id=aid,
                display_name=row["display_name"],
                summary=row["summary"],
            )
        )
    return EditorialArchetypeTaxonomy(version=raw["taxonomy_version"], archetypes=tuple(out))
