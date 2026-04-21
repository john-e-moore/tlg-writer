"""revision_result JSON Schema and stub builder."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from tlg_writer.json_schema import validate
from tlg_writer.paths import repo_root
from tlg_writer.revision_result import build_stub_revision_result_assigned


def _fixture(name: str) -> Path:
    return repo_root() / "tests" / "fixtures" / "pipeline" / name


def test_revision_result_fixture_validates() -> None:
    doc = json.loads(_fixture("revision_result_minimal.json").read_text(encoding="utf-8"))
    validate(doc, "revision_result")


def test_build_stub_revision_result_validates() -> None:
    doc = build_stub_revision_result_assigned(
        run_id="2026-01-01T00-00-00Z__assigned__x",
        draft_markdown="# Draft\n\nHello.",
    )
    validate(doc, "revision_result")
    assert "_Editorial revision pass: not performed (stub)._" in doc["revised_markdown"]


def test_revision_result_rejects_extra_top_level_key() -> None:
    doc = build_stub_revision_result_assigned(run_id="rid", draft_markdown="x")
    doc["extra"] = 1
    with pytest.raises(ValidationError):
        validate(doc, "revision_result")


def test_revision_result_rejects_empty_revised_markdown() -> None:
    doc = build_stub_revision_result_assigned(run_id="rid", draft_markdown="x")
    doc["revised_markdown"] = ""
    with pytest.raises(ValidationError):
        validate(doc, "revision_result")
