"""Phase 0 assigned-topic skeleton: full run tree with stub LLM stages."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tlg_writer.json_schema import validate
from tlg_writer.layout import STAGE_DIRS
from tlg_writer.paths import repo_root
from tlg_writer.run_id import build_run_id, normalize_slug


def _git_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root(),
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        return out.stdout.strip() or None
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _stage_metrics(stage: str) -> dict[str, Any]:
    return {
        "stage": stage,
        "model_id": "stub",
        "tokens_input": 0,
        "tokens_output": 0,
        "latency_ms": 0.0,
        "retries": 0,
        "validation": {"output_schema": "ok", "note": "Phase 0 skeleton; no provider calls."},
    }


def _validate_stage_bundle(stage: str, output_obj: dict[str, Any], metrics_obj: dict[str, Any]) -> None:
    validate(output_obj, "skeleton_stage_output")
    validate(metrics_obj, "stage_metrics")


def _write_stage(
    run_dir: Path,
    stage: str,
    input_obj: dict[str, Any],
    output_obj: dict[str, Any],
    summary_md: str,
) -> None:
    metrics_obj = _stage_metrics(stage)
    _validate_stage_bundle(stage, output_obj, metrics_obj)
    base = run_dir / stage
    _write_json(base / "input.json", input_obj)
    _write_json(base / "output.json", output_obj)
    _write_text(base / "summary.md", summary_md)
    _write_json(base / "metrics.json", metrics_obj)


@dataclass(frozen=True)
class AssignedSkeletonResult:
    run_dir: Path
    run_id: str


def run_assigned_skeleton(
    *,
    topic: str,
    slug: str,
    artifacts_root: Path,
    when: datetime | None = None,
    run_id: str | None = None,
) -> AssignedSkeletonResult:
    """
    Create `artifacts_root / <run_id>` with full stage layout (Phase 0).

    When ``run_id`` is set, it must match the documented id pattern; used for tests.
    """
    when = when or datetime.now(timezone.utc)
    if run_id is None:
        rid = build_run_id(when, "assigned", slug)
    else:
        rid = run_id
        normalize_slug(slug)  # validate slug shape even if id fixed

    run_dir = artifacts_root / rid
    if run_dir.exists():
        raise FileExistsError(f"run directory already exists: {run_dir}")

    run_dir.mkdir(parents=True)
    (run_dir / "logs").mkdir()
    _write_text(
        run_dir / "logs" / "run.log",
        f"run_id={rid}\nmode=assigned\nphase=0_skeleton\n",
    )

    for d in STAGE_DIRS:
        (run_dir / d).mkdir()

    created_at = when.astimezone(timezone.utc)
    iso = created_at.isoformat().replace("+00:00", "Z")

    # --- inputs (intake) ---
    inputs_in = {
        "schema_version": "0.1",
        "raw_topic": topic,
        "mode": "assigned",
    }
    inputs_out: dict[str, Any] = {
        "schema_version": "0.1",
        "stage": "inputs",
        "status": "completed",
        "message": "Normalized assigned-topic request (Phase 0 stub).",
        "payload": {"topic": topic, "mode": "assigned"},
    }
    _write_stage(
        run_dir,
        "inputs",
        inputs_in,
        inputs_out,
        summary_md=(
            "## inputs\n\n"
            "Recorded CLI topic for **assigned** mode. No auto-topic selection.\n"
        ),
    )

    prev = inputs_out["payload"]

    # --- source_reading ---
    src_out: dict[str, Any] = {
        "schema_version": "0.1",
        "stage": "source_reading",
        "status": "stub",
        "message": "Fixture-style source reading; no files ingested in Phase 0.",
        "payload": {"highlights": [], "claims": [], "topic_echo": prev.get("topic")},
    }
    _write_stage(
        run_dir,
        "source_reading",
        {"schema_version": "0.1", "upstream": "inputs", "topic": topic},
        src_out,
        "## source_reading\n\nStub stage. Operator should replace with real reader.\n",
    )

    # --- topic_selection (assigned: explicit skip) ---
    ts_out: dict[str, Any] = {
        "schema_version": "0.1",
        "stage": "topic_selection",
        "status": "skipped",
        "message": "assigned mode: topic provided by user; auto-topic selection did not run.",
        "payload": {"reason": "assigned_topic", "topic": topic},
    }
    _write_stage(
        run_dir,
        "topic_selection",
        {"schema_version": "0.1", "mode": "assigned"},
        ts_out,
        "## topic_selection\n\n**Skipped** for assigned mode (see `output.json`).\n",
    )

    # --- framing ---
    frame_out: dict[str, Any] = {
        "schema_version": "0.1",
        "stage": "framing",
        "status": "stub",
        "message": "Placeholder framing decision.",
        "payload": {"archetype": "data-dissection", "rationale": "Phase 0 placeholder only."},
    }
    _write_stage(
        run_dir,
        "framing",
        {"schema_version": "0.1", "source_reading": src_out["payload"]},
        frame_out,
        "## framing\n\nStub archetype selection for wiring tests.\n",
    )

    # --- retrieval ---
    retr_out: dict[str, Any] = {
        "schema_version": "0.1",
        "stage": "retrieval",
        "status": "stub",
        "message": "No archive query in Phase 0.",
        "payload": {"ranked_ids": []},
    }
    _write_stage(
        run_dir,
        "retrieval",
        {"schema_version": "0.1", "framing": frame_out["payload"]},
        retr_out,
        "## retrieval\n\nEmpty ranked set until archive hooks exist.\n",
    )

    # --- brief ---
    brief_out: dict[str, Any] = {
        "schema_version": "0.1",
        "stage": "brief",
        "status": "stub",
        "message": "Structured brief not yet modeled against piece_brief schema.",
        "payload": {"thesis": f"(stub) Develop an angle on: {topic}", "constraints": []},
    }
    _write_stage(
        run_dir,
        "brief",
        {"schema_version": "0.1", "retrieval": retr_out["payload"]},
        brief_out,
        "## brief\n\nMinimal stub brief object under `payload`.\n",
    )

    # --- drafting ---
    draft_body = (
        f"# (Phase 0 stub draft)\n\nTopic: **{topic}**.\n\n"
        "This text exists so `final/` has a readable precursor. "
        "It is not client-ready copy.\n"
    )
    draft_out: dict[str, Any] = {
        "schema_version": "0.1",
        "stage": "drafting",
        "status": "stub",
        "message": "Stub draft from skeleton pipeline.",
        "payload": {"markdown": draft_body},
    }
    _write_stage(
        run_dir,
        "drafting",
        {"schema_version": "0.1", "brief": brief_out["payload"]},
        draft_out,
        "## drafting\n\nStub markdown only.\n",
    )

    # --- critique ---
    crit_out: dict[str, Any] = {
        "schema_version": "0.1",
        "stage": "critique",
        "status": "stub",
        "message": "No rubric scoring in Phase 0.",
        "payload": {"notes": ["voice not evaluated", "macro not evaluated"]},
    }
    _write_stage(
        run_dir,
        "critique",
        {"schema_version": "0.1", "draft": draft_out["payload"]},
        crit_out,
        "## critique\n\nPlaceholder critic notes.\n",
    )

    # --- revision ---
    rev_out: dict[str, Any] = {
        "schema_version": "0.1",
        "stage": "revision",
        "status": "stub",
        "message": "Passthrough with cosmetic tweak for observability.",
        "payload": {"markdown": draft_body + "\n_Editorial revision pass: not performed (stub)._ \n"},
    }
    _write_stage(
        run_dir,
        "revision",
        {"schema_version": "0.1", "critique": crit_out["payload"], "draft": draft_out["payload"]},
        rev_out,
        "## revision\n\nStub revision; see `payload.markdown`.\n",
    )

    # --- evaluation ---
    eval_out: dict[str, Any] = {
        "schema_version": "0.1",
        "stage": "evaluation",
        "status": "stub",
        "message": "Pass/fail rubric not run.",
        "payload": {"recommendation": "human_review_required", "pass": False},
    }
    _write_stage(
        run_dir,
        "evaluation",
        {"schema_version": "0.1", "revision": rev_out["payload"]},
        eval_out,
        "## evaluation\n\nExplicit **human_review_required** (stub).\n",
    )

    # --- final (human-readable deliverable) ---
    piece_md = rev_out["payload"]["markdown"]
    final_out: dict[str, Any] = {
        "schema_version": "0.1",
        "stage": "final",
        "status": "completed",
        "message": "Packaged stub piece for Phase 0 acceptance (low quality by design).",
        "payload": {
            "format": "markdown",
            "body": piece_md,
            "limitations": [
                "All upstream stages are stubs or skipped.",
                "Not suitable for external distribution.",
            ],
        },
    }
    _write_stage(
        run_dir,
        "final",
        {"schema_version": "0.1", "evaluation": eval_out["payload"]},
        final_out,
        "## final\n\nDeliverable is intentionally weak; "
        "see `piece.md` and manifest `limitations`.\n",
    )
    _write_text(run_dir / "final" / "piece.md", piece_md)

    stages = list(STAGE_DIRS)
    stage_status = {s: "stub" for s in stages}
    stage_status["inputs"] = "completed"
    stage_status["topic_selection"] = "skipped"
    stage_status["final"] = "completed"

    artifact_index = {"manifest": "manifest.json", "config": "config.json", "logs": "logs/"}
    for s in stages:
        artifact_index[s] = f"{s}/"

    manifest: dict[str, Any] = {
        "schema_version": "0.1",
        "run_id": rid,
        "created_at": iso,
        "mode": "assigned",
        "topic": {"label": topic, "source": "cli"},
        "status": "completed",
        "stages_executed": stages,
        "stage_status": stage_status,
        "artifact_index": artifact_index,
        "pipeline_phases": {
            "note": "Phase 0 vertical slice: stubs/mocks only; see `.agent/SPEC.md` §18.",
        },
        "limitations": [
            "No live LLM calls.",
            "Schemas for piece_brief, critique, evaluation not yet wired.",
        ],
    }
    gc = _git_commit()
    if gc:
        manifest["git_commit"] = gc
    validate(manifest, "run_manifest")
    _write_json(run_dir / "manifest.json", manifest)

    config = {
        "schema_version": "0.1",
        "mode": "assigned",
        "models_by_stage": {s: "stub" for s in stages},
        "prompts": "see prompts/<stage>/ on disk (placeholders in Phase 0)",
    }
    _write_json(run_dir / "config.json", config)

    return AssignedSkeletonResult(run_dir=run_dir, run_id=rid)
