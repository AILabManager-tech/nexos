"""Tests régression pour A-004 chantier 4 : détection rate limit + retry/pivot.

Couvre `detect_rate_limit_in_log` et la logique de retry dans `run_cli`.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from orchestrator.cli_runner import detect_rate_limit_in_log, run_cli


def test_detects_claude_oauth_message(tmp_path: Path):
    """Cas central : log Claude CLI avec message 'out of extra usage'."""
    log = tmp_path / "session.log"
    log.write_text(
        "phase content...\nYou're out of extra usage · resets 4:20am (America/Toronto)\n",
        encoding="utf-8",
    )
    assert detect_rate_limit_in_log(log) is True


def test_detects_http_429(tmp_path: Path):
    log = tmp_path / "session.log"
    log.write_text("Error: HTTP 429 Too Many Requests\n", encoding="utf-8")
    assert detect_rate_limit_in_log(log) is True


def test_detects_rate_limit_with_dash(tmp_path: Path):
    log = tmp_path / "session.log"
    log.write_text("error: rate-limit exceeded\n", encoding="utf-8")
    assert detect_rate_limit_in_log(log) is True


def test_detects_quota_exceeded(tmp_path: Path):
    log = tmp_path / "session.log"
    log.write_text("API quota exceeded for this account\n", encoding="utf-8")
    assert detect_rate_limit_in_log(log) is True


def test_detects_resets_pattern(tmp_path: Path):
    log = tmp_path / "session.log"
    log.write_text("Limit reached. Resets at 4:20am\n", encoding="utf-8")
    assert detect_rate_limit_in_log(log) is True


def test_negative_on_normal_output(tmp_path: Path):
    """Log normal sans rate limit → False."""
    log = tmp_path / "session.log"
    log.write_text("Phase ph4-build complete. Files written.\n", encoding="utf-8")
    assert detect_rate_limit_in_log(log) is False


def test_returns_false_when_log_missing(tmp_path: Path):
    log = tmp_path / "missing.log"
    assert detect_rate_limit_in_log(log) is False


def test_scans_only_last_4kb(tmp_path: Path):
    """Le rate limit dans le tail doit être détecté ; pattern noyé en début
    de log volumineux doit aussi être trouvé si dans les derniers 4 Ko."""
    log = tmp_path / "session.log"
    # 10 Ko de bruit puis rate limit
    log.write_text("x" * 10000 + "\nrate limit hit\n", encoding="utf-8")
    assert detect_rate_limit_in_log(log) is True


def test_pattern_outside_tail_not_detected(tmp_path: Path):
    """Si rate limit est tout au début et puis 10 Ko de bruit → pas détecté
    (par design, on regarde le tail)."""
    log = tmp_path / "session.log"
    log.write_text("rate limit hit\n" + "x" * 10000, encoding="utf-8")
    assert detect_rate_limit_in_log(log) is False


def test_run_cli_success_no_retry(tmp_path: Path):
    """Cas succès : un seul appel CLI, pas de retry."""
    log_path = tmp_path / "session.log"
    log_path.write_text("ok\n", encoding="utf-8")

    with patch("orchestrator.cli_runner._dispatch_cli", return_value=0) as mock:
        rc = run_cli("prompt", str(tmp_path), log_path)
    assert rc == 0
    assert mock.call_count == 1


def test_run_cli_non_rate_limit_failure_no_retry(tmp_path: Path):
    """Cas échec non-rate-limit : pas de retry, return immédiat."""
    log_path = tmp_path / "session.log"
    log_path.write_text("syntax error in prompt\n", encoding="utf-8")

    with patch("orchestrator.cli_runner._dispatch_cli", return_value=1) as mock:
        rc = run_cli("prompt", str(tmp_path), log_path)
    assert rc == 1
    assert mock.call_count == 1


def test_run_cli_rate_limit_retries(tmp_path: Path):
    """Rate limit → retry avec backoff. Succès au 2e essai → return 0."""
    log_path = tmp_path / "session.log"
    log_path.write_text("rate limit exceeded\n", encoding="utf-8")

    call_count = [0]

    def side_effect(host, prompt, cwd, log):
        call_count[0] += 1
        if call_count[0] >= 2:
            # 2e tentative : réussit (effacer le log "rate limit")
            log_path.write_text("ok\n", encoding="utf-8")
            return 0
        return 1

    with (
        patch("orchestrator.cli_runner._dispatch_cli", side_effect=side_effect),
        patch("orchestrator.cli_runner.time.sleep") as mock_sleep,
    ):
        rc = run_cli("prompt", str(tmp_path), log_path)

    assert rc == 0
    assert call_count[0] == 2
    # Backoff 30s appliqué
    assert mock_sleep.called
    mock_sleep.assert_called_with(30)


def test_run_cli_all_retries_fail_then_pivot_codex(tmp_path: Path):
    """Si Claude rate limit persiste → pivot Codex."""
    log_path = tmp_path / "session.log"
    log_path.write_text("rate limit\n", encoding="utf-8")

    dispatch_calls = []

    def side_effect(host, prompt, cwd, log):
        dispatch_calls.append(host)
        if host == "codex":
            log_path.write_text("ok codex\n", encoding="utf-8")
            return 0
        return 1

    with (
        patch("orchestrator.cli_runner.get_cli_host", return_value="claude"),
        patch("orchestrator.cli_runner._dispatch_cli", side_effect=side_effect),
        patch("orchestrator.cli_runner._is_codex_available", return_value=True),
        patch("orchestrator.cli_runner.time.sleep"),
    ):
        rc = run_cli("prompt", str(tmp_path), log_path)

    assert rc == 0
    # 1 tentative initiale + 3 retries Claude + 1 pivot Codex = 5
    assert dispatch_calls == ["claude", "claude", "claude", "claude", "codex"]
