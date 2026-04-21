"""run_id formatting and slug validation."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from tlg_writer.run_id import build_run_id, normalize_slug


def test_normalize_slug() -> None:
    assert normalize_slug("Jobs-Report") == "jobs-report"
    assert normalize_slug("  my_topic ") == "my-topic"


@pytest.mark.parametrize("bad", ["", "---", "  ", "🙂", "!!!"])
def test_normalize_slug_rejects(bad: str) -> None:
    with pytest.raises(ValueError):
        normalize_slug(bad)


def test_build_run_id() -> None:
    when = datetime(2026, 4, 17, 14, 32, 10, tzinfo=timezone.utc)
    assert build_run_id(when, "assigned", "jobs-report") == (
        "2026-04-17T14-32-10Z__assigned__jobs-report"
    )
