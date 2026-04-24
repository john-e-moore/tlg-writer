"""Phase 0 editorial skeleton: full run tree with stub LLM stages (assigned and auto)."""

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
from tlg_writer.final_deliverable import build_stub_final_deliverable_assigned
from tlg_writer.framing_decision import build_stub_framing_decision_assigned
from tlg_writer.inputs_result import build_stub_inputs_result_assigned, build_stub_inputs_result_auto
from tlg_writer.json_schema import validate
from tlg_writer.layout import STAGE_DIRS
from tlg_writer.paths import repo_root
from tlg_writer.piece_brief import build_stub_piece_brief_assigned
from tlg_writer.retrieval_result import (
    build_stub_retrieval_result_assigned,
    ranked_piece_references,
)
from tlg_writer.revision_result import build_stub_revision_result_assigned
from tlg_writer.run_id import build_run_id, normalize_slug
from tlg_writer.source_reading_result import build_stub_source_reading_result_assigned
from tlg_writer.stage_schemas import output_json_schema_for_stage, validate_pipeline_stage_output
from tlg_writer.topic_selection_result import (
    build_stub_topic_selection_result_assigned_skipped,
    build_stub_topic_selection_result_auto_completed,
)


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


DEFAULT_AUTO_TOPIC_LABEL = "Phase 0 auto-topic stub (global macro themes)"


@dataclass(frozen=True)
class AssignedSkeletonResult:
    run_dir: Path
    run_id: str


