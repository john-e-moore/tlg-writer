"""Stub corpus batch: metadata batch → schema-valid labels + features + run manifest."""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tlg_writer.json_schema import validate
from tlg_writer.paths import repo_root
from tlg_writer.run_id import build_corpus_batch_run_id, normalize_slug


def _git_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root(),
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        return out.stdout.strip() or None
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def piece_artifact_stem(piece_id: str) -> str:
    h = hashlib.sha256(piece_id.encode("utf-8")).hexdigest()[:16]
    return f"piece_{h}"


def _try_repo_relative(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path.resolve())


def _stub_label(piece_id: str, record: dict[str, Any], labeled_at: str) -> dict[str, Any]:
    core = record.get("core") or {}
    title = core.get("title")
    basic: dict[str, Any] = {}
    if title:
        basic["title"] = title
    return {
        "piece_id": piece_id,
        "schema_version": "v1",
        "labeled_at_utc": labeled_at,
        "labels": {
            "basic_metadata": basic,
            "editorial": {},
            "voice": {},
            "structural": {},
            "quality": {},
        },
        "reviewer_notes": "stub batch: replace with real labeling (SPEC §9).",
    }


def _stub_features(piece_id: str, record: dict[str, Any], extracted_at: str) -> dict[str, Any]:
    body = record.get("body") or {}
    features: dict[str, Any] = {"stub": True, "source": "corpus_batch_stub"}
    if body:
        for k in ("words_approx", "characters_with_spaces", "characters_no_spaces"):
            if k in body:
                features[k] = body[k]
    return {
        "piece_id": piece_id,
        "schema_version": "v1",
        "extracted_at_utc": extracted_at,
        "features": features,
        "sources": ["scripts/run_corpus_batch_stub.py"],
    }


@dataclass(frozen=True)
class CorpusBatchStubResult:
    run_dir: Path
    run_id: str


def run_corpus_batch_stub(
    *,
    metadata_batch: Path,
    labels_dir: Path,
    features_dir: Path,
    artifacts_root: Path,
    slug: str,
    when: datetime | None = None,
    run_id: str | None = None,
) -> CorpusBatchStubResult:
    """
    Read a ``pieces_metadata_*.json`` batch, emit ``piece_label`` / ``piece_features``
    files under ``labels_dir`` / ``features_dir``, and write ``artifacts_root/<run_id>/``
    with ``manifest.json`` (``corpus_batch_manifest``), ``summary.md``, and ``logs/run.log``.

    Rows with per-file ``error`` from metadata extraction are skipped but counted.
    """
    when = when or datetime.now(timezone.utc)
    if run_id is None:
        rid = build_corpus_batch_run_id(when, slug)
    else:
        rid = run_id
        normalize_slug(slug)

    root = repo_root()
    run_dir = artifacts_root / rid
    if run_dir.exists():
        raise FileExistsError(f"run directory already exists: {run_dir}")

    raw = json.loads(metadata_batch.read_text(encoding="utf-8"))
    validate(raw, "pieces_metadata_batch")

    created = when.astimezone(timezone.utc)
    labeled_at = created.isoformat().replace("+00:00", "Z")
    extracted_at = labeled_at

    labels_dir.mkdir(parents=True, exist_ok=True)
    features_dir.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True)
    (run_dir / "logs").mkdir()

    artifact_index: dict[str, dict[str, str]] = {}
    labels_written = 0
    features_written = 0
    skipped = 0
    log_lines: list[str] = [f"run_id={rid}", f"metadata_batch={metadata_batch}", ""]

    for row in raw:
        piece_id = row.get("relative_to_repo")
        if not piece_id or not isinstance(piece_id, str):
            skipped += 1
            log_lines.append("skip: missing relative_to_repo")
            continue
        if "error" in row:
            skipped += 1
            log_lines.append(f"skip (metadata error): {piece_id}")
            continue

        stem = piece_artifact_stem(piece_id)
        label_path = labels_dir / f"{stem}.json"
        feature_path = features_dir / f"{stem}.json"

        label_obj = _stub_label(piece_id, row, labeled_at)
        feature_obj = _stub_features(piece_id, row, extracted_at)
        validate(label_obj, "piece_label")
        validate(feature_obj, "piece_features")

        _write_json(label_path, label_obj)
        _write_json(feature_path, feature_obj)
        labels_written += 1
        features_written += 1

        artifact_index[piece_id] = {
            "label_relpath": _try_repo_relative(label_path, root),
            "feature_relpath": _try_repo_relative(feature_path, root),
        }
        log_lines.append(f"ok: {piece_id} -> {stem}.json")

    meta_relpath = _try_repo_relative(metadata_batch, root)
    counts = {
        "records_total": len(raw),
        "labels_written": labels_written,
        "features_written": features_written,
        "skipped_with_errors": skipped,
    }

    limitations = [
        "Deterministic stub only: no LLM or human labels (SPEC §21 step 3 placeholder).",
    ]
    if skipped == len(raw) and len(raw) > 0:
        limitations.append("All input rows were skipped (errors or missing ids).")

    manifest: dict[str, Any] = {
        "schema_version": "0.1",
        "run_id": rid,
        "created_at": labeled_at,
        "status": "completed",
        "job": {
            "kind": "stub_label_and_features",
            "note": "Writes schema-valid envelopes from metadata batch; not editorial quality.",
        },
        "inputs": {"metadata_batch_path": meta_relpath},
        "counts": counts,
        "outputs": {
            "labels_dir": _try_repo_relative(labels_dir, root),
            "features_dir": _try_repo_relative(features_dir, root),
        },
        "artifact_index": artifact_index,
        "limitations": limitations,
    }
    gc = _git_commit()
    if gc:
        manifest["git_commit"] = gc

    validate(manifest, "corpus_batch_manifest")
    _write_json(run_dir / "manifest.json", manifest)
    _write_text(
        run_dir / "summary.md",
        "## corpus batch (stub)\n\n"
        f"- Records in batch: **{counts['records_total']}**\n"
        f"- Labels written: **{counts['labels_written']}**\n"
        f"- Features written: **{counts['features_written']}**\n"
        f"- Skipped (metadata errors / bad rows): **{counts['skipped_with_errors']}**\n\n"
        "See `manifest.json` for paths. Replace stubs with real extractors per SPEC §9.\n",
    )
    _write_text(run_dir / "logs" / "run.log", "\n".join(log_lines) + "\n")

    return CorpusBatchStubResult(run_dir=run_dir, run_id=rid)
