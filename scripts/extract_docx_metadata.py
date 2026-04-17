#!/usr/bin/env python3
"""Extract OOXML metadata from Word .docx files into JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

NS = {
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "ep": "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}


def _text(el: ET.Element | None) -> str | None:
    if el is None:
        return None
    t = (el.text or "").strip()
    return t or None


def parse_core(root: ET.Element) -> dict[str, str]:
    out: dict[str, str] = {}
    for tag in ("title", "subject", "creator", "keywords", "description"):
        el = root.find(f"dc:{tag}", NS)
        v = _text(el)
        if v:
            out[tag] = v
    el = root.find("cp:category", NS)
    v = _text(el)
    if v:
        out["category"] = v
    for tag in ("lastModifiedBy", "revision"):
        el = root.find(f"cp:{tag}", NS)
        v = _text(el)
        if v:
            out[tag] = v
    for tag in ("created", "modified"):
        el = root.find(f"dcterms:{tag}", NS)
        if el is not None and el.text:
            out[tag] = el.text
    return out


def parse_app(root: ET.Element) -> dict[str, str]:
    out: dict[str, str] = {}
    for child in root:
        tag = child.tag.split("}")[-1]
        if child.text is not None and child.text.strip():
            out[tag] = child.text.strip()
        # Some values are nested (e.g. Vector); skip empty containers
    return out


def mask_core_pii(core: dict[str, str]) -> None:
    """Replace known PII fields in core metadata (mutates in place)."""
    for key in ("creator", "lastModifiedBy"):
        if key in core:
            core[key] = "masked"


def body_stats_from_document(z: zipfile.ZipFile) -> dict[str, int]:
    data = z.read("word/document.xml")
    doc_root = ET.fromstring(data)
    parts: list[str] = []
    w_t = f"{{{NS['w']}}}t"
    for t_el in doc_root.iter(w_t):
        if t_el.text:
            parts.append(t_el.text)
        if t_el.tail:
            parts.append(t_el.tail)
    full_text = "".join(parts)
    chars_ws = len(full_text)
    chars_no_ws = len(re.sub(r"\s+", "", full_text))
    words = len(full_text.split())
    return {
        "words_approx": words,
        "characters_with_spaces": chars_ws,
        "characters_no_spaces": chars_no_ws,
    }


def extract_docx(path: Path) -> dict:
    st = path.stat()
    mtime = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat()
    record: dict = {
        "source_path": str(path),
        "filesystem": {
            "size_bytes": st.st_size,
            "mtime_utc": mtime,
        },
    }
    try:
        with zipfile.ZipFile(path, "r") as z:
            names = set(z.namelist())
            if "docProps/core.xml" in names:
                record["core"] = parse_core(ET.fromstring(z.read("docProps/core.xml")))
                mask_core_pii(record["core"])
            else:
                record["core"] = {}
            if "docProps/app.xml" in names:
                record["app"] = parse_app(ET.fromstring(z.read("docProps/app.xml")))
            else:
                record["app"] = {}
            if "word/document.xml" in names:
                record["body"] = body_stats_from_document(z)
            else:
                record["body"] = {}
    except Exception as e:  # noqa: BLE001 — per-file capture
        record["error"] = f"{type(e).__name__}: {e}"
    return record


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/raw/pieces/unlabeled"),
        help="Directory containing .docx files",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw/pieces/metadata"),
        help="Directory to write JSON outputs",
    )
    args = p.parse_args()
    input_dir: Path = args.input_dir
    output_dir: Path = args.output_dir
    if not input_dir.is_dir():
        print(f"Input directory not found: {input_dir}", file=sys.stderr)
        return 1
    output_dir.mkdir(parents=True, exist_ok=True)

    docx_files = sorted(input_dir.glob("*.docx"))
    # input_dir is .../data/raw/pieces/unlabeled → repo-relative doc path under data/
    data_dir = input_dir.parent.parent.parent
    records: list[dict] = []
    for f in docx_files:
        meta = extract_docx(f)
        try:
            meta["relative_to_repo"] = str(Path("data") / f.relative_to(data_dir))
        except ValueError:
            meta["relative_to_repo"] = str(f)
        records.append(meta)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
    combined = output_dir / f"pieces_metadata_{stamp}.json"
    with combined.open("w", encoding="utf-8") as fh:
        json.dump(records, fh, indent=2, ensure_ascii=False)

    errors = sum(1 for r in records if "error" in r)
    print(f"Wrote {len(records)} records to {combined} ({errors} errors).")
    return 0 if errors == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
