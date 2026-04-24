"""Unit tests for corpus batch_statistics v1 builder."""

from __future__ import annotations

import pytest

from tlg_writer.corpus_batch_stub import build_batch_statistics_v1


def test_build_batch_statistics_v1_length_mismatch() -> None:
    with pytest.raises(ValueError, match="written row count"):
        build_batch_statistics_v1(
            skip_missing_piece_id=0,
            skip_metadata_row_error=0,
            written_title_present=0,
            written_title_missing=0,
            words_approx_per_written=[1],
            primary_archetype_id_per_written=[None, None],
        )


def test_build_batch_statistics_v1_words_and_skips() -> None:
    stats = build_batch_statistics_v1(
        skip_missing_piece_id=2,
        skip_metadata_row_error=1,
        written_title_present=1,
        written_title_missing=2,
        words_approx_per_written=[100, None, 50],
        primary_archetype_id_per_written=[None, None, None],
    )
    assert stats["schema_version"] == "v1"
    assert stats["skip_reasons"]["missing_piece_id"] == 2
    assert stats["skip_reasons"]["metadata_row_error"] == 1
    assert stats["metadata_core_titles"]["present"] == 1
    assert stats["metadata_core_titles"]["missing"] == 2
    assert stats["features_words_approx"]["non_null_count"] == 2
    assert stats["features_words_approx"]["min"] == 50
    assert stats["features_words_approx"]["max"] == 100
    assert stats["features_words_approx"]["sum"] == 150
    assert stats["labels_editorial_primary_archetype"]["without_primary"] == 3
    assert stats["labels_editorial_primary_archetype"]["primary_id_counts"] == {}


def test_build_batch_statistics_v1_archetype_histogram() -> None:
    stats = build_batch_statistics_v1(
        skip_missing_piece_id=0,
        skip_metadata_row_error=0,
        written_title_present=3,
        written_title_missing=0,
        words_approx_per_written=[10, 20, 30],
        primary_archetype_id_per_written=[
            "data_dissection",
            "data_dissection",
            "scenario",
        ],
    )
    la = stats["labels_editorial_primary_archetype"]
    assert la["with_primary"] == 3
    assert la["without_primary"] == 0
    assert la["primary_id_counts"] == {"data_dissection": 2, "scenario": 1}


def test_build_batch_statistics_v1_empty_writes() -> None:
    stats = build_batch_statistics_v1(
        skip_missing_piece_id=0,
        skip_metadata_row_error=0,
        written_title_present=0,
        written_title_missing=0,
        words_approx_per_written=[],
        primary_archetype_id_per_written=[],
    )
    assert stats["features_words_approx"]["min"] is None
    assert stats["labels_editorial_primary_archetype"]["primary_id_counts"] == {}
