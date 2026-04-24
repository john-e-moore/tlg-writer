#!/usr/bin/env python3
"""CLI: Phase 0 assigned-topic skeleton run (inspectable `artifacts/runs/` tree)."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow running before editable install: `python scripts/run_assigned_skeleton.py`
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from tlg_writer.run_id import normalize_slug
from tlg_writer.skeleton_pipeline import run_assigned_skeleton


def main() -> int:
    p = argparse.ArgumentParser(
        description="Create a Phase 0 assigned-topic skeleton run under artifacts/runs/."
    )
    p.add_argument(
        "--topic",
        required=True,
        help="Assigned topic label (free text).",
    )
    p.add_argument(
        "--slug",
        required=True,
        help="Kebab-case slug for run_id (e.g. jobs-report).",
    )
    p.add_argument(
        "--artifacts-root",
        type=Path,
        default=_REPO_ROOT / "artifacts" / "runs",
        help="Directory in which the run folder is created (default: artifacts/runs).",
    )
    p.add_argument(
        "--run-id",
        help="Override run_id (for tests). Must not collide with an existing directory.",
    )
    p.add_argument(
        "--utc",
        help='Fixed UTC timestamp as "YYYY-MM-DDTHH:MM:SS" for reproducible run_id '
        "(only when --run-id is omitted).",
    )
    p.add_argument(
        "--corpus-labels-dir",
        type=Path,
        default=None,
        help=(
            "Optional directory of piece_label *.json files; retrieval ranks hits from disk "
            "(see build_retrieval_result_from_labels_dir) instead of empty Phase 0 stubs."
        ),
    )
    p.add_argument(
        "--corpus-labels-recursive",
        action="store_true",
        help="When set with --corpus-labels-dir, scan *.json recursively.",
    )
    p.add_argument(
        "--corpus-retrieval-max-hits",
        type=int,
        default=12,
        help="Cap ranked_hits when using --corpus-labels-dir (default: 12).",
    )
    args = p.parse_args()
    try:
        normalize_slug(args.slug)
    except ValueError as e:
        p.error(str(e))

    when: datetime | None = None
    if args.utc:
        when = datetime.strptime(args.utc, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)

    res = run_assigned_skeleton(
        topic=args.topic,
        slug=args.slug,
        artifacts_root=args.artifacts_root,
        when=when,
        run_id=args.run_id,
        corpus_labels_dir=args.corpus_labels_dir,
        corpus_labels_recursive=args.corpus_labels_recursive,
        corpus_retrieval_max_hits=args.corpus_retrieval_max_hits,
    )
    print(res.run_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
