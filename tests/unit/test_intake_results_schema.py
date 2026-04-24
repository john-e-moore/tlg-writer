"""inputs_result, source_reading_result, topic_selection_result schemas and stubs."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from tlg_writer.inputs_result import build_stub_inputs_result_assigned, build_stub_inputs_result_auto
from tlg_writer.json_schema import validate
from tlg_writer.paths import repo_root
from tlg_writer.source_reading_result import build_stub_source_reading_result_assigned
from tlg_writer.topic_selection_result import (
    build_stub_topic_selection_result_assigned_skipped,
    build_stub_topic_selection_result_auto_completed,
)


def _fixture(name: str) -> Path:
    return repo_root() / "tests" / "fixtures" / "pipeline" / name


def test_inputs_result_fixture_and_stub() -> None:
    doc = json.loads(_fixture("inputs_result_minimal.json").read_text(encoding="utf-8"))
    validate(doc, "inputs_result")
    stub = build_stub_inputs_result_assigned(run_id="2026-01-01T00-00-00Z__assigned__x", topic="T")
    validate(stub, "inputs_result")


def test_inputs_result_rejects_bad_mode() -> None:
    doc = build_stub_inputs_result_assigned(run_id="r", topic="t")
    doc["mode"] = "not_a_mode"
    with pytest.raises(ValidationError):
        validate(doc, "inputs_result")


def test_source_reading_result_fixture_and_stub() -> None:
    doc = json.loads(_fixture("source_reading_result_minimal.json").read_text(encoding="utf-8"))
    validate(doc, "source_reading_result")
    stub = build_stub_source_reading_result_assigned(run_id="2026-01-01T00-00-00Z__assigned__x", topic="T")
    validate(stub, "source_reading_result")


def test_topic_selection_result_fixture_and_stub() -> None:
    doc = json.loads(_fixture("topic_selection_result_minimal.json").read_text(encoding="utf-8"))
    validate(doc, "topic_selection_result")
    stub = build_stub_topic_selection_result_assigned_skipped(
        run_id="2026-01-01T00-00-00Z__assigned__x",
        topic="T",
    )
    validate(stub, "topic_selection_result")


def test_inputs_result_auto_stub_validates() -> None:
    doc = build_stub_inputs_result_auto(run_id="2026-01-01T00-00-00Z__auto__x", selected_topic_label="T")
    validate(doc, "inputs_result")


def test_topic_selection_result_completed_fixture_and_stub() -> None:
    doc = json.loads(
        _fixture("topic_selection_result_completed_minimal.json").read_text(encoding="utf-8")
    )
    validate(doc, "topic_selection_result")
    stub = build_stub_topic_selection_result_auto_completed(
        run_id="2026-01-01T00-00-00Z__auto__x",
        selected_topic_label="Chosen",
    )
    validate(stub, "topic_selection_result")


def test_topic_selection_result_rejects_wrong_skip_reason() -> None:
    doc = build_stub_topic_selection_result_assigned_skipped(run_id="r", topic="t")
    doc["skip_reason"] = "other"
    with pytest.raises(ValidationError):
        validate(doc, "topic_selection_result")
