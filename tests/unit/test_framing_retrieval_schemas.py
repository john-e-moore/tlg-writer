"""framing_decision and retrieval_result JSON Schemas."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from tlg_writer.framing_decision import build_stub_framing_decision_assigned
from tlg_writer.json_schema import validate, validate_file
from tlg_writer.paths import repo_root, schemas_dir
from tlg_writer.retrieval_result import build_stub_retrieval_result_assigned, ranked_piece_references


def _fixture(name: str) -> Path:
    return repo_root() / "tests" / "fixtures" / "pipeline" / name


def test_framing_decision_minimal_fixture() -> None:
    validate_file(_fixture("framing_decision_minimal.json"), "framing_decision")


def test_retrieval_result_minimal_fixture() -> None:
    validate_file(_fixture("retrieval_result_minimal.json"), "retrieval_result")


def test_framing_decision_rejects_extra_keys() -> None:
    doc = json.loads(_fixture("framing_decision_minimal.json").read_text(encoding="utf-8"))
    doc["extra"] = "nope"
    with pytest.raises(ValidationError):
        validate(doc, "framing_decision")


def test_retrieval_result_rejects_extra_keys() -> None:
    doc = json.loads(_fixture("retrieval_result_minimal.json").read_text(encoding="utf-8"))
    doc["ranked_hits"][0]["extra_hit_field"] = "nope"
    with pytest.raises(ValidationError):
        validate(doc, "retrieval_result")


def test_framing_archetype_enum_matches_piece_label() -> None:
    fd = json.loads((schemas_dir() / "framing_decision.schema.json").read_text(encoding="utf-8"))
    pl = json.loads((schemas_dir() / "piece_label.schema.json").read_text(encoding="utf-8"))
    a = set(fd["$defs"]["editorial_archetype_id"]["enum"])
    b = set(pl["$defs"]["editorial_archetype_id"]["enum"])
    assert a == b


def test_retrieval_empty_hits_validates() -> None:
    doc = {
        "schema_version": "v1",
        "run_id": "rid",
        "rationale": "No archive wired.",
        "ranked_hits": [],
    }
    validate(doc, "retrieval_result")


def test_build_stub_framing_decision_validates() -> None:
    doc = build_stub_framing_decision_assigned(
        run_id="2026-01-02T03-04-05Z__assigned__my-topic",
        topic="US payrolls",
        primary_archetype_id="data_dissection",
    )
    validate(doc, "framing_decision")


def test_build_stub_retrieval_result_validates() -> None:
    doc = build_stub_retrieval_result_assigned(
        run_id="2026-01-02T03-04-05Z__assigned__my-topic",
        topic="US payrolls",
    )
    validate(doc, "retrieval_result")


def test_ranked_piece_references_sorts_by_rank() -> None:
    doc = {
        "schema_version": "v1",
        "run_id": "r",
        "rationale": "x",
        "ranked_hits": [
            {"rank": 2, "piece_reference": "b", "why_selected": "second"},
            {"rank": 1, "piece_reference": "a", "why_selected": "first"},
        ],
    }
    assert ranked_piece_references(doc) == ["a", "b"]
