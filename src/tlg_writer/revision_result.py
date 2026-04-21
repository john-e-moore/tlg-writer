"""Revision result document builder (SPEC §7.9)."""

from __future__ import annotations

from typing import Any


def build_stub_revision_result_assigned(
    *,
    run_id: str,
    draft_markdown: str,
) -> dict[str, Any]:
    """
    Build a schema-``v1`` revision object for assigned-topic skeleton runs.

    Deterministic placeholder suitable for ``revision/output.json`` validation
    as ``revision_result`` (cosmetic append only).
    """
    revised = (
        draft_markdown.rstrip()
        + "\n\n_Editorial revision pass: not performed (stub)._ \n"
    )
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "revised_markdown": revised,
        "change_summary": (
            "Phase 0 stub: cosmetic append only; no substantive revision applied."
        ),
        "unresolved_concerns": [
            "Upstream draft and critique were stubs; human review required before distribution.",
        ],
    }
