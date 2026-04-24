"""final_deliverable JSON Schema and stub builder."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from tlg_writer.final_deliverable import build_stub_final_deliverable_assigned
from tlg_writer.json_schema import validate
from tlg_writer.paths import repo_root


def _fixture(name: str) -> Path:
    return repo_root() / "tests" / "fixtures" / "pipeline" / name


def test_final_deliverable_fixture_validates() -> None:
    doc = json.loads(_fixture("final_deliverable_minimal.json").read_text(encoding="utf-8"))
    validate(doc, "final_deliverable")


def test_build_stub_final_deliverable_validates() -> None:
    doc = build_stub_final_deliverable_assigned(
        run_id="2026-01-01T00-00-00Z__assigned__x",
        body_markdown="# Hello\n",
    )
    validate(doc, "final_deliverable")
    assert doc["format"] == "markdown"


def test_final_deliverable_rejects_extra_top_level_key() -> None:
    doc = build_stub_final_deliverable_assigned(run_id="rid", body_markdown="x")
    doc["extra"] = 1
    with pytest.raises(ValidationError):
        validate(doc, "final_deliverable")


def test_final_deliverable_rejects_wrong_format() -> None:
    doc = build_stub_final_deliverable_assigned(run_id="rid", body_markdown="x")
    doc["format"] = "html"
    with pytest.raises(ValidationError):
        validate(doc, "final_deliverable")
