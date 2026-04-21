"""Corpus stub batch: metadata → labels/features + artifacts/runs manifest."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from tlg_writer.corpus_batch_stub import run_corpus_batch_stub
from tlg_writer.json_schema import validate
from tlg_writer.paths import repo_root


def test_corpus_batch_stub_end_to_end(tmp_path: Path) -> None:
    repo = repo_root()
    batch = repo / "tests" / "fixtures" / "corpus" / "minimal_metadata_batch.json"
    labels = tmp_path / "labeled"
    feats = tmp_path / "features"
    arts = tmp_path / "runs"
    when = datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)
    res = run_corpus_batch_stub(
        metadata_batch=batch,
        labels_dir=labels,
        features_dir=feats,
        artifacts_root=arts,
        slug="fixture-batch",
        when=when,
        run_id="2026-04-21T12-00-00Z__corpus__fixture-batch",
    )
    assert res.run_dir.name == res.run_id
    manifest_path = res.run_dir / "manifest.json"
    assert manifest_path.is_file()
    man = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate(man, "corpus_batch_manifest")
    assert man["counts"]["records_total"] == 1
    assert man["counts"]["labels_written"] == 1
    assert man["counts"]["skipped_with_errors"] == 0

    idx = man["artifact_index"]
    assert len(idx) == 1
    row = next(iter(idx.values()))

    def _resolve(p: str) -> Path:
        path = Path(p)
        return path if path.is_absolute() else repo / path

    label_path = _resolve(row["label_relpath"])
    feat_path = _resolve(row["feature_relpath"])
    assert label_path.is_file()
    assert feat_path.is_file()
    validate(json.loads(label_path.read_text(encoding="utf-8")), "piece_label")
    validate(json.loads(feat_path.read_text(encoding="utf-8")), "piece_features")

    assert (res.run_dir / "summary.md").is_file()
    assert (res.run_dir / "logs" / "run.log").is_file()
    run_log = (res.run_dir / "logs" / "run.log").read_text(encoding="utf-8")
    assert "run_id=" in run_log
    assert "ok:" in run_log
    assert str(batch) in run_log


def test_corpus_batch_stub_empty_batch_writes_valid_manifest(tmp_path: Path) -> None:
    batch = tmp_path / "empty_batch.json"
    batch.write_text("[]", encoding="utf-8")
    res = run_corpus_batch_stub(
        metadata_batch=batch,
        labels_dir=tmp_path / "l_empty",
        features_dir=tmp_path / "f_empty",
        artifacts_root=tmp_path / "r_empty",
        slug="empty-batch",
        when=datetime(2026, 4, 21, 16, 0, 0, tzinfo=timezone.utc),
        run_id="2026-04-21T16-00-00Z__corpus__empty-batch",
    )
    man = json.loads((res.run_dir / "manifest.json").read_text(encoding="utf-8"))
    validate(man, "corpus_batch_manifest")
    assert man["counts"]["records_total"] == 0
    assert man["counts"]["labels_written"] == 0
    assert man["counts"]["features_written"] == 0
    assert man["counts"]["skipped_with_errors"] == 0
    assert man["artifact_index"] == {}
    assert (res.run_dir / "logs" / "run.log").is_file()


def test_corpus_batch_stub_skips_error_rows(tmp_path: Path) -> None:
    repo = repo_root()
    batch = repo / "tests" / "fixtures" / "corpus" / "metadata_batch_with_error.json"
    res = run_corpus_batch_stub(
        metadata_batch=batch,
        labels_dir=tmp_path / "l",
        features_dir=tmp_path / "f",
        artifacts_root=tmp_path / "r",
        slug="skip-test",
        when=datetime(2026, 4, 21, 13, 0, 0, tzinfo=timezone.utc),
        run_id="2026-04-21T13-00-00Z__corpus__skip-test",
    )
    man = json.loads((res.run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert man["counts"]["records_total"] == 2
    assert man["counts"]["labels_written"] == 1
    assert man["counts"]["skipped_with_errors"] == 1
    assert len(man["artifact_index"]) == 1


def test_corpus_batch_stub_rejects_duplicate_run_dir(tmp_path: Path) -> None:
    repo = repo_root()
    batch = repo / "tests" / "fixtures" / "corpus" / "minimal_metadata_batch.json"
    kwargs = dict(
        metadata_batch=batch,
        labels_dir=tmp_path / "l2",
        features_dir=tmp_path / "f2",
        artifacts_root=tmp_path / "r2",
        slug="dup",
        run_id="2026-04-21T14-00-00Z__corpus__dup",
        when=datetime(2026, 4, 21, 14, 0, 0, tzinfo=timezone.utc),
    )
    run_corpus_batch_stub(**kwargs)

    with pytest.raises(FileExistsError):
        run_corpus_batch_stub(**kwargs)
