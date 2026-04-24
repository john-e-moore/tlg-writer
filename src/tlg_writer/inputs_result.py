"""Inputs (intake) stage document builder."""

from __future__ import annotations

from typing import Any


def build_stub_inputs_result_assigned(*, run_id: str, topic: str) -> dict[str, Any]:
    """
    Build a schema-``v1`` inputs result for assigned-topic skeleton runs.

    Suitable for ``inputs/output.json`` validation as ``inputs_result``.
    """
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "mode": "assigned",
        "topic": {"label": topic, "source": "cli"},
        "intake_status": "completed",
        "summary": (
            "Recorded CLI topic for **assigned** mode; no auto-topic selection at intake."
        ),
    }
