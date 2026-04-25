"""Source reading stage document builders."""

from __future__ import annotations

import re
from typing import Any


def _first_sentences(text: str, *, max_items: int) -> list[str]:
    chunks = [c.strip() for c in re.split(r"(?<=[.!?])\s+", text) if c.strip()]
    return chunks[:max_items]


def build_source_reading_result_assigned(
    *,
    run_id: str,
    topic: str,
    source_notes: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Build a schema-``v1`` source reading result for assigned-topic runs.

    ``source_notes`` entries accept:
    - ``path``: repo-relative path string
    - ``preview``: preview text extracted from that source
    """
    if not source_notes:
        return build_stub_source_reading_result_assigned(run_id=run_id, topic=topic)

    highlights: list[str] = []
    claims: list[str] = []
    for note in source_notes:
        path = str(note.get("path", "unknown"))
        preview = str(note.get("preview", "")).strip()
        if not preview:
            continue
        sentences = _first_sentences(preview, max_items=2)
        if not sentences:
            continue
        highlights.append(f"{path}: {sentences[0]}")
        for sentence in sentences[1:]:
            claims.append(f"{path}: {sentence}")

    if not highlights:
        return build_stub_source_reading_result_assigned(run_id=run_id, topic=topic)

    return {
        "schema_version": "v1",
        "run_id": run_id,
        "reading_status": "completed",
        "highlights": highlights[:8],
        "claims": claims[:8],
        "topic_echo": topic,
        "summary": (
            f"Ingested {len(source_notes)} local source file(s); extracted deterministic "
            "preview-based highlights and claims."
        ),
    }


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
