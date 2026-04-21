"""JSON Schema contracts for corpus metadata, labels, and features."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from tlg_writer.json_schema import validate, validate_file
from tlg_writer.paths import repo_root


def _fixture(name: str) -> Path:
    return repo_root() / "tests" / "fixtures" / "corpus" / name


def test_minimal_piece_label_fixture() -> None:
    validate_file(_fixture("minimal_piece_label.json"), "piece_label")


def test_minimal_piece_features_fixture() -> None:
    validate_file(_fixture("minimal_piece_features.json"), "piece_features")


def test_pieces_metadata_batch_accepts_empty_list() -> None:
    validate([], "pieces_metadata_batch")


def test_pieces_metadata_batch_rejects_missing_body() -> None:
    bad = [
        {
            "source_path": "/x",
            "relative_to_repo": "data/x.docx",
            "filesystem": {"size_bytes": 1, "mtime_utc": "t"},
            "core": {},
            "app": {},
        }
    ]
    with pytest.raises(jsonschema.ValidationError):
        validate(bad, "pieces_metadata_batch")
