"""Phase 0 skeleton: directory layout, manifest schema, assigned topic_selection skip."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from tlg_writer.json_schema import validate_file
from tlg_writer.layout import STAGE_DIRS
from tlg_writer.skeleton_pipeline import run_assigned_skeleton

# Mirrors `run_assigned_skeleton` output_schema routing (see `skeleton_pipeline._write_stage`).
_OUTPUT_SCHEMA_BY_STAGE: dict[str, str] = {
    "inputs": "skeleton_stage_output",
    "source_reading": "skeleton_stage_output",
    "topic_selection": "skeleton_stage_output",
    "framing": "framing_decision",
    "retrieval": "retrieval_result",
    "brief": "piece_brief",
    "drafting": "skeleton_stage_output",
    "critique": "critique_result",
    "revision": "revision_result",
    "evaluation": "evaluation_result",
    "final": "skeleton_stage_output",
}


def test_skeleton_run_layout_and_manifest(tmp_path: Path) -> None:
    when = datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)
    res = run_assigned_skeleton(
        topic="Test jobs report angle",
        slug="fixture-run",
        artifacts_root=tmp_path,
        when=when,
        run_id="2026-04-21T12-00-00Z__assigned__fixture-run",
    )
    root = res.run_dir
    assert root.is_dir()
    assert (root / "manifest.json").is_file()
    assert (root / "config.json").is_file()
    assert (root / "logs" / "run.log").is_file()

    for stage in STAGE_DIRS:
        d = root / stage
        assert d.is_dir()
        assert (d / "input.json").is_file()
        assert (d / "output.json").is_file()
        assert (d / "summary.md").is_file()
        assert (d / "metrics.json").is_file()

    validate_file(root / "manifest.json", "run_manifest")
    validate_file(root / "source_reading" / "output.json", "skeleton_stage_output")
    validate_file(root / "framing" / "output.json", "framing_decision")
    validate_file(root / "retrieval" / "output.json", "retrieval_result")
    validate_file(root / "brief" / "output.json", "piece_brief")
    validate_file(root / "critique" / "output.json", "critique_result")
    validate_file(root / "revision" / "output.json", "revision_result")
    validate_file(root / "evaluation" / "output.json", "evaluation_result")
    validate_file(root / "topic_selection" / "output.json", "skeleton_stage_output")
    validate_file(root / "inputs" / "metrics.json", "stage_metrics")

    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["stages_executed"] == list(STAGE_DIRS)
    for stage in STAGE_DIRS:
        assert manifest["artifact_index"][stage] == f"{stage}/"

    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
    assert config["mode"] == "assigned"
    assert set(config["models_by_stage"]) == set(STAGE_DIRS)

    ts = (root / "topic_selection" / "output.json").read_text(encoding="utf-8")
    assert "skipped" in ts
    assert "assigned" in ts.lower()

    piece = root / "final" / "piece.md"
    assert piece.is_file()
    body = piece.read_text(encoding="utf-8")
    assert "Phase 0 stub" in body
    assert "Thesis:" in body


def test_skeleton_refuses_existing_run_dir(tmp_path: Path) -> None:
    rid = "2026-04-21T12-00-00Z__assigned__collision"
    run_assigned_skeleton(
        topic="t",
        slug="collision",
        artifacts_root=tmp_path,
        run_id=rid,
    )
    with pytest.raises(FileExistsError):
        run_assigned_skeleton(
            topic="t",
            slug="collision",
            artifacts_root=tmp_path,
            run_id=rid,
        )


def test_skeleton_each_stage_output_and_metrics_are_schema_valid(tmp_path: Path) -> None:
    when = datetime(2026, 4, 21, 15, 0, 0, tzinfo=timezone.utc)
    res = run_assigned_skeleton(
        topic="Schema sweep topic",
        slug="schema-sweep",
        artifacts_root=tmp_path,
        when=when,
        run_id="2026-04-21T15-00-00Z__assigned__schema-sweep",
    )
    root = res.run_dir
    for stage in STAGE_DIRS:
        schema = _OUTPUT_SCHEMA_BY_STAGE[stage]
        validate_file(root / stage / "output.json", schema)
        validate_file(root / stage / "metrics.json", "stage_metrics")
        summary = (root / stage / "summary.md").read_text(encoding="utf-8")
        assert summary.strip()


def test_run_id_from_cli_slug_matches_pattern(tmp_path: Path) -> None:
    when = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    res = run_assigned_skeleton(
        topic="x",
        slug="my-topic",
        artifacts_root=tmp_path,
        when=when,
    )
    assert res.run_id == "2026-01-02T03-04-05Z__assigned__my-topic"
