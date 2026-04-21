"""Draft result document builder (SPEC §7.7)."""

from __future__ import annotations

from typing import Any


def build_stub_draft_result_assigned(
    *,
    run_id: str,
    topic: str,
    thesis: str,
) -> dict[str, Any]:
    """
    Build a schema-``v1`` draft object for assigned-topic skeleton runs.

    Deterministic placeholder suitable for ``drafting/output.json`` validation
    as ``draft_result``.
    """
    body = (
        f"# (Phase 0 stub draft)\n\nThesis: **{thesis}**\n\n"
        f"Assigned topic label: **{topic}**.\n\n"
        "This text exists so `final/` has a readable precursor. "
        "It is not client-ready copy.\n"
    )
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "body_markdown": body,
        "writer_notes": ["Phase 0: drafting agent did not run; body is template-filled."],
        "uncertainty_flags": [],
    }
