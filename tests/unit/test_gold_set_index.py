"""Gold set index schema and semantics."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tlg_writer.gold_set import (
    load_gold_set_index,
    validate_gold_set_index_document,
    validate_gold_set_index_semantics,
)
from tlg_writer.paths import repo_root


def test_fixture_validates() -> None:
    path = repo_root() / "tests/fixtures/corpus/gold_set_index_minimal.json"
    doc = load_gold_set_index(path)
    assert doc["gold_set_version"] == "fixture-v1"
    assert len(doc["entries"]) == 2


def test_rejects_duplicate_paths() -> None:
    doc = {
        "gold_set_version": "x",
        "entries": [
            {"piece_relative_to_repo": "a/b.docx", "roles": ["canonical_voice_example"]},
            {"piece_relative_to_repo": "a/b.docx", "roles": ["canonical_future_implications_example"]},
        ],
    }
    validate_gold_set_index_document(doc)
    with pytest.raises(ValueError, match="Duplicate piece_relative_to_repo"):
        validate_gold_set_index_semantics(doc)


def test_rejects_unknown_archetype() -> None:
    doc = {
        "gold_set_version": "x",
        "entries": [
            {
                "piece_relative_to_repo": "only.docx",
                "roles": ["canonical_voice_example"],
                "primary_archetype_id": "not_a_real_archetype_id",
            }
        ],
    }
    validate_gold_set_index_document(doc)
    with pytest.raises(ValueError, match="not_a_real_archetype_id"):
        validate_gold_set_index_semantics(doc)


def test_schema_rejects_bad_role(tmp_path: Path) -> None:
    bad = {
        "gold_set_version": "x",
        "entries": [
            {"piece_relative_to_repo": "x.docx", "roles": ["not_a_valid_role"]},
        ],
    }
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(Exception):
        load_gold_set_index(p)
