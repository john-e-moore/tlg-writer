"""Piece brief document builder and helpers (SPEC §7.6)."""

from __future__ import annotations

from typing import Any


def build_stub_piece_brief_assigned(
    *,
    run_id: str,
    topic: str,
    primary_archetype_id: str | None,
    ranked_retrieved_piece_ids: list[str],
) -> dict[str, Any]:
    """
    Build a schema-``v1`` brief object for assigned-topic skeleton runs.

    Populated deterministically from upstream stub payloads; suitable for
    ``brief/output.json`` validation as ``piece_brief``.
    """
    thesis = (
        f"(stub) Develop a data-grounded angle on: {topic}. "
        "Replace with a real brief builder when prompts and sources are wired."
    )
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "thesis": thesis,
        "audience_assumptions": [
            "Macro-aware institutional reader (stub).",
        ],
        "constraints": [
            "Phase 0 skeleton: no live retrieval or client distribution.",
        ],
        "required_citations": [],
        "candidate_analogs": list(ranked_retrieved_piece_ids),
        "implications_to_explore": [
            "Stub: connect headline data to policy or market pricing (to be refined).",
        ],
        "tone_target": "firm_house_style_placeholder",
        **({"primary_archetype_id": primary_archetype_id} if primary_archetype_id else {}),
    }
