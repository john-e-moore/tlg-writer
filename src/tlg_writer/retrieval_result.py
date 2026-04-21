"""Retrieval result document builder (SPEC §7.5)."""

from __future__ import annotations

from typing import Any, Mapping


def build_stub_retrieval_result_assigned(*, run_id: str, topic: str) -> dict[str, Any]:
    """
    Build a schema-``v1`` retrieval object for Phase 0 skeleton runs.

    ``ranked_hits`` is empty until archive hooks exist; rationale records that
    honestly for operators.
    """
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "rationale": (
            "(stub) No archive query in Phase 0; ranked_hits intentionally empty "
            f"for topic {topic!r}."
        ),
        "ranked_hits": [],
    }


def ranked_piece_references(retrieval_doc: Mapping[str, Any]) -> list[str]:
    """Return ``piece_reference`` values in ascending ``rank`` order."""
    hits = list(retrieval_doc["ranked_hits"])
    hits.sort(key=lambda h: int(h["rank"]))
    return [str(h["piece_reference"]) for h in hits]
