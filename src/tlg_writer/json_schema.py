"""Validate JSON documents against `schemas/json/*.schema.json`."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema import Draft202012Validator

from tlg_writer.paths import schemas_dir


@lru_cache(maxsize=32)
def _validator(schema_name: str) -> Draft202012Validator:
    path = schemas_dir() / f"{schema_name}.schema.json"
    with path.open(encoding="utf-8") as f:
        schema = json.load(f)
    return Draft202012Validator(schema)


def validate(instance: Any, schema_name: str) -> None:
    """Raise jsonschema.ValidationError if instance does not validate."""
    validator = _validator(schema_name)
    validator.validate(instance)


def validate_file(path: Path, schema_name: str) -> None:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    validate(data, schema_name)
