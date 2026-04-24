"""Validate on-disk ``piece_label`` / ``piece_features`` JSON trees (read-only)."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from jsonschema import ValidationError

from tlg_writer.json_schema import validate

_SCHEMA_BY_KIND = {
    "labels": "piece_label",
    "features": "piece_features",
}


def iter_json_files(root: Path, *, recursive: bool) -> Iterator[Path]:
    """Yield ``*.json`` paths under ``root`` (non-recursive unless ``recursive``)."""
    if not root.is_dir():
        raise NotADirectoryError(f"not a directory: {root}")
    if recursive:
        yield from sorted(p for p in root.rglob("*.json") if p.is_file())
    else:
        yield from sorted(p for p in root.glob("*.json") if p.is_file())


def validate_corpus_json_files(
    root: Path,
    *,
    kind: str,
    recursive: bool = False,
) -> list[tuple[Path, str]]:
    """
    Validate every ``*.json`` file under ``root`` against the schema for ``kind``.

    ``kind`` is ``\"labels\"`` (``piece_label``) or ``\"features\"`` (``piece_features``).
    Returns a list of ``(path, message)`` for failures; empty when all files validate.
    """
    schema = _SCHEMA_BY_KIND.get(kind)
    if schema is None:
        raise ValueError(f"kind must be one of {sorted(_SCHEMA_BY_KIND)}; got {kind!r}")

    failures: list[tuple[Path, str]] = []
    for path in iter_json_files(root, recursive=recursive):
        try:
            data: Any = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            failures.append((path, f"invalid JSON: {e}"))
            continue
        try:
            validate(data, schema)
        except ValidationError as e:
            failures.append((path, f"schema {schema}: {e.message}"))
    return failures
