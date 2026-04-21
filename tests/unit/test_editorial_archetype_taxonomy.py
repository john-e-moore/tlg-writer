"""Bundled editorial archetype taxonomy (SPEC §8) and label contract alignment."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from tlg_writer.editorial_archetypes import load_editorial_archetype_taxonomy, raw_taxonomy_document
from tlg_writer.json_schema import validate, validate_file
from tlg_writer.paths import repo_root, schemas_dir


def _fixture(name: str) -> Path:
    return repo_root() / "tests" / "fixtures" / "corpus" / name


def test_raw_taxonomy_document_validates() -> None:
    doc = raw_taxonomy_document("v1")
    assert doc["taxonomy_id"] == "editorial_archetypes"
    assert len(doc["archetypes"]) == 8


def test_load_editorial_archetype_taxonomy_ids_unique() -> None:
    tax = load_editorial_archetype_taxonomy("v1")
    ids = [a.id for a in tax.archetypes]
    assert len(ids) == len(set(ids))


def test_taxonomy_ids_match_piece_label_enum() -> None:
    tax = load_editorial_archetype_taxonomy("v1")
    from_ids = {a.id for a in tax.archetypes}
    with (schemas_dir() / "piece_label.schema.json").open(encoding="utf-8") as f:
        label_schema = json.load(f)
    enum_ids = set(label_schema["$defs"]["editorial_archetype_id"]["enum"])
    assert from_ids == enum_ids


def test_piece_label_with_archetype_fixture() -> None:
    validate_file(_fixture("piece_label_with_archetype.json"), "piece_label")


def test_piece_label_rejects_unknown_archetype_id() -> None:
    bad = {
        "piece_id": "x",
        "schema_version": "v1",
        "labels": {
            "basic_metadata": {},
            "editorial": {"primary_archetype_id": "not_a_real_archetype"},
            "voice": {},
            "structural": {},
            "quality": {},
        },
    }
    with pytest.raises(jsonschema.ValidationError):
        validate(bad, "piece_label")


def test_editorial_archetype_taxonomy_fixture_file_matches_schema() -> None:
    path = repo_root() / "src" / "tlg_writer" / "editorial_archetype_taxonomy.v1.json"
    validate_file(path, "editorial_archetype_taxonomy")
