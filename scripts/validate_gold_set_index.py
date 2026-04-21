#!/usr/bin/env python3
"""Validate a gold set index JSON file (schemas/json/gold_set_index.schema.json)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tlg_writer.gold_set import load_gold_set_index, validate_gold_set_index_document
from tlg_writer.paths import repo_root


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=None,
        help="Path to gold_set_index JSON (defaults to tests fixture for smoke).",
    )
    parser.add_argument(
        "--no-semantics",
        action="store_true",
        help="Schema only; skip duplicate-path and archetype-id checks.",
    )
    args = parser.parse_args()
    path = args.path
    if path is None:
        path = repo_root() / "tests/fixtures/corpus/gold_set_index_minimal.json"
        print(f"No path given; validating bundled fixture: {path}", file=sys.stderr)
    path = path.resolve()
    try:
        if args.no_semantics:
            with path.open(encoding="utf-8") as f:
                doc = json.load(f)
            validate_gold_set_index_document(doc)
        else:
            load_gold_set_index(path)
    except Exception as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        return 1
    print("ok", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
