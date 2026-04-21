"""evaluation_result JSON Schema and stub builder."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from tlg_writer.evaluation_result import build_stub_evaluation_result_assigned
from tlg_writer.json_schema import validate
from tlg_writer.paths import repo_root


def _fixture(name: str) -> Path:
    return repo_root() / "tests" / "fixtures" / "pipeline" / name


def test_evaluation_result_fixture_validates() -> None:
    doc = json.loads(_fixture("evaluation_result_minimal.json").read_text(encoding="utf-8"))
    validate(doc, "evaluation_result")


def test_build_stub_evaluation_result_validates() -> None:
    doc = build_stub_evaluation_result_assigned(run_id="2026-01-01T00-00-00Z__assigned__x")
    validate(doc, "evaluation_result")
    assert doc["recommendation"] == "human_review_required"
    assert doc["pass"] is False


def test_evaluation_result_rejects_extra_top_level_key() -> None:
    doc = build_stub_evaluation_result_assigned(run_id="rid")
    doc["extra"] = 1
    with pytest.raises(ValidationError):
        validate(doc, "evaluation_result")


def test_evaluation_result_rejects_bad_recommendation() -> None:
    doc = build_stub_evaluation_result_assigned(run_id="rid")
    doc["recommendation"] = "maybe"
    with pytest.raises(ValidationError):
        validate(doc, "evaluation_result")
