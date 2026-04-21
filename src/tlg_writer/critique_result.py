"""Critique result document builder (SPEC §7.8, §15.1)."""

from __future__ import annotations

from typing import Any


_RUBRIC_KEYS = (
    "voice_match",
    "framing_quality",
    "originality",
    "macro_soundness",
    "evidence_usage",
    "conversational_quality",
    "sendability",
)


def build_stub_critique_result_assigned(*, run_id: str) -> dict[str, Any]:
    """
    Build a schema-``v1`` critique object for assigned-topic skeleton runs.

    Deterministic placeholder suitable for ``critique/output.json`` validation
    as ``critique_result`` (all rubric scores unset).
    """
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "rubric_scores": {k: None for k in _RUBRIC_KEYS},
        "meets_publish_bar": False,
        "revision_notes": [
            "voice not evaluated (Phase 0 stub)",
            "macro not evaluated (Phase 0 stub)",
        ],
        "summary": (
            "Phase 0 stub: specialized critics did not run; rubric scores are null "
            "and the draft requires human review."
        ),
    }
