#!/usr/bin/env python3
"""Preview or remove expired customer-service Harness session directories."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path


SESSION_PREFIX = "customer-service-"
SESSION_ARTIFACT_NAMES = {"session.jsonl", "session.jsonl.zstd"}


class CleanupError(ValueError):
    """A retention request is unsafe or does not match the Harness session layout."""


@dataclass(frozen=True, slots=True)
class CleanupResult:
    """Summary returned by one dry-run or applied retention pass."""

    matched: int
    removed: int
    reclaimed_bytes: int


def resolve_session_root(dsh_home: Path) -> Path:
    """Resolve the isolated Harness session root and reject broad destructive targets."""
    home = dsh_home.expanduser().resolve()
    filesystem_root = Path(home.anchor).resolve()
    user_home = Path.home().resolve()
    if home == filesystem_root or home == user_home:
        raise CleanupError("DCS_DSH_HOME must be an isolated child directory, not a filesystem or user home")
    if home.name.lower() in {"", "home", "users", "documents", "work"}:
        raise CleanupError("DCS_DSH_HOME is too broad for customer-service retention")

    session_root = home / "sessions"
    if not session_root.is_dir():
        raise CleanupError(f"Harness session root does not exist: {session_root}")
    return session_root


def find_expired_session_dirs(session_root: Path, cutoff_timestamp: float) -> list[Path]:
    """Find only customer-service session directories whose fixed log artifact is expired."""
    expired: list[Path] = []
    for artifact in session_root.rglob("session.jsonl*"):
        if not artifact.is_file() or artifact.name not in SESSION_ARTIFACT_NAMES:
            continue
        session_dir = artifact.parent
        if not session_dir.name.startswith(SESSION_PREFIX):
            continue
        latest_activity = max(
            (item.stat().st_mtime for item in session_dir.rglob("*") if item.is_file()),
            default=artifact.stat().st_mtime,
        )
        if latest_activity < cutoff_timestamp:
            expired.append(session_dir)
    return sorted(set(expired))


def directory_size(path: Path) -> int:
    """Return the regular-file byte count for one candidate session directory."""
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def cleanup_sessions(
    dsh_home: Path,
    older_than_days: int,
    *,
    apply: bool,
    service_stopped: bool,
    now_timestamp: float | None = None,
) -> CleanupResult:
    """Preview or remove expired sessions after validating scope and service ownership."""
    if older_than_days < 1:
        raise CleanupError("older-than-days must be at least 1")
    if apply and not service_stopped:
        raise CleanupError("--apply requires --confirm-service-stopped")

    session_root = resolve_session_root(dsh_home)
    now = time.time() if now_timestamp is None else now_timestamp
    cutoff = now - older_than_days * 24 * 60 * 60
    candidates = find_expired_session_dirs(session_root, cutoff)
    reclaimed_bytes = sum(directory_size(path) for path in candidates)

    if apply:
        for path in candidates:
            # 候选目录由固定 sessions 根、固定日志文件名和客服前缀共同限定，删除前再次校验父级边界。
            if session_root not in path.parents or not path.name.startswith(SESSION_PREFIX):
                raise CleanupError(f"refusing to remove unexpected path: {path}")
            shutil.rmtree(path)
        for project_dir in sorted(
            (path for path in session_root.iterdir() if path.is_dir()),
            key=lambda path: len(path.parts),
            reverse=True,
        ):
            if not any(project_dir.iterdir()):
                project_dir.rmdir()

    return CleanupResult(
        matched=len(candidates),
        removed=len(candidates) if apply else 0,
        reclaimed_bytes=reclaimed_bytes,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse explicit retention options; deletion is never the default behavior."""
    parser = argparse.ArgumentParser(description=__doc__)
    configured_home = os.environ.get("DCS_DSH_HOME", "").strip()
    parser.add_argument(
        "--dsh-home",
        type=Path,
        default=Path(configured_home) if configured_home else None,
        help="isolated Harness home; defaults to DCS_DSH_HOME",
    )
    parser.add_argument("--older-than-days", type=int, default=90)
    parser.add_argument("--apply", action="store_true", help="remove matched sessions; default is dry-run")
    parser.add_argument(
        "--confirm-service-stopped",
        action="store_true",
        help="required with --apply because the persistence backend has no cross-process lease",
    )
    args = parser.parse_args(argv)
    if args.dsh_home is None:
        parser.error("--dsh-home or DCS_DSH_HOME is required")
    return args


def main(argv: list[str] | None = None) -> int:
    """Run one retention pass and print a compact operator-facing result."""
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        result = cleanup_sessions(
            args.dsh_home,
            args.older_than_days,
            apply=args.apply,
            service_stopped=args.confirm_service_stopped,
        )
    except CleanupError as exc:
        print(f"customer-service-session-cleanup: {exc}", file=sys.stderr)
        return 2

    mode = "applied" if args.apply else "dry-run"
    print(
        f"customer-service-session-cleanup: mode={mode} matched={result.matched} "
        f"removed={result.removed} bytes={result.reclaimed_bytes}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
