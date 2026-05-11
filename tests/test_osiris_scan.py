"""Tests régression pour tools/osiris-scan.sh (Item 4 chantier 4).

Couvre : timeout configurable, retry exponential, budget total, fallback
JSON valide en toutes circonstances. Sans ce fix, le scanner timeout
silencieusement (vu re-run Nobert 2026-05-10 : "osiris-scan.sh ran but
no output") et corrompt le ph5-qa-report.
"""

from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OSIRIS_SCAN = REPO_ROOT / "tools" / "osiris-scan.sh"


def _make_fake_osiris(tmp_path: Path, scanner_body: str) -> Path:
    """Crée un faux OSIRIS_PATH avec un scanner.py qui exécute le body donné."""
    osiris_dir = tmp_path / "fake_osiris"
    osiris_dir.mkdir()
    (osiris_dir / "scanner.py").write_text(scanner_body, encoding="utf-8")
    return osiris_dir


def test_returns_valid_json_when_scanner_missing(tmp_path: Path):
    """Sans scanner.py → JSON valide avec error."""
    result = subprocess.run(
        ["bash", str(OSIRIS_SCAN), "https://example.com"],
        capture_output=True,
        text=True,
        timeout=10,
        env={"PATH": "/usr/bin:/bin", "OSIRIS_PATH": str(tmp_path / "doesnotexist")},
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "error" in data


def test_returns_scanner_output_on_success(tmp_path: Path):
    """Scanner qui réussit → stdout = JSON du scanner."""
    body = textwrap.dedent(
        """\
        import sys, json
        print(json.dumps({"score": 8.5, "url": sys.argv[1]}))
        """
    )
    osiris_dir = _make_fake_osiris(tmp_path, body)
    result = subprocess.run(
        ["bash", str(OSIRIS_SCAN), "https://example.com"],
        capture_output=True,
        text=True,
        timeout=10,
        env={"PATH": "/usr/bin:/bin", "OSIRIS_PATH": str(osiris_dir)},
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["score"] == 8.5
    assert data["url"] == "https://example.com"


def test_retries_on_timeout(tmp_path: Path):
    """Scanner qui timeout → retry avec backoff (Item 4)."""
    # Scanner qui hang infiniment
    body = textwrap.dedent(
        """\
        import time
        time.sleep(120)
        """
    )
    osiris_dir = _make_fake_osiris(tmp_path, body)
    result = subprocess.run(
        ["bash", str(OSIRIS_SCAN), "https://example.com"],
        capture_output=True,
        text=True,
        timeout=30,
        env={
            "PATH": "/usr/bin:/bin",
            "OSIRIS_PATH": str(osiris_dir),
            "OSIRIS_TIMEOUT_S": "2",  # timeout court pour le test
            "OSIRIS_MAX_RETRIES": "2",
            "OSIRIS_BUDGET_S": "20",
        },
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    # Doit reporter l'erreur après 2 tentatives
    assert "error" in data
    assert "failed after 2 attempts" in data["error"]
    assert "timeout" in data["last_error"].lower()


def test_budget_exceeded_returns_json(tmp_path: Path):
    """Si budget total dépassé → JSON error budget exceeded."""
    body = textwrap.dedent(
        """\
        import time
        time.sleep(120)
        """
    )
    osiris_dir = _make_fake_osiris(tmp_path, body)
    result = subprocess.run(
        ["bash", str(OSIRIS_SCAN), "https://example.com"],
        capture_output=True,
        text=True,
        timeout=15,
        env={
            "PATH": "/usr/bin:/bin",
            "OSIRIS_PATH": str(osiris_dir),
            "OSIRIS_TIMEOUT_S": "1",
            "OSIRIS_MAX_RETRIES": "10",
            "OSIRIS_BUDGET_S": "3",  # budget court → exceeded après 2-3 tentatives
        },
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "error" in data
    # Soit budget exceeded soit failed after retries — les deux sont OK
    assert ("budget" in data["error"]) or ("failed after" in data["error"])


def test_invalid_json_output_retried_then_fails(tmp_path: Path):
    """Scanner qui sort du non-JSON → retry, et au final JSON error valide."""
    body = textwrap.dedent(
        """\
        print("not valid json output")
        """
    )
    osiris_dir = _make_fake_osiris(tmp_path, body)
    result = subprocess.run(
        ["bash", str(OSIRIS_SCAN), "https://example.com"],
        capture_output=True,
        text=True,
        timeout=30,
        env={
            "PATH": "/usr/bin:/bin",
            "OSIRIS_PATH": str(osiris_dir),
            "OSIRIS_TIMEOUT_S": "5",
            "OSIRIS_MAX_RETRIES": "2",
            "OSIRIS_BUDGET_S": "20",
        },
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)  # ne doit PAS lever
    assert "error" in data


def test_first_attempt_success_no_retry(tmp_path: Path):
    """Première tentative réussit → pas de retry, donc rapide."""
    body = textwrap.dedent(
        """\
        import json
        print(json.dumps({"ok": True}))
        """
    )
    osiris_dir = _make_fake_osiris(tmp_path, body)

    import time

    start = time.monotonic()
    result = subprocess.run(
        ["bash", str(OSIRIS_SCAN), "https://example.com"],
        capture_output=True,
        text=True,
        timeout=10,
        env={
            "PATH": "/usr/bin:/bin",
            "OSIRIS_PATH": str(osiris_dir),
            "OSIRIS_TIMEOUT_S": "5",
            "OSIRIS_MAX_RETRIES": "3",
            "OSIRIS_BUDGET_S": "20",
        },
    )
    elapsed = time.monotonic() - start
    assert result.returncode == 0
    assert json.loads(result.stdout)["ok"] is True
    # Pas de retry = pas de sleep → terminé en quelques secondes
    assert elapsed < 5.0
