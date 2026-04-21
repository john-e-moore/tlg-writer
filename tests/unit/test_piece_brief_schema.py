"""piece_brief JSON Schema and taxonomy enum alignment."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from tlg_writer.json_schema import validate, validate_file
from tlg_writer.paths import repo_root, schemas_dir
from tlg_writer.piece_brief import build_stub_piece_brief_assigned


def _fixture(name: str) -> Path:
    return repo_root() / "tests" / "fixtures" / "pipeline" / name


def test_piece_brief_minimal_fixture() -> None:
    validate_file(_fixture("piece_brief_minimal.json"), "piece_brief")


def test_piece_brief_rejects_extra_keys() -> None:
    doc = json.loads(_fixture("piece_brief_minimal.json").read_text(encoding="utf-8"))
    doc["extra"] = "nope"
    with pytest.raises(ValidationError):
        validate(doc, "piece_brief")


def test_piece_brief_archetype_enum_matches_piece_label() -> None:
    pb = json.loads((schemas_dir() / "piece_brief.schema.json").read_text(encoding="utf-8"))
    pl = json.loads((schemas_dir() / "piece_label.schema.json").read_text(encoding="utf-8"))
    a = set(pb["$defs"]["editorial_archetype_id"]["enum"])
    b = set(pl["$defs"]["editorial_archetype_id"]["enum"])
    assert a == b


def test_build_stub_piece_brief_assigned_validates() -> None:
    doc = build_stub_piece_brief_assigned(
        run_id="2026-01-02T03-04-05Z__assigned__my-topic",
        topic="US payrolls",
        primary_archetype_id="data_dissection",
        ranked_retrieved_piece_ids=[],
    )
    validate(doc, "piece_brief")


def test_build_stub_piece_brief_without_archetype_validates() -> None:
    doc = build_stub_piece_brief_assigned(
        run_id="rid",
        topic="t",
        primary_archetype_id=None,
        ranked_retrieved_piece_ids=["piece_a", "piece_b"],
    )
    validate(doc, "piece_brief")
    assert "primary_archetype_id" not in doc
