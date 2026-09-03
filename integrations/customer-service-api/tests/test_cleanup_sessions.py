"""Safety and retention tests for the customer-service session cleanup utility."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest


CLEANUP_PATH = Path(__file__).resolve().parents[1] / "cleanup_sessions.py"
SPEC = importlib.util.spec_from_file_location("customer_service_cleanup_sessions", CLEANUP_PATH)
assert SPEC is not None and SPEC.loader is not None
CLEANUP = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CLEANUP
SPEC.loader.exec_module(CLEANUP)


def create_session(home: Path, session_id: str, modified_at: float) -> Path:
    """Create one minimal Harness session artifact with a controlled activity timestamp."""
    session_dir = home / "sessions" / "--workspace--" / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    artifact = session_dir / "session.jsonl.zstd"
    artifact.write_bytes(b"session-data")
    os.utime(artifact, (modified_at, modified_at))
    return session_dir


def test_cleanup_is_dry_run_by_default_and_only_matches_customer_service_sessions(tmp_path: Path) -> None:
    now = 2_000_000_000.0
    home = tmp_path / "isolated-dsh-home"
    old_customer = create_session(home, "customer-service-v2-old", now - 100 * 24 * 60 * 60)
    fresh_customer = create_session(home, "customer-service-v2-fresh", now - 5 * 24 * 60 * 60)
    unrelated = create_session(home, "developer-session", now - 100 * 24 * 60 * 60)

    result = CLEANUP.cleanup_sessions(
        home,
        90,
        apply=False,
        service_stopped=False,
        now_timestamp=now,
    )

    assert result.matched == 1
    assert result.removed == 0
    assert old_customer.exists()
    assert fresh_customer.exists()
    assert unrelated.exists()


def test_cleanup_requires_stopped_service_confirmation_before_removal(tmp_path: Path) -> None:
    now = 2_000_000_000.0
    home = tmp_path / "isolated-dsh-home"
    old_customer = create_session(home, "customer-service-v2-old", now - 100 * 24 * 60 * 60)

    with pytest.raises(CLEANUP.CleanupError, match="confirm-service-stopped"):
        CLEANUP.cleanup_sessions(
            home,
            90,
            apply=True,
            service_stopped=False,
            now_timestamp=now,
        )

    assert old_customer.exists()


def test_cleanup_removes_only_expired_customer_service_directory_when_confirmed(tmp_path: Path) -> None:
    now = 2_000_000_000.0
    home = tmp_path / "isolated-dsh-home"
    old_customer = create_session(home, "customer-service-v2-old", now - 100 * 24 * 60 * 60)
    fresh_customer = create_session(home, "customer-service-v2-fresh", now - 5 * 24 * 60 * 60)

    result = CLEANUP.cleanup_sessions(
        home,
        90,
        apply=True,
        service_stopped=True,
        now_timestamp=now,
    )

    assert result.matched == 1
    assert result.removed == 1
    assert not old_customer.exists()
    assert fresh_customer.exists()


def test_cleanup_rejects_user_home_as_target() -> None:
    with pytest.raises(CLEANUP.CleanupError, match="isolated child directory"):
        CLEANUP.resolve_session_root(Path.home())
