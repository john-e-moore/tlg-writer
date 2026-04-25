"""Phase 0 skeleton: directory layout, manifest schema, assigned topic_selection skip."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from tlg_writer.json_schema import validate_file
from tlg_writer.layout import STAGE_DIRS
from tlg_writer.llm_client import ChatCompletionResult, StubLLMClient
from tlg_writer.skeleton_pipeline import run_assigned_skeleton, run_auto_skeleton
from tlg_writer.stage_schemas import OUTPUT_SCHEMA_BY_STAGE


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
    validate_file(root / "inputs" / "output.json", "inputs_result")
    validate_file(root / "source_reading" / "output.json", "source_reading_result")
    validate_file(root / "framing" / "output.json", "framing_decision")
    validate_file(root / "retrieval" / "output.json", "retrieval_result")
    validate_file(root / "brief" / "output.json", "piece_brief")
    validate_file(root / "critique" / "output.json", "critique_result")
    validate_file(root / "revision" / "output.json", "revision_result")
    validate_file(root / "evaluation" / "output.json", "evaluation_result")
    validate_file(root / "drafting" / "output.json", "draft_result")
    validate_file(root / "final" / "output.json", "final_deliverable")
    validate_file(root / "topic_selection" / "output.json", "topic_selection_result")
    validate_file(root / "inputs" / "metrics.json", "stage_metrics")

    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["stages_executed"] == list(STAGE_DIRS)
    for stage in STAGE_DIRS:
        assert manifest["artifact_index"][stage] == f"{stage}/"

    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
    assert config["mode"] == "assigned"
    assert set(config["models_by_stage"]) == set(STAGE_DIRS)
    assert config["llm_client_probe"]["model"] == "phase0-probe"
    run_log = (root / "logs" / "run.log").read_text(encoding="utf-8")
    assert "llm_probe_model=phase0-probe" in run_log
    metrics0 = json.loads((root / "inputs" / "metrics.json").read_text(encoding="utf-8"))
    assert metrics0["llm"]["phase0_client_probe"]["model"] == "phase0-probe"

    ts = (root / "topic_selection" / "output.json").read_text(encoding="utf-8")
    assert "skipped" in ts
    assert "assigned" in ts.lower()

    piece = root / "final" / "piece.md"
    assert piece.is_file()
    body = piece.read_text(encoding="utf-8")
    assert "Phase 0 stub" in body
    assert "Thesis:" in body
    final_json = json.loads((root / "final" / "output.json").read_text(encoding="utf-8"))
    assert final_json["body_markdown"] == body


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
        schema = OUTPUT_SCHEMA_BY_STAGE[stage]
        validate_file(root / stage / "output.json", schema)
        validate_file(root / stage / "metrics.json", "stage_metrics")
        summary = (root / stage / "summary.md").read_text(encoding="utf-8")
        assert summary.strip()


def test_skeleton_llm_probe_uses_injected_client_once(tmp_path: Path) -> None:
    calls: list[str] = []

    class TraceStub(StubLLMClient):
        def complete_chat(self, **kwargs):  # type: ignore[no-untyped-def]
            calls.append("ping")
            return super().complete_chat(**kwargs)

    res = run_assigned_skeleton(
        topic="t",
        slug="llm-trace",
        artifacts_root=tmp_path,
        run_id="2026-04-21T12-00-00Z__assigned__llm-trace",
        llm_client=TraceStub(),
    )
    assert calls == ["ping"]
    cfg = json.loads((res.run_dir / "config.json").read_text(encoding="utf-8"))
    assert cfg["llm_client_probe"]["model"] == "phase0-probe"


def test_auto_skeleton_run_layout_manifest_and_topic_selection_completed(tmp_path: Path) -> None:
    when = datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)
    res = run_auto_skeleton(
        slug="fixture-auto",
        artifacts_root=tmp_path,
        when=when,
        run_id="2026-04-21T12-00-00Z__auto__fixture-auto",
        topic="Stub-selected macro angle",
    )
    root = res.run_dir
    assert "__auto__" in res.run_id
    validate_file(root / "manifest.json", "run_manifest")
    validate_file(root / "inputs" / "output.json", "inputs_result")
    validate_file(root / "topic_selection" / "output.json", "topic_selection_result")

    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["mode"] == "auto"

    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
    assert config["mode"] == "auto"

    ts = json.loads((root / "topic_selection" / "output.json").read_text(encoding="utf-8"))
    assert ts["selection_status"] == "completed"
    assert ts["selected_topic_label"] == "Stub-selected macro angle"

    inp = json.loads((root / "inputs" / "output.json").read_text(encoding="utf-8"))
    assert inp["mode"] == "auto"
    assert inp["topic"]["source"] == "auto_stub"


def test_run_id_from_cli_slug_matches_pattern(tmp_path: Path) -> None:
    when = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    res = run_assigned_skeleton(
        topic="x",
        slug="my-topic",
        artifacts_root=tmp_path,
        when=when,
    )
    assert res.run_id == "2026-01-02T03-04-05Z__assigned__my-topic"


def test_auto_run_id_from_cli_slug_matches_pattern(tmp_path: Path) -> None:
    when = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    res = run_auto_skeleton(
        slug="my-topic",
        artifacts_root=tmp_path,
        when=when,
    )
    assert res.run_id == "2026-01-02T03-04-05Z__auto__my-topic"


def _retrieval_fixtures_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "corpus" / "retrieval_labels"


def test_assigned_skeleton_corpus_labels_dir_populates_retrieval(tmp_path: Path) -> None:
    when = datetime(2026, 4, 24, 14, 0, 0, tzinfo=timezone.utc)
    labels = _retrieval_fixtures_dir()
    res = run_assigned_skeleton(
        topic="Corpus retrieval smoke",
        slug="corpus-retrieval",
        artifacts_root=tmp_path,
        when=when,
        run_id="2026-04-24T14-00-00Z__assigned__corpus-retrieval",
        corpus_labels_dir=labels,
    )
    retr = json.loads((res.run_dir / "retrieval" / "output.json").read_text(encoding="utf-8"))
    validate_file(res.run_dir / "retrieval" / "output.json", "retrieval_result")
    assert len(retr["ranked_hits"]) == 3
    refs = [h["piece_reference"] for h in retr["ranked_hits"]]
    assert refs[0].endswith("match-data-dissection.docx")
    assert refs[1].endswith("alt-in-alternates.docx")
    assert refs[2].endswith("other-archetype.docx")

    cfg = json.loads((res.run_dir / "config.json").read_text(encoding="utf-8"))
    assert cfg["corpus_retrieval"]["recursive"] is False
    assert cfg["corpus_retrieval"]["max_hits"] == 12
    assert "retrieval_labels" in cfg["corpus_retrieval"]["labels_dir"]


_LLM_FRAMING_FIXTURE = json.dumps(
    {
        "schema_version": "v1",
        "run_id": "ignored-by-pipeline",
        "primary_archetype_id": "data_dissection",
        "rationale": "Integration test: synthetic LLM framing body.",
        "candidate_analogs": ["analog-a"],
        "key_implications_to_explore": ["implication-1"],
        "proposed_structure_outline": ["Act I", "Act II", "Act III"],
    }
)


class _RoutingFramingLlmClient:
    """Probe uses phase0-probe; framing uses a separate model id."""

    def complete_chat(  # type: ignore[no-untyped-def]
        self,
        *,
        messages,
        model,
        temperature=0.0,
        max_tokens=1024,
    ):
        if model == "phase0-probe":
            return ChatCompletionResult(
                text="ok",
                model="phase0-probe",
                input_tokens=1,
                output_tokens=1,
                latency_ms=0.1,
            )
        return ChatCompletionResult(
            text=_LLM_FRAMING_FIXTURE,
            model="test-framing-llm",
            input_tokens=100,
            output_tokens=200,
            latency_ms=12.0,
        )


def test_assigned_skeleton_llm_framing_produces_valid_framing_and_config(tmp_path: Path) -> None:
    when = datetime(2026, 4, 24, 16, 0, 0, tzinfo=timezone.utc)
    rid = "2026-04-24T16-00-00Z__assigned__llm-framing"
    res = run_assigned_skeleton(
        topic="LLM framing topic",
        slug="llm-framing",
        artifacts_root=tmp_path,
        when=when,
        run_id=rid,
        llm_framing=True,
        framing_model="framing-cheap-test",
        llm_client=_RoutingFramingLlmClient(),
    )
    root = res.run_dir
    validate_file(root / "framing" / "output.json", "framing_decision")
    framing = json.loads((root / "framing" / "output.json").read_text(encoding="utf-8"))
    assert framing["run_id"] == rid
    assert "Integration test" in framing["rationale"]

    cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
    assert cfg["llm_framing"]["enabled"] is True
    assert cfg["llm_framing"]["model_requested"] == "framing-cheap-test"
    assert cfg["llm_framing"]["model_effective"] == "test-framing-llm"
    assert cfg["models_by_stage"]["framing"] == "test-framing-llm"

    m = json.loads((root / "framing" / "metrics.json").read_text(encoding="utf-8"))
    assert m["llm"]["framing_completion"]["model"] == "test-framing-llm"
    assert m["validation"]["source"] == "llm_json_framing"

    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["stage_status"]["framing"] == "llm_structured_json"


def test_assigned_skeleton_llm_framing_rejects_default_stub_client(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="non-stub"):
        run_assigned_skeleton(
            topic="t",
            slug="x",
            artifacts_root=tmp_path,
            run_id="2026-04-24T16-00-00Z__assigned__stub-framing",
            llm_framing=True,
            llm_client=StubLLMClient(),
        )


def test_assigned_skeleton_rejects_non_dir_corpus_labels(tmp_path: Path) -> None:
    missing = tmp_path / "not-a-dir"
    with pytest.raises(NotADirectoryError):
        run_assigned_skeleton(
            topic="t",
            slug="bad-corpus",
            artifacts_root=tmp_path,
            run_id="2026-04-24T14-00-00Z__assigned__bad-corpus",
            corpus_labels_dir=missing,
        )


def test_assigned_skeleton_source_paths_populate_source_reading(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    source_a = repo_root / "tests" / "fixtures" / "pipeline" / "source_note_a.txt"
    source_b = repo_root / "tests" / "fixtures" / "pipeline" / "source_note_b.md"
    res = run_assigned_skeleton(
        topic="Source ingestion run",
        slug="source-ingestion",
        artifacts_root=tmp_path,
        run_id="2026-04-25T12-00-00Z__assigned__source-ingestion",
        source_paths=[source_a, source_b],
    )

    source_reading = json.loads(
        (res.run_dir / "source_reading" / "output.json").read_text(encoding="utf-8")
    )
    assert source_reading["reading_status"] == "completed"
    assert source_reading["highlights"]
    assert any("source_note_a.txt" in h for h in source_reading["highlights"])

    source_input = json.loads(
        (res.run_dir / "source_reading" / "input.json").read_text(encoding="utf-8")
    )
    assert len(source_input["source_notes"]) == 2

    cfg = json.loads((res.run_dir / "config.json").read_text(encoding="utf-8"))
    assert cfg["source_ingestion"]["count"] == 2
