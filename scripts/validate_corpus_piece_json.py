#!/usr/bin/env python3
"""Validate ``piece_label`` and/or ``piece_features`` JSON files under corpus directories."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tlg_writer.corpus_piece_artifacts import validate_corpus_json_files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--labels-dir",
        type=Path,
        default=None,
        help="Directory of piece_label JSON files (*.json).",
    )
    parser.add_argument(
        "--features-dir",
        type=Path,
        default=None,
        help="Directory of piece_features JSON files (*.json).",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Include *.json in subdirectories (default: only top-level *.json).",
    )
    args = parser.parse_args()
    if args.labels_dir is None and args.features_dir is None:
        parser.error("pass at least one of --labels-dir or --features-dir")

    any_fail = False
    for label, kind in (args.labels_dir, "labels"), (args.features_dir, "features"):
        if label is None:
            continue
        path = label.resolve()
        failures = validate_corpus_json_files(path, kind=kind, recursive=args.recursive)
        if failures:
            any_fail = True
            for fp, msg in failures:
                print(f"{fp}: {msg}", file=sys.stderr)
        else:
            print(f"ok {kind}: {path} ({_count_json(path, args.recursive)} files)")

    return 1 if any_fail else 0


def _count_json(root: Path, recursive: bool) -> int:
    if not root.is_dir():
        return 0
    if recursive:
        return sum(1 for p in root.rglob("*.json") if p.is_file())
    return sum(1 for p in root.glob("*.json") if p.is_file())


if __name__ == "__main__":
    raise SystemExit(main())
