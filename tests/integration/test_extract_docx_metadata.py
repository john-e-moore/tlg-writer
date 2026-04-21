"""End-to-end metadata extraction writes schema-valid JSON."""

from __future__ import annotations

import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import pytest

from tlg_writer.json_schema import validate
from tlg_writer.paths import repo_root


def _write_minimal_docx(path: Path) -> None:
    """Tiny OOXML package: core + body only (enough for extract_docx_metadata)."""
    buf = bytearray()
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(
            "docProps/core.xml",
            b"""<?xml version="1.0" encoding="UTF-8"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:title>Fixture piece</dc:title>
</cp:coreProperties>""",
        )
        z.writestr(
            "word/document.xml",
            b"""<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body><w:p><w:r><w:t>One two three four.</w:t></w:r></w:p></w:body>
</w:document>""",
        )


def test_extract_docx_metadata_writes_valid_batch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = repo_root()
    # Script assumes .../data/raw/pieces/unlabeled for relative_to_repo.
    input_dir = tmp_path / "data" / "raw" / "pieces" / "unlabeled"
    input_dir.mkdir(parents=True)
    _write_minimal_docx(input_dir / "fixture.docx")
    output_dir = tmp_path / "data" / "raw" / "pieces" / "metadata"
    output_dir.mkdir(parents=True)

    script = repo / "scripts" / "extract_docx_metadata.py"
    monkeypatch.chdir(repo)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "extract_docx_metadata.py",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
        ],
    )
    spec = importlib.util.spec_from_file_location("_extract_docx_metadata", script)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.main() == 0

    written = list(output_dir.glob("pieces_metadata_*.json"))
    assert len(written) == 1
    data = json.loads(written[0].read_text(encoding="utf-8"))
    validate(data, "pieces_metadata_batch")
    assert len(data) == 1
    row = data[0]
    assert row["relative_to_repo"].startswith("data/raw/pieces/unlabeled/")
    assert row["body"].get("words_approx", 0) >= 1
