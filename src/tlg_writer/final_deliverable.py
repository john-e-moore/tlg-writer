"""Final deliverable document builder (SPEC §7.10, §12.3)."""

from __future__ import annotations

from typing import Any


def build_stub_final_deliverable_assigned(
    *,
    run_id: str,
    body_markdown: str,
) -> dict[str, Any]:
    """
    Build a schema-``v1`` final deliverable for assigned-topic skeleton runs.

    Deterministic placeholder suitable for ``final/output.json`` validation as
    ``final_deliverable`` (body matches ``final/piece.md``).
    """
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "format": "markdown",
        "body_markdown": body_markdown,
        "limitations": [
            "All upstream stages are stubs or skipped.",
            "Not suitable for external distribution.",
        ],
        "summary": (
            "Phase 0 stub: markdown packaged for inspection; quality is intentionally low."
        ),
    }
