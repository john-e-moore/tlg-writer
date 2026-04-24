"""Source reading stage document builder."""

from __future__ import annotations

from typing import Any


def build_stub_source_reading_result_assigned(
    *,
    run_id: str,
    topic: str,
) -> dict[str, Any]:
    """
    Build a schema-``v1`` source reading result for assigned-topic skeleton runs.

    Suitable for ``source_reading/output.json`` validation as ``source_reading_result``.
    """
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "reading_status": "stub",
        "highlights": [],
        "claims": [],
        "topic_echo": topic,
        "summary": "Phase 0 stub: no source files ingested; highlights and claims are empty.",
    }
