"""Registry mapping pipeline stages to output JSON schema names."""

from __future__ import annotations

import pytest
from jsonschema import ValidationError

from tlg_writer.layout import STAGE_DIRS
from tlg_writer.stage_schemas import (
    OUTPUT_SCHEMA_BY_STAGE,
    output_json_schema_for_stage,
    validate_pipeline_stage_output,
)


def test_registry_covers_all_stage_dirs_in_order() -> None:
    assert tuple(OUTPUT_SCHEMA_BY_STAGE) == STAGE_DIRS
    assert len(OUTPUT_SCHEMA_BY_STAGE) == len(STAGE_DIRS)


def test_output_json_schema_for_stage_unknown() -> None:
    with pytest.raises(KeyError):
        output_json_schema_for_stage("not_a_stage")


def test_validate_pipeline_stage_output_rejects_bad_doc() -> None:
    with pytest.raises(ValidationError):
        validate_pipeline_stage_output("inputs", {"schema_version": "nope"})
