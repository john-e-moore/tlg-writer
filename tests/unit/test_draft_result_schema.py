"""draft_result JSON Schema and stub builder."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from tlg_writer.draft_result import build_stub_draft_result_assigned
from tlg_writer.json_schema import validate
from tlg_writer.paths import repo_root


def _fixture(name: str) -> Path:
    return repo_root() / "tests" / "fixtures" / "pipeline" / name


def test_draft_result_fixture_validates() -> None:
    doc = json.loads(_fixture("draft_result_minimal.json").read_text(encoding="utf-8"))
    validate(doc, "draft_result")


def test_build_stub_draft_result_validates() -> None:
    doc = build_stub_draft_result_assigned(
        run_id="2026-01-01T00-00-00Z__assigned__x",
        topic="t",
        thesis="A thesis.",
    )
    validate(doc, "draft_result")
    assert "Phase 0 stub draft" in doc["body_markdown"]


def test_draft_result_rejects_extra_top_level_key() -> None:
    doc = build_stub_draft_result_assigned(run_id="rid", topic="t", thesis="x")
    doc["extra"] = 1
    with pytest.raises(ValidationError):
        validate(doc, "draft_result")


def test_draft_result_rejects_empty_body() -> None:
    doc = build_stub_draft_result_assigned(run_id="rid", topic="t", thesis="x")
    doc["body_markdown"] = ""
    with pytest.raises(ValidationError):
        validate(doc, "draft_result")