def _execute_phase0_run(
    *,
    rid: str,
    artifacts_root: Path,
    when: datetime,
    run_log_mode_tag: str,
    manifest_mode: str,
    manifest_topic: dict[str, str],
    config_mode: str,
    content_topic: str,
    inputs_in: dict[str, Any],
    inputs_doc: dict[str, Any],
    inputs_summary_md: str,
    ts_doc: dict[str, Any],
    topic_selection_summary_md: str,
    stage_status_topic_selection: str,
) -> AssignedSkeletonResult:
    run_dir = artifacts_root / rid
    if run_dir.exists():
        raise FileExistsError(f"run directory already exists: {run_dir}")

    run_dir.mkdir(parents=True)
    (run_dir / "logs").mkdir()
    _write_text(
        run_dir / "logs" / "run.log",
        f"run_id={rid}\nmode={run_log_mode_tag}\nphase=0_skeleton\n",
    )

    for d in STAGE_DIRS:
        (run_dir / d).mkdir()

    created_at = when.astimezone(timezone.utc)
    iso = created_at.isoformat().replace("+00:00", "Z")

    validate_pipeline_stage_output("inputs", inputs_doc)
    _write_stage(
        run_dir,
        "inputs",
        inputs_in,
        inputs_doc,
        summary_md=inputs_summary_md,
        output_schema=output_json_schema_for_stage("inputs"),
    )

    source_doc = build_stub_source_reading_result_assigned(run_id=rid, topic=content_topic)
    validate_pipeline_stage_output("source_reading", source_doc)
    _write_stage(
        run_dir,
        "source_reading",
        {"schema_version": "0.1", "inputs_result": inputs_doc, "topic": content_topic},
        source_doc,
        "## source_reading\n\nStructured **source_reading_result**; "
        "Phase 0 stub (no files ingested).\n",
        output_schema=output_json_schema_for_stage("source_reading"),
    )

    validate_pipeline_stage_output("topic_selection", ts_doc)
    _write_stage(
        run_dir,
        "topic_selection",
        {
            "schema_version": "0.1",
            "inputs_result": inputs_doc,
            "source_reading_result": source_doc,
        },
        ts_doc,
        summary_md=topic_selection_summary_md,
        output_schema=output_json_schema_for_stage("topic_selection"),
    )

    framing_doc = build_stub_framing_decision_assigned(
        run_id=rid,
        topic=content_topic,
        primary_archetype_id="data_dissection",
    )
    validate_pipeline_stage_output("framing", framing_doc)
    _write_stage(
        run_dir,
        "framing",
        {
            "schema_version": "0.1",
            "source_reading_result": source_doc,
            "topic_selection_result": ts_doc,
        },
        framing_doc,
        "## framing\n\nStructured **framing_decision** (`schemas/json/framing_decision.schema.json`); "
        "stub content pending real framing stage.\n",
        output_schema=output_json_schema_for_stage("framing"),
    )

    retr_doc = build_stub_retrieval_result_assigned(run_id=rid, topic=content_topic)
    validate_pipeline_stage_output("retrieval", retr_doc)
    _write_stage(
        run_dir,
        "retrieval",
        {"schema_version": "0.1", "framing_decision": framing_doc},
        retr_doc,
        "## retrieval\n\nStructured **retrieval_result** (`schemas/json/retrieval_result.schema.json`); "
        "empty ranked_hits until archive hooks exist.\n",
        output_schema=output_json_schema_for_stage("retrieval"),
    )

    arch_id = str(framing_doc["primary_archetype_id"])
    brief_doc = build_stub_piece_brief_assigned(
        run_id=rid,
        topic=content_topic,
        primary_archetype_id=arch_id,
        ranked_retrieved_piece_ids=ranked_piece_references(retr_doc),
    )
    validate_pipeline_stage_output("brief", brief_doc)
    _write_stage(
        run_dir,
        "brief",
        {
            "schema_version": "0.1",
            "topic": content_topic,
            "framing_decision": framing_doc,
            "retrieval_result": retr_doc,
        },
        brief_doc,
        "## brief\n\nStructured **piece_brief** (`schemas/json/piece_brief.schema.json`); "
        "content is still stub-quality pending real brief builder.\n",
        output_schema=output_json_schema_for_stage("brief"),
    )

    draft_doc = build_stub_draft_result_assigned(
        run_id=rid,
        topic=content_topic,
        thesis=str(brief_doc["thesis"]),
    )
    validate_pipeline_stage_output("drafting", draft_doc)
    _write_stage(
        run_dir,
        "drafting",
        {"schema_version": "0.1", "piece_brief": brief_doc},
        draft_doc,
        "## drafting\n\nStructured **draft_result** (`schemas/json/draft_result.schema.json`); "
        "stub prose only.\n",
        output_schema=output_json_schema_for_stage("drafting"),
    )

    critique_doc = build_stub_critique_result_assigned(run_id=rid)
    validate_pipeline_stage_output("critique", critique_doc)
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
        output_schema=output_json_schema_for_stage("critique"),
    )

    revision_doc = build_stub_revision_result_assigned(
        run_id=rid,
        draft_markdown=draft_doc["body_markdown"],
    )
    validate_pipeline_stage_output("revision", revision_doc)
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
        output_schema=output_json_schema_for_stage("revision"),
    )

    evaluation_doc = build_stub_evaluation_result_assigned(run_id=rid)
    validate_pipeline_stage_output("evaluation", evaluation_doc)
    _write_stage(
        run_dir,
        "evaluation",
        {"schema_version": "0.1", "revision_result": revision_doc},
        evaluation_doc,
        "## evaluation\n\nStructured **evaluation_result** (`schemas/json/evaluation_result.schema.json`); "
        "explicit **human_review_required** until a real evaluator runs.\n",
        output_schema=output_json_schema_for_stage("evaluation"),
    )

    piece_md = revision_doc["revised_markdown"]
    final_doc = build_stub_final_deliverable_assigned(
        run_id=rid,
        body_markdown=piece_md,
    )
    validate_pipeline_stage_output("final", final_doc)
    _write_stage(
        run_dir,
        "final",
        {"schema_version": "0.1", "evaluation_result": evaluation_doc},
        final_doc,
        "## final\n\nStructured **final_deliverable** (`schemas/json/final_deliverable.schema.json`); "
        "`piece.md` mirrors `body_markdown`.\n",
        output_schema=output_json_schema_for_stage("final"),
    )
    _write_text(run_dir / "final" / "piece.md", piece_md)

    stages = list(STAGE_DIRS)
    stage_status = {s: "stub" for s in stages}
    stage_status["inputs"] = "completed"
    stage_status["topic_selection"] = stage_status_topic_selection
    stage_status["final"] = "completed"

    artifact_index = {"manifest": "manifest.json", "config": "config.json", "logs": "logs/"}
    for s in stages:
        artifact_index[s] = f"{s}/"

    manifest: dict[str, Any] = {
        "schema_version": "0.1",
        "run_id": rid,
        "created_at": iso,
        "mode": manifest_mode,
        "topic": manifest_topic,
        "status": "completed",
        "stages_executed": stages,
        "stage_status": stage_status,
        "artifact_index": artifact_index,
        "pipeline_phases": {
            "note": "Phase 0 vertical slice: stubs/mocks only; see `.agent/SPEC.md` §18.",
        },
        "limitations": [
            "No live LLM calls.",
            "All stage output.json files validate against v1 JSON Schemas (including intake); "
            "content remains stub-quality until real agents are wired.",
        ],
    }
    gc = _git_commit()
    if gc:
        manifest["git_commit"] = gc
    validate(manifest, "run_manifest")
    _write_json(run_dir / "manifest.json", manifest)

    config = {
        "schema_version": "0.1",
        "mode": config_mode,
        "models_by_stage": {s: "stub" for s in stages},
        "prompts": "see prompts/<stage>/ on disk (placeholders in Phase 0)",
    }
    _write_json(run_dir / "config.json", config)

    return AssignedSkeletonResult(run_dir=run_dir, run_id=rid)


