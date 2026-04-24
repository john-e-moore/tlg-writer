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


def _format_corpus_stub_summary(counts: dict[str, int], batch_statistics: dict[str, Any]) -> str:
    sr = batch_statistics["skip_reasons"]
    mt = batch_statistics["metadata_core_titles"]
    fw = batch_statistics["features_words_approx"]
    la = batch_statistics["labels_editorial_primary_archetype"]
    dist = la["primary_id_counts"]
    dist_lines = "\n".join(f"| `{k}` | {v} |" for k, v in sorted(dist.items())) or "| _(none)_ | — |"

    w_block = (
        f"- Non-null `words_approx`: **{fw['non_null_count']}** / {fw['samples']}\n"
        f"- Min / max / sum: **{fw['min']}** / **{fw['max']}** / **{fw['sum']}**\n"
    )

    return (
        "## corpus batch (stub)\n\n"
        "### counts\n\n"
        f"- Records in batch: **{counts['records_total']}**\n"
        f"- Labels written: **{counts['labels_written']}**\n"
        f"- Features written: **{counts['features_written']}**\n"
        f"- Skipped (total): **{counts['skipped_with_errors']}**\n"
        f"  - Missing `relative_to_repo`: **{sr['missing_piece_id']}**\n"
        f"  - Metadata extraction `error` field: **{sr['metadata_row_error']}**\n\n"
        "### metadata (`core.title` among written rows)\n\n"
        f"- Present: **{mt['present']}**\n"
        f"- Missing: **{mt['missing']}**\n\n"
        "### features (`body.words_approx` among written rows)\n\n"
        f"{w_block}\n"
        "### labels (`editorial.primary_archetype_id`)\n\n"
        f"- With primary: **{la['with_primary']}**\n"
        f"- Without primary: **{la['without_primary']}**\n\n"
        "| primary_archetype_id | count |\n| --- | --- |\n"
        f"{dist_lines}\n\n"
        "See `manifest.json` (`batch_statistics`) for machine-readable aggregates. "
        "Replace stubs with real extractors per SPEC §9.\n"
    )


def build_batch_statistics_v1(
    *,
    skip_missing_piece_id: int,
    skip_metadata_row_error: int,
    written_title_present: int,
    written_title_missing: int,
    words_approx_per_written: list[int | None],
    primary_archetype_id_per_written: list[str | None],
) -> dict[str, Any]:
    """
    Build ``corpus_batch_manifest.batch_statistics`` (schema ``v1``) from per-row aggregates.

    ``words_approx_per_written`` / ``primary_archetype_id_per_written`` must align with
    successful writes (same length).
    """
    if len(words_approx_per_written) != len(primary_archetype_id_per_written):
        raise ValueError("words_approx and primary_archetype lists must match written row count")

    non_null_words = [w for w in words_approx_per_written if w is not None]
    if non_null_words:
        w_min: int | None = min(non_null_words)
        w_max: int | None = max(non_null_words)
        w_sum: int | None = sum(non_null_words)
    else:
        w_min = w_max = w_sum = None

    with_primary = 0
    counts: dict[str, int] = {}
    for pid in primary_archetype_id_per_written:
        if pid:
            with_primary += 1
            counts[pid] = counts.get(pid, 0) + 1
    without_primary = len(primary_archetype_id_per_written) - with_primary

    return {
        "schema_version": "v1",
        "skip_reasons": {
            "missing_piece_id": skip_missing_piece_id,
            "metadata_row_error": skip_metadata_row_error,
        },
        "metadata_core_titles": {
            "present": written_title_present,
            "missing": written_title_missing,
        },
        "features_words_approx": {
            "samples": len(words_approx_per_written),
            "non_null_count": len(non_null_words),
            "min": w_min,
            "max": w_max,
            "sum": w_sum,
        },
        "labels_editorial_primary_archetype": {
            "with_primary": with_primary,
            "without_primary": without_primary,
            "primary_id_counts": counts,
        },
    }


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
    with ``manifest.json`` (``corpus_batch_manifest`` including ``batch_statistics`` v1),
    ``summary.md`` (human-readable tables for the same aggregates), and ``logs/run.log``.

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
    skip_missing_piece_id = 0
    skip_metadata_row_error = 0
    written_title_present = 0
    written_title_missing = 0
    words_approx_per_written: list[int | None] = []
    primary_archetype_id_per_written: list[str | None] = []
    log_lines: list[str] = [f"run_id={rid}", f"metadata_batch={metadata_batch}", ""]

    for row in raw:
        piece_id = row.get("relative_to_repo")
        if not piece_id or not isinstance(piece_id, str):
            skipped += 1
            skip_missing_piece_id += 1
            log_lines.append("skip: missing relative_to_repo")
            continue
        if "error" in row:
            skipped += 1
            skip_metadata_row_error += 1
            log_lines.append(f"skip (metadata error): {piece_id}")
            continue

        stem = piece_artifact_stem(piece_id)
        label_path = labels_dir / f"{stem}.json"
        feature_path = features_dir / f"{stem}.json"

        core = row.get("core") or {}
        title = core.get("title")
        if isinstance(title, str) and title.strip():
            written_title_present += 1
        else:
            written_title_missing += 1

        body = row.get("body") or {}
        w_raw = body.get("words_approx")
        words_approx_per_written.append(int(w_raw) if isinstance(w_raw, int) else None)

        label_obj = _stub_label(piece_id, row, labeled_at)
        feature_obj = _stub_features(piece_id, row, extracted_at)
        validate(label_obj, "piece_label")
        validate(feature_obj, "piece_features")

        ed = (label_obj.get("labels") or {}).get("editorial") or {}
        p_raw = ed.get("primary_archetype_id")
        primary_archetype_id_per_written.append(p_raw if isinstance(p_raw, str) else None)

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
    batch_statistics = build_batch_statistics_v1(
        skip_missing_piece_id=skip_missing_piece_id,
        skip_metadata_row_error=skip_metadata_row_error,
        written_title_present=written_title_present,
        written_title_missing=written_title_missing,
        words_approx_per_written=words_approx_per_written,
        primary_archetype_id_per_written=primary_archetype_id_per_written,
    )

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

    manifest["batch_statistics"] = batch_statistics

    validate(manifest, "corpus_batch_manifest")
    _write_json(run_dir / "manifest.json", manifest)
    summary_body = _format_corpus_stub_summary(counts, batch_statistics)
    _write_text(run_dir / "summary.md", summary_body)
    _write_text(run_dir / "logs" / "run.log", "\n".join(log_lines) + "\n")

    return CorpusBatchStubResult(run_dir=run_dir, run_id=rid)
