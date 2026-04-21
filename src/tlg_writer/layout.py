"""Pipeline stage names and directory layout (see `.agent/AGENTS.md`)."""

from __future__ import annotations

# Order for assigned-topic Phase 0 skeleton (topic_selection may record skip).
STAGE_DIRS: tuple[str, ...] = (
    "inputs",
    "source_reading",
    "topic_selection",
    "framing",
    "retrieval",
    "brief",
    "drafting",
    "critique",
    "revision",
    "evaluation",
    "final",
)

TOP_LEVEL_FILES = ("manifest.json", "config.json")
