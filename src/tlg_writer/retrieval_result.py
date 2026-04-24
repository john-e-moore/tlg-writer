"""Retrieval result document builder (SPEC §7.5)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import ValidationError

from tlg_writer.corpus_piece_artifacts import iter_json_files
from tlg_writer.json_schema import validate


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


def _archetype_match_score(doc: Mapping[str, Any], framing_primary: str) -> int:
    editorial = (doc.get("labels") or {}).get("editorial") or {}
    primary = editorial.get("primary_archetype_id")
    if isinstance(primary, str) and primary == framing_primary:
        return 2
    alts = editorial.get("alternate_archetype_ids")
    if isinstance(alts, list) and framing_primary in (x for x in alts if isinstance(x, str)):
        return 1
    return 0


def build_retrieval_result_from_labels_dir(
    *,
    run_id: str,
    topic: str,
    framing_primary_archetype_id: str,
    labels_dir: Path,
    max_hits: int = 12,
    recursive: bool = False,
) -> dict[str, Any]:
    """
    Build a ``retrieval_result`` v1 by scanning schema-valid ``piece_label`` JSON files.

    Ranks by archetype alignment to ``framing_primary_archetype_id`` (primary match,
    then alternate-id match, then remaining pieces for a stable pool). When no valid
    labels are found, falls back to the Phase 0 empty-hit stub (same as
    :func:`build_stub_retrieval_result_assigned`).
    """
    rows: list[tuple[int, str, dict[str, Any]]] = []
    for path in iter_json_files(labels_dir, recursive=recursive):
        try:
            raw: Any = json.loads(path.read_text(encoding="utf-8"))
            validate(raw, "piece_label")
        except (json.JSONDecodeError, ValidationError, KeyError):
            continue
        piece_id = str(raw["piece_id"])
        score = _archetype_match_score(raw, framing_primary_archetype_id)
        rows.append((score, piece_id, raw))

    if not rows:
        return build_stub_retrieval_result_assigned(run_id=run_id, topic=topic)

    rows.sort(key=lambda r: (-r[0], r[1]))
    cap = max_hits if max_hits > 0 else 12
    picked = rows[:cap]

    hits: list[dict[str, Any]] = []
    for i, (score, piece_id, doc) in enumerate(picked, start=1):
        basic = (doc.get("labels") or {}).get("basic_metadata") or {}
        title = basic.get("title") if isinstance(basic.get("title"), str) else None
        editorial = (doc.get("labels") or {}).get("editorial") or {}
        primary = editorial.get("primary_archetype_id")
        if score >= 2:
            why = (
                f"Primary archetype on label matches framing ({framing_primary_archetype_id!r}); "
                f"title={title!r}."
            )
        elif score == 1:
            why = (
                f"Alternate archetype list includes framing id {framing_primary_archetype_id!r}; "
                f"title={title!r}."
            )
        else:
            why = (
                "Included from label pool without archetype match to framing; "
                f"label primary={primary!r}; title={title!r}."
            )
        hit: dict[str, Any] = {
            "rank": i,
            "piece_reference": piece_id,
            "why_selected": why,
        }
        if title:
            hit["feature_summary"] = f"title: {title}"
        hits.append(hit)

    rationale = (
        f"Filesystem scan of piece_label JSON under {labels_dir} "
        f"(recursive={recursive}); ranked by alignment to framing primary_archetype_id="
        f"{framing_primary_archetype_id!r}; topic={topic!r}; labels_seen={len(rows)}."
    )
    return {
        "schema_version": "v1",
        "run_id": run_id,
        "rationale": rationale,
        "ranked_hits": hits,
    }
