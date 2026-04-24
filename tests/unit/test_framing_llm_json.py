"""Helpers for LLM-sourced framing JSON."""

from __future__ import annotations

import json

import pytest

from tlg_writer.framing_decision import extract_json_object_from_llm_text, normalize_framing_decision_from_llm


def test_extract_json_object_bare() -> None:
    obj = {"a": 1, "b": "x"}
    out = extract_json_object_from_llm_text(json.dumps(obj))
    assert out == obj


def test_extract_json_object_fenced() -> None:
    payload = {"schema_version": "v1", "run_id": "r1"}
    text = f"Here is the result:\n```json\n{json.dumps(payload)}\n```\n"
    out = extract_json_object_from_llm_text(text)
    assert out == payload


def test_extract_json_object_rejects_garbage() -> None:
    with pytest.raises(ValueError, match="no JSON object"):
        extract_json_object_from_llm_text("no braces here")


def test_normalize_framing_overrides_run_id() -> None:
    doc = {"schema_version": "v0", "run_id": "old", "primary_archetype_id": "scenario"}
    out = normalize_framing_decision_from_llm(doc, run_id="new-run")
    assert out["run_id"] == "new-run"
    assert out["schema_version"] == "v1"
