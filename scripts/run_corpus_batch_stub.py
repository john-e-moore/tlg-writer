#!/usr/bin/env python3
"""Run stub labeling + feature extraction from a metadata batch (SPEC §21 steps 3–4 slice)."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from tlg_writer.corpus_batch_stub import run_corpus_batch_stub
from tlg_writer.paths import repo_root
from tlg_writer.run_id import normalize_slug


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--metadata-batch",
        type=Path,
        required=True,
        help="Path to pieces_metadata_<UTC>.json (validated as pieces_metadata_batch)",
    )
    p.add_argument(
        "--labels-dir",
        type=Path,
        default=Path("data/processed/pieces/labeled"),
        help="Directory for piece_label JSON files",
    )
    p.add_argument(
        "--features-dir",
        type=Path,
        default=Path("data/processed/pieces/extracted_features"),
        help="Directory for piece_features JSON files",
    )
    p.add_argument(
        "--artifacts-root",
        type=Path,
        default=Path("artifacts/runs"),
        help="Root for timestamped corpus run directories",
    )
    p.add_argument(
        "--slug",
        required=True,
        help="Kebab-case slug for run_id (see .agent/AGENTS.md)",
    )
    p.add_argument(
        "--run-id",
        type=str,
        default=None,
        help="Fixed run_id for tests (default: allocate fresh UTC id)",
    )
    p.add_argument(
        "--utc",
        type=str,
        default=None,
        help="ISO-8601 instant (UTC) for run_id timestamp; tests only",
    )
    args = p.parse_args()
    root = repo_root()
    batch = (root / args.metadata_batch) if not args.metadata_batch.is_absolute() else args.metadata_batch
    labels_dir = (root / args.labels_dir) if not args.labels_dir.is_absolute() else args.labels_dir
    features_dir = (root / args.features_dir) if not args.features_dir.is_absolute() else args.features_dir
    artifacts_root = (
        root / args.artifacts_root if not args.artifacts_root.is_absolute() else args.artifacts_root
    )

    if not batch.is_file():
        print(f"Metadata batch not found: {batch}", file=sys.stderr)
        return 1

    normalize_slug(args.slug)
    when: datetime | None = None
    if args.utc:
        when = datetime.fromisoformat(args.utc.replace("Z", "+00:00"))
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)

    try:
        res = run_corpus_batch_stub(
            metadata_batch=batch,
            labels_dir=labels_dir,
            features_dir=features_dir,
            artifacts_root=artifacts_root,
            slug=args.slug,
            when=when,
            run_id=args.run_id,
        )
    except FileExistsError as e:
        print(str(e), file=sys.stderr)
        return 3
    except Exception as e:  # noqa: BLE001 — CLI boundary
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        return 2

    print(res.run_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
