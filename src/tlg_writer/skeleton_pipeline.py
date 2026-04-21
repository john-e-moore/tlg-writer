"""Phase 0 assigned-topic skeleton: full run tree with stub LLM stages."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tlg_writer.critique_result import build_stub_critique_result_assigned
from tlg_writer.draft_result import build_stub_draft_result_assigned
from tlg_writer.evaluation_result import build_stub_evaluation_result_assigned
from tlg_writer.revision_result import build_stub_revision_result_assigned
from tlg_writer.framing_decision import build_stub_framing_decision_assigned
from tlg_writer.json_schema import validate
from tlg_writer.layout import STAGE_DIRS
from tlg_writer.paths import repo_root
from tlg_writer.piece_brief import build_stub_piece_brief_assigned
from tlg_writer.retrieval_result import (
    build_stub_retrieval_result_assigned,
    ranked_piece_references,
)
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


def _validate_stage_bundle(
    stage: str,
    output_obj: dict[str, Any],
    metrics_obj: dict[str, Any],
    *,
    output_schema: str = "skeleton_stage_output",
) -> None:
    validate(output_obj, output_schema)
    validate(metrics_obj, "stage_metrics")


def _write_stage(
    run_dir: Path,
    stage: str,
    input_obj: dict[str, Any],
    output_obj: dict[str, Any],
    summary_md: str,
    *,
    output_schema: str = "skeleton_stage_output",
) -> None:
    metrics_obj = _stage_metrics(stage)
    _validate_stage_bundle(stage, output_obj, metrics_obj, output_schema=output_schema)
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

    # --- framing (canonical framing_decision on output.json) ---
    framing_doc = build_stub_framing_decision_assigned(
        run_id=rid,
        topic=topic,
        primary_archetype_id="data_dissection",
    )
    validate(framing_doc, "framing_decision")
    _write_stage(
        run_dir,
        "framing",
        {"schema_version": "0.1", "source_reading": src_out["payload"]},
        framing_doc,
        "## framing\n\nStructured **framing_decision** (`schemas/json/framing_decision.schema.json`); "
        "stub content pending real framing stage.\n",
        output_schema="framing_decision",
    )

    # --- retrieval (canonical retrieval_result on output.json) ---
    retr_doc = build_stub_retrieval_result_assigned(run_id=rid, topic=topic)
    validate(retr_doc, "retrieval_result")
    _write_stage(
        run_dir,
        "retrieval",
        {"schema_version": "0.1", "framing_decision": framing_doc},
        retr_doc,
        "## retrieval\n\nStructured **retrieval_result** (`schemas/json/retrieval_result.schema.json`); "
        "empty ranked_hits until archive hooks exist.\n",
        output_schema="retrieval_result",
    )

    # --- brief (canonical piece_brief on output.json) ---
    arch_id = str(framing_doc["primary_archetype_id"])
    brief_doc = build_stub_piece_brief_assigned(
        run_id=rid,
        topic=topic,
        primary_archetype_id=arch_id,
        ranked_retrieved_piece_ids=ranked_piece_references(retr_doc),
    )
    validate(brief_doc, "piece_brief")
    _write_stage(
        run_dir,
        "brief",
        {
            "schema_version": "0.1",
            "topic": topic,
            "framing_decision": framing_doc,
            "retrieval_result": retr_doc,
        },
        brief_doc,
        "## brief\n\nStructured **piece_brief** (`schemas/json/piece_brief.schema.json`); "
        "content is still stub-quality pending real brief builder.\n",
        output_schema="piece_brief",
    )

    # --- drafting (canonical draft_result on output.json) ---
    draft_doc = build_stub_draft_result_assigned(
        run_id=rid,
        topic=topic,
        thesis=str(brief_doc["thesis"]),
    )
    validate(draft_doc, "draft_result")
    _write_stage(
        run_dir,
        "drafting",
        {"schema_version": "0.1", "piece_brief": brief_doc},
        draft_doc,
        "## drafting\n\nStructured **draft_result** (`schemas/json/draft_result.schema.json`); "
        "stub prose only.\n",
        output_schema="draft_result",
    )

    # --- critique (canonical critique_result on output.json) ---
    critique_doc = build_stub_critique_result_assigned(run_id=rid)
    validate(critique_doc, "critique_result")
    _write_stage(
        run_dir,
        "critique",
        {
            "schema_version": "0.1",
            "piece_brief": brief_doc,
            "draft_result": draft_doc,
        },
        critique_doc,
        "## critique\n\nStructured **critique_result** (`schemas/json/critique_result.schema.json`); "
        "null rubric scores until real critics run.\n",
        output_schema="critique_result",
    )

    # --- revision (canonical revision_result on output.json) ---
    revision_doc = build_stub_revision_result_assigned(
        run_id=rid,
        draft_markdown=draft_doc["body_markdown"],
    )
    validate(revision_doc, "revision_result")
    _write_stage(
        run_dir,
        "revision",
        {
            "schema_version": "0.1",
            "critique_result": critique_doc,
            "draft_result": draft_doc,
        },
        revision_doc,
        "## revision\n\nStructured **revision_result** (`schemas/json/revision_result.schema.json`); "
        "stub pass appends a single cosmetic line.\n",
        output_schema="revision_result",
    )

    # --- evaluation (canonical evaluation_result on output.json) ---
    evaluation_doc = build_stub_evaluation_result_assigned(run_id=rid)
    validate(evaluation_doc, "evaluation_result")
    _write_stage(
        run_dir,
        "evaluation",
        {"schema_version": "0.1", "revision_result": revision_doc},
        evaluation_doc,
        "## evaluation\n\nStructured **evaluation_result** (`schemas/json/evaluation_result.schema.json`); "
        "explicit **human_review_required** until a real evaluator runs.\n",
        output_schema="evaluation_result",
    )

    # --- final (human-readable deliverable) ---
    piece_md = revision_doc["revised_markdown"]
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
        {"schema_version": "0.1", "evaluation_result": evaluation_doc},
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
            "Stages from framing/ through evaluation/ emit v1 domain JSON; "
            "inputs/, source_reading/, topic_selection/, and final/ remain Phase 0 generic stubs.",
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
