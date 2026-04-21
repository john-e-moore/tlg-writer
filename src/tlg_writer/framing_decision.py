"""Framing decision document builder (SPEC §7.4)."""

from __future__ import annotations

from typing import Any


def build_stub_framing_decision_assigned(
    *,
    run_id: str,
    topic: str,
    primary_archetype_id: str,
) -> dict[str, Any]:
    """
    Build a schema-``v1`` framing object for assigned-topic skeleton runs.

    Deterministic placeholder content suitable for ``framing/output.json``
    validation as ``framing_decision``.
    """
    default_alternates = [
        "historical_analog",
        "future_implications",
        "narrative_challenge",
    ]
    rejected = [a for a in default_alternates if a != primary_archetype_id][:2]
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "primary_archetype_id": primary_archetype_id,
        "rejected_alternate_archetype_ids": rejected,
        "rationale": (
            f"(stub) Placeholder framing for assigned topic {topic!r} (Phase 0); "
            "replace with a real framing stage when prompts and sources are wired."
        ),
        "candidate_analogs": [],
        "key_implications_to_explore": [
            "Stub: enumerate transmission mechanisms from the headline data.",
        ],
        "proposed_structure_outline": [
            "Setup and reader promise",
            "Evidence from the release",
            "Interpretation / analog",
            "Trading or policy tilt",
            "Risks / caveats",
        ],
    }
