"""Filesystem retrieval from piece_label directories."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tlg_writer.json_schema import validate
from tlg_writer.retrieval_result import (
    build_retrieval_result_from_labels_dir,
    build_stub_retrieval_result_assigned,
)


def test_build_retrieval_from_labels_dir_ranks_by_archetype(tmp_path: Path) -> None:
    (tmp_path / "a.json").write_text(
        json.dumps(
            {
                "piece_id": "z/last.docx",
                "schema_version": "v1",
                "labels": {
                    "basic_metadata": {},
                    "editorial": {"primary_archetype_id": "historical_analog"},
                    "voice": {},
                    "structural": {},
                    "quality": {},
                },
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "b.json").write_text(
        json.dumps(
            {
                "piece_id": "m/middle.docx",
                "schema_version": "v1",
                "labels": {
                    "basic_metadata": {},
                    "editorial": {
                        "primary_archetype_id": "scenario",
                        "alternate_archetype_ids": ["data_dissection"],
                    },
                    "voice": {},
                    "structural": {},
                    "quality": {},
                },
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "c.json").write_text(
        json.dumps(
            {
                "piece_id": "a/first.docx",
                "schema_version": "v1",
                "labels": {
                    "basic_metadata": {},
                    "editorial": {"primary_archetype_id": "data_dissection"},
                    "voice": {},
                    "structural": {},
                    "quality": {},
                },
            }
        ),
        encoding="utf-8",
    )
    doc = build_retrieval_result_from_labels_dir(
        run_id="rid",
        topic="t",
        framing_primary_archetype_id="data_dissection",
        labels_dir=tmp_path,
        max_hits=10,
    )
    validate(doc, "retrieval_result")
    assert [h["piece_reference"] for h in doc["ranked_hits"]] == [
        "a/first.docx",
        "m/middle.docx",
        "z/last.docx",
    ]


def test_build_retrieval_empty_dir_falls_back_to_stub(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    doc = build_retrieval_result_from_labels_dir(
        run_id="rid",
        topic="t",
        framing_primary_archetype_id="data_dissection",
        labels_dir=empty,
    )
    assert doc == build_stub_retrieval_result_assigned(run_id="rid", topic="t")


def test_build_retrieval_skips_invalid_json(tmp_path: Path) -> None:
    (tmp_path / "bad.json").write_text("{not json", encoding="utf-8")
    (tmp_path / "ok.json").write_text(
        json.dumps(
            {
                "piece_id": "ok.docx",
                "schema_version": "v1",
                "labels": {
                    "basic_metadata": {},
                    "editorial": {"primary_archetype_id": "data_dissection"},
                    "voice": {},
                    "structural": {},
                    "quality": {},
                },
            }
        ),
        encoding="utf-8",
    )
    doc = build_retrieval_result_from_labels_dir(
        run_id="rid",
        topic="t",
        framing_primary_archetype_id="data_dissection",
        labels_dir=tmp_path,
    )
    assert len(doc["ranked_hits"]) == 1
    assert doc["ranked_hits"][0]["piece_reference"] == "ok.docx"


def test_build_retrieval_recursive(tmp_path: Path) -> None:
    sub = tmp_path / "nested"
    sub.mkdir()
    (sub / "deep.json").write_text(
        json.dumps(
            {
                "piece_id": "deep.docx",
                "schema_version": "v1",
                "labels": {
                    "basic_metadata": {},
                    "editorial": {"primary_archetype_id": "data_dissection"},
                    "voice": {},
                    "structural": {},
                    "quality": {},
                },
            }
        ),
        encoding="utf-8",
    )
    flat = build_retrieval_result_from_labels_dir(
        run_id="rid",
        topic="t",
        framing_primary_archetype_id="data_dissection",
        labels_dir=tmp_path,
        recursive=False,
    )
    assert flat["ranked_hits"] == []
    deep = build_retrieval_result_from_labels_dir(
        run_id="rid",
        topic="t",
        framing_primary_archetype_id="data_dissection",
        labels_dir=tmp_path,
        recursive=True,
    )
    assert len(deep["ranked_hits"]) == 1
