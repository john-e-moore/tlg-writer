"""Evaluation result document builder (SPEC §7.10, §15.1)."""

from __future__ import annotations

from typing import Any


_SCORECARD_KEYS = (
    "voice_match",
    "framing_quality",
    "originality",
    "macro_soundness",
    "evidence_usage",
    "conversational_quality",
    "sendability",
)


def build_stub_evaluation_result_assigned(*, run_id: str) -> dict[str, Any]:
    """
    Build a schema-``v1`` evaluation object for assigned-topic skeleton runs.

    Deterministic placeholder suitable for ``evaluation/output.json`` validation
    as ``evaluation_result`` (no rubric run; human review required).
    """
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "pass": False,
        "recommendation": "human_review_required",
        "scorecard": {k: None for k in _SCORECARD_KEYS},
        "summary": (
            "Phase 0 stub: final evaluation rubric did not run; scorecard entries are null "
            "and distribution requires human review per §15.3."
        ),
    }
