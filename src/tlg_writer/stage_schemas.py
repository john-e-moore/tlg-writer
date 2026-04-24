"""Registry: pipeline stage directory → ``output.json`` JSON Schema name.

Single source of truth for assigned-topic skeleton output validation and tests.
See ``schemas/json/<name>.schema.json`` and ``tlg_writer.json_schema.validate``.
"""

from __future__ import annotations

from typing import Any, Final

from tlg_writer.layout import STAGE_DIRS

# Order must match ``STAGE_DIRS`` (fail fast at import if layout drifts).
_PIPELINE_OUTPUT_SCHEMA_ORDER: tuple[str, ...] = (
    "inputs_result",
    "source_reading_result",
    "topic_selection_result",
    "framing_decision",
    "retrieval_result",
    "piece_brief",
    "draft_result",
    "critique_result",
    "revision_result",
    "evaluation_result",
    "final_deliverable",
)

if len(_PIPELINE_OUTPUT_SCHEMA_ORDER) != len(STAGE_DIRS):
    raise RuntimeError("stage_schemas: STAGE_DIRS and schema tuple length mismatch")

OUTPUT_SCHEMA_BY_STAGE: Final[dict[str, str]] = dict(
    zip(STAGE_DIRS, _PIPELINE_OUTPUT_SCHEMA_ORDER, strict=True)
)


def output_json_schema_for_stage(stage: str) -> str:
    """Return the schema stem (no ``.schema.json``) used for ``<stage>/output.json``."""
    try:
        return OUTPUT_SCHEMA_BY_STAGE[stage]
    except KeyError as e:
        raise KeyError(f"unknown pipeline stage directory: {stage!r}") from e


def validate_pipeline_stage_output(stage: str, instance: Any) -> None:
    """Validate a parsed ``output.json`` object for ``stage`` against the registry."""
    from tlg_writer.json_schema import validate

    validate(instance, output_json_schema_for_stage(stage))
