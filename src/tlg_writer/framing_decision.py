"""Framing decision document builder (SPEC §7.4)."""

from __future__ import annotations

import json
import re
from typing import Any

from tlg_writer.json_schema import validate
from tlg_writer.llm_client import ChatCompletionResult, ChatMessage, LLMClient
from tlg_writer.paths import repo_root


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


_JSON_FENCE = re.compile(r"```(?:json)?\s*([\s\S]*?)```", re.IGNORECASE)


def extract_json_object_from_llm_text(text: str) -> dict[str, Any]:
    """Parse a single JSON object from model text (optionally wrapped in ``json`` fences)."""
    raw = text.strip()
    m = _JSON_FENCE.search(raw)
    if m:
        raw = m.group(1).strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("no JSON object found in LLM response")
    return json.loads(raw[start : end + 1])


def normalize_framing_decision_from_llm(data: dict[str, Any], *, run_id: str) -> dict[str, Any]:
    """Force pipeline identity fields; keep provider-chosen editorial content."""
    merged = dict(data)
    merged["schema_version"] = "v1"
    merged["run_id"] = run_id
    return merged


def load_framing_llm_prompt_texts() -> tuple[str, str]:
    """Return (system, user_suffix) from ``prompts/framing/`` (user file is appended after context)."""
    root = repo_root()
    system = (root / "prompts" / "framing" / "system.md").read_text(encoding="utf-8")
    user_suffix = (root / "prompts" / "framing" / "user.md").read_text(encoding="utf-8")
    return system, user_suffix


def build_framing_llm_user_message(
    *,
    run_id: str,
    topic: str,
    source_reading_result: dict[str, Any],
    topic_selection_result: dict[str, Any],
    user_suffix: str,
) -> str:
    return (
        f"run_id (must match pipeline): {run_id}\n"
        f"assigned_topic: {topic}\n\n"
        "source_reading_result (JSON):\n"
        f"{json.dumps(source_reading_result, indent=2)}\n\n"
        "topic_selection_result (JSON):\n"
        f"{json.dumps(topic_selection_result, indent=2)}\n\n"
        f"{user_suffix.strip()}\n"
    )


def complete_framing_decision_via_llm(
    *,
    client: LLMClient,
    run_id: str,
    topic: str,
    source_reading_result: dict[str, Any],
    topic_selection_result: dict[str, Any],
    model: str,
) -> tuple[dict[str, Any], ChatCompletionResult]:
    """
    One chat completion whose text decodes to a ``framing_decision`` v1 document.

    The pipeline overwrites ``run_id`` / ``schema_version`` after parsing.
    """
    system, user_suffix = load_framing_llm_prompt_texts()
    user = build_framing_llm_user_message(
        run_id=run_id,
        topic=topic,
        source_reading_result=source_reading_result,
        topic_selection_result=topic_selection_result,
        user_suffix=user_suffix,
    )
    result = client.complete_chat(
        messages=[
            ChatMessage(role="system", content=system.strip()),
            ChatMessage(role="user", content=user),
        ],
        model=model,
        temperature=0.2,
        max_tokens=2048,
    )
    parsed = extract_json_object_from_llm_text(result.text)
    if not isinstance(parsed, dict):
        raise ValueError("LLM framing JSON root must be an object")
    doc = normalize_framing_decision_from_llm(parsed, run_id=run_id)
    validate(doc, "framing_decision")
    return doc, result
