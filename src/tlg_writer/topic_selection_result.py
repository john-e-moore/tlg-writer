"""Topic selection stage document builder."""

from __future__ import annotations

from typing import Any


def build_stub_topic_selection_result_assigned_skipped(
    *,
    run_id: str,
    topic: str,
) -> dict[str, Any]:
    """
    Build a schema-``v1`` topic selection record when **assigned** mode skips auto-selection.

    Suitable for ``topic_selection/output.json`` validation as ``topic_selection_result``.
    """
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "selection_status": "skipped",
        "skip_reason": "assigned_topic",
        "carried_topic_label": topic,
        "summary": (
            "assigned mode: topic provided by the operator; automatic topic_selection did not run."
        ),
    }


def build_stub_topic_selection_result_auto_completed(
    *,
    run_id: str,
    selected_topic_label: str,
) -> dict[str, Any]:
    """
    Build a schema-``v1`` topic selection record for **auto** Phase 0 stub runs.

    ``candidates_considered`` is empty until a real selector exists.
    """
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "selection_status": "completed",
        "selected_topic_label": selected_topic_label,
        "candidates_considered": [],
        "summary": (
            "Phase 0 **auto** stub: selection is marked completed with a deterministic label; "
            "no candidate search ran."
        ),
    }
