"""Helpers for deterministic local source-file ingestion."""

from __future__ import annotations

import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def _read_docx_text(path: Path) -> str:
    with zipfile.ZipFile(path, "r") as zf:
        data = zf.read("word/document.xml")
    root = ET.fromstring(data)
    w_t = f"{{{_NS['w']}}}t"
    chunks: list[str] = []
    for node in root.iter(w_t):
        if node.text:
            chunks.append(node.text)
    return " ".join(chunks).strip()


def _read_text_like(path: Path) -> str:
    # Prefer UTF-8 with replacement for deterministic behavior on mixed corpora.
    return path.read_text(encoding="utf-8", errors="replace").strip()


def read_source_preview(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return _read_text_like(path)
    if suffix == ".json":
        raw = json.loads(_read_text_like(path))
        return json.dumps(raw, ensure_ascii=False, indent=2)
    if suffix == ".docx":
        return _read_docx_text(path)
    raise ValueError(f"Unsupported source file extension: {path.suffix}")


def collect_source_notes(*, source_paths: list[Path], repo_root: Path) -> list[dict[str, Any]]:
    notes: list[dict[str, Any]] = []
    for path in source_paths:
        resolved = path.resolve()
        if not resolved.is_file():
            raise FileNotFoundError(f"Source file not found: {path}")
        preview = read_source_preview(resolved)
        try:
            rel = str(resolved.relative_to(repo_root))
        except ValueError:
            rel = str(resolved)
        notes.append(
            {
                "path": rel,
                "size_bytes": resolved.stat().st_size,
                "preview": preview[:1200],
            }
        )
    return notes
