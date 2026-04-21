"""run_id builder per `.agent/AGENTS.md` / `.agent/SPEC.md` §12.1."""

from __future__ import annotations

import re
from datetime import datetime, timezone


_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def normalize_slug(raw: str) -> str:
    s = raw.strip().lower().replace("_", "-")
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if not s or not _SLUG_RE.match(s):
        raise ValueError(
            "slug must be lowercase ASCII letters, digits, and hyphens (kebab-case)"
        )
    return s


def format_run_timestamp(when: datetime) -> str:
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    else:
        when = when.astimezone(timezone.utc)
    # SPEC example: 2026-04-17T14-32-10Z (colons in time replaced with hyphens)
    return when.strftime("%Y-%m-%dT%H-%M-%SZ")


def build_run_id(when: datetime, mode: str, slug: str) -> str:
    if mode not in ("assigned", "auto"):
        raise ValueError('mode must be "assigned" or "auto"')
    ts = format_run_timestamp(when)
    safe_slug = normalize_slug(slug)
    return f"{ts}__{mode}__{safe_slug}"
