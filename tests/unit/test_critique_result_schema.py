"""critique_result JSON Schema and stub builder."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from tlg_writer.critique_result import build_stub_critique_result_assigned
from tlg_writer.json_schema import validate
from tlg_writer.paths import repo_root


def _fixture(name: str) -> Path:
    return repo_root() / "tests" / "fixtures" / "pipeline" / name


def test_critique_result_fixture_validates() -> None:
    doc = json.loads(_fixture("critique_result_minimal.json").read_text(encoding="utf-8"))
    validate(doc, "critique_result")


def test_build_stub_critique_result_validates() -> None:
    doc = build_stub_critique_result_assigned(run_id="2026-01-01T00-00-00Z__assigned__x")
    validate(doc, "critique_result")


def test_critique_result_rejects_extra_top_level_key() -> None:
    doc = build_stub_critique_result_assigned(run_id="rid")
    doc["extra"] = 1
    with pytest.raises(ValidationError):
        validate(doc, "critique_result")


def test_critique_result_rejects_score_out_of_range() -> None:
    doc = build_stub_critique_result_assigned(run_id="rid")
    doc["rubric_scores"] = {**doc["rubric_scores"], "voice_match": 1.5}
    with pytest.raises(ValidationError):
        validate(doc, "critique_result")
