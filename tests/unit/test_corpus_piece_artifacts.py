"""Tests for corpus piece JSON directory validation."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tlg_writer.corpus_piece_artifacts import iter_json_files, validate_corpus_json_files
from tlg_writer.paths import repo_root


def test_iter_json_files_non_recursive(tmp_path: Path) -> None:
    (tmp_path / "a.json").write_text("{}", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.json").write_text("{}", encoding="utf-8")
    names = {p.name for p in iter_json_files(tmp_path, recursive=False)}
    assert names == {"a.json"}


def test_iter_json_files_recursive(tmp_path: Path) -> None:
    (tmp_path / "a.json").write_text("{}", encoding="utf-8")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "b.json").write_text("{}", encoding="utf-8")
    names = {p.name for p in iter_json_files(tmp_path, recursive=True)}
    assert names == {"a.json", "b.json"}


def test_iter_json_files_not_a_directory(tmp_path: Path) -> None:
    f = tmp_path / "nope.txt"
    f.write_text("x", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        list(iter_json_files(f, recursive=False))


def test_validate_labels_ok_minimal_fixture(tmp_path: Path) -> None:
    src = repo_root() / "tests/fixtures/corpus/minimal_piece_label.json"
    dst = tmp_path / "piece_x.json"
    dst.write_bytes(src.read_bytes())
    assert validate_corpus_json_files(tmp_path, kind="labels") == []


def test_validate_labels_bad_missing_required(tmp_path: Path) -> None:
    (tmp_path / "bad.json").write_text(json.dumps({"schema_version": "v1"}), encoding="utf-8")
    failures = validate_corpus_json_files(tmp_path, kind="labels")
    assert len(failures) == 1
    assert failures[0][0].name == "bad.json"
    assert "schema piece_label" in failures[0][1]


def test_validate_features_malformed_json(tmp_path: Path) -> None:
    (tmp_path / "broken.json").write_text("{", encoding="utf-8")
    failures = validate_corpus_json_files(tmp_path, kind="features")
    assert len(failures) == 1
    assert "invalid JSON" in failures[0][1]


def test_validate_kind_invalid(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="kind"):
        validate_corpus_json_files(tmp_path, kind="nope")  # type: ignore[arg-type]


def test_validate_corpus_piece_json_script_smoke(tmp_path: Path) -> None:
    src = repo_root() / "tests/fixtures/corpus/minimal_piece_label.json"
    shutil.copy(src, tmp_path / "piece_smoke.json")
    script = repo_root() / "scripts" / "validate_corpus_piece_json.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--labels-dir", str(tmp_path)],
        cwd=repo_root(),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "ok labels" in proc.stdout
