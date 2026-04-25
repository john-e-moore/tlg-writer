from __future__ import annotations

from pathlib import Path

import pytest

from tlg_writer.source_inputs import collect_source_notes


def test_collect_source_notes_reads_text_files() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    paths = [
        repo_root / "tests" / "fixtures" / "pipeline" / "source_note_a.txt",
        repo_root / "tests" / "fixtures" / "pipeline" / "source_note_b.md",
    ]
    notes = collect_source_notes(source_paths=paths, repo_root=repo_root)
    assert len(notes) == 2
    assert notes[0]["path"].startswith("tests/fixtures/pipeline/")
    assert "labor market" in notes[0]["preview"]
    assert "Inflation note" in notes[1]["preview"]


def test_collect_source_notes_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        collect_source_notes(
            source_paths=[tmp_path / "missing.txt"],
            repo_root=tmp_path,
        )
