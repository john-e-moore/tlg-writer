"""Unit tests for corpus batch artifact naming helpers."""

from __future__ import annotations

import hashlib

from tlg_writer.corpus_batch_stub import piece_artifact_stem


def test_piece_artifact_stem_is_stable_for_same_id() -> None:
    pid = "data/raw/pieces/unlabeled/example.docx"
    a = piece_artifact_stem(pid)
    b = piece_artifact_stem(pid)
    assert a == b
    assert a.startswith("piece_")
    h = hashlib.sha256(pid.encode("utf-8")).hexdigest()[:16]
    assert a == f"piece_{h}"


def test_piece_artifact_stem_differs_when_id_differs() -> None:
    assert piece_artifact_stem("a.docx") != piece_artifact_stem("b.docx")
