#!/usr/bin/env python3
"""Print the bundled editorial archetype taxonomy (SPEC §8)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running without editable install (repo checkout).
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from tlg_writer.editorial_archetypes import (  # noqa: E402
    load_editorial_archetype_taxonomy,
    raw_taxonomy_document,
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--json",
        action="store_true",
        help="Emit the validated taxonomy document as JSON (single object).",
    )
    p.add_argument(
        "--version",
        default="v1",
        help="Taxonomy bundle version (default: v1).",
    )
    args = p.parse_args()
    tax = load_editorial_archetype_taxonomy(args.version)
    if args.json:
        doc = raw_taxonomy_document(args.version)
        json.dump(doc, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    for a in tax.archetypes:
        print(f"{a.id}\t{a.display_name}")
        print(f"  {a.summary}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