def run_assigned_skeleton(
    *,
    topic: str,
    slug: str,
    artifacts_root: Path,
    when: datetime | None = None,
    run_id: str | None = None,
) -> AssignedSkeletonResult:
    """
    Create `artifacts_root / <run_id>` with full stage layout (Phase 0, **assigned**).

    When ``run_id`` is set, it must match the documented id pattern; used for tests.
    """
    when = when or datetime.now(timezone.utc)
    if run_id is None:
        rid = build_run_id(when, "assigned", slug)
    else:
        rid = run_id
        normalize_slug(slug)

    inputs_doc = build_stub_inputs_result_assigned(run_id=rid, topic=topic)
    return _execute_phase0_run(
        rid=rid,
        artifacts_root=artifacts_root,
        when=when,
        run_log_mode_tag="assigned",
        manifest_mode="assigned",
        manifest_topic={"label": topic, "source": "cli"},
        config_mode="assigned",
        content_topic=topic,
        inputs_in={"schema_version": "0.1", "raw_topic": topic, "mode": "assigned"},
        inputs_doc=inputs_doc,
        inputs_summary_md=(
            "## inputs\n\n"
            "Recorded CLI topic for **assigned** mode. No auto-topic selection.\n"
        ),
        ts_doc=build_stub_topic_selection_result_assigned_skipped(run_id=rid, topic=topic),
        topic_selection_summary_md=(
            "## topic_selection\n\n**Skipped** for assigned mode (see `output.json`).\n"
        ),
        stage_status_topic_selection="skipped",
    )


def run_auto_skeleton(
    *,
    slug: str,
    artifacts_root: Path,
    when: datetime | None = None,
    run_id: str | None = None,
    topic: str | None = None,
) -> AssignedSkeletonResult:
    """
    Create `artifacts_root / <run_id>` with full stage layout (Phase 0, **auto** stub).

    Uses ``build_run_id(..., "auto", slug)``. Topic label is ``topic`` when provided,
    otherwise :data:`DEFAULT_AUTO_TOPIC_LABEL`. No live topic search.
    """
    when = when or datetime.now(timezone.utc)
    if run_id is None:
        rid = build_run_id(when, "auto", slug)
    else:
        rid = run_id
        normalize_slug(slug)

    label = topic if topic else DEFAULT_AUTO_TOPIC_LABEL
    inputs_doc = build_stub_inputs_result_auto(run_id=rid, selected_topic_label=label)
    return _execute_phase0_run(
        rid=rid,
        artifacts_root=artifacts_root,
        when=when,
        run_log_mode_tag="auto",
        manifest_mode="auto",
        manifest_topic={"label": label, "source": "auto_pipeline"},
        config_mode="auto",
        content_topic=label,
        inputs_in={"schema_version": "0.1", "raw_topic": label, "mode": "auto"},
        inputs_doc=inputs_doc,
        inputs_summary_md=(
            "## inputs\n\n**Auto** mode (Phase 0 stub); topic label is template-filled.\n"
        ),
        ts_doc=build_stub_topic_selection_result_auto_completed(
            run_id=rid,
            selected_topic_label=label,
        ),
        topic_selection_summary_md=(
            "## topic_selection\n\nPhase 0 **auto** stub: completed with deterministic label "
            "(no search).\n"
        ),
        stage_status_topic_selection="completed",
    )
