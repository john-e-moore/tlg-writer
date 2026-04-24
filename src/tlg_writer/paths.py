"""Repository-root resolution for loading schemas and default artifact roots."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """Return the git repo root (directory containing `schemas/json`)."""
    here = Path(__file__).resolve()
    for p in (here.parent, *here.parents):
        if (p / "schemas" / "json").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (missing schemas/json).")


def schemas_dir() -> Path:
    return repo_root() / "schemas" / "json"


def as_repo_relative(path: Path) -> str:
    """Return a path relative to the repo root when possible, else an absolute string."""
    root = repo_root()
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path.resolve())
