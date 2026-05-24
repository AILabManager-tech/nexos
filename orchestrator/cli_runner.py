"""Exécution CLI — lance l'agent LLM (Claude, Codex, ou Gemini) et capture sa sortie."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from ._shared import say

_CODEX_CLI_TIMEOUT = 1800  # 30 minutes par phase

# A-004 chantier 4 : détection rate limit Claude OAuth + retry/pivot.
# Patterns observés :
# - "You're out of extra usage · resets 4:20am (America/Toronto)" (Claude CLI)
# - "rate limit exceeded"
# - "HTTP 429"
# - "quota exceeded"
_RATE_LIMIT_PATTERNS = [
    re.compile(r"rate[\s-]?limit", re.IGNORECASE),
    re.compile(r"\b429\b"),
    re.compile(r"out of\s+(?:extra\s+)?usage", re.IGNORECASE),
    re.compile(r"quota\s+exceeded", re.IGNORECASE),
    re.compile(r"resets?\s+(?:at\s+)?\d", re.IGNORECASE),
]
_RATE_LIMIT_BACKOFF_S = (30, 120, 480)  # 30s, 2min, 8min


def get_cli_host() -> str:
    """Détermine quel CLI hôte utiliser.

    Ordre de préférence :
    1. NEXOS_LLM_HOST env var (claude, codex, gemini)
    2. Détection automatique : claude > codex > gemini
    3. Fallback : claude (défaut depuis pivot 2026-04-17 phase-L,
       codex auth s'étant révélée fragile en production)
    """
    env_host = os.environ.get("NEXOS_LLM_HOST", "").lower()
    if env_host in ("claude", "codex", "gemini"):
        return env_host

    # Détection : essayer claude d'abord (plus probable en Claude Code)
    for cli in ("claude", "codex", "gemini"):
        try:
            subprocess.run([cli, "--version"], capture_output=True, timeout=2)
            return cli
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    # Fallback : default to claude (depuis pivot 2026-04-17)
    return "claude"


def run_codex_cli(prompt: str, cwd: str, log_path: Path) -> int:
    """Lance Codex CLI avec le prompt et capture la sortie.

    Timeout: 30 minutes par défaut pour éviter un blocage indéfini.
    """
    cmd = ["codex", "exec", "--dangerously-bypass-approvals-and-sandbox", "-"]

    log_path.parent.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()

    process = None
    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        if process.stdin:
            try:
                process.stdin.write(prompt)
                process.stdin.close()
            except BrokenPipeError:
                pass

        deadline = time.monotonic() + _CODEX_CLI_TIMEOUT

        with log_path.open("w", encoding="utf-8") as log:
            log.write("# NEXOS v3.0 Log\n")
            log.write(f"# Date: {datetime.now().isoformat()}\n")
            log.write(f"# Prompt:\n{prompt}\n\n---\n\n")

            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                log.write(line)
                if time.monotonic() > deadline:
                    say(
                        f"\n[red]⚠ Codex CLI timeout ({_CODEX_CLI_TIMEOUT // 60}min) — interruption[/]"
                    )
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                    return 124

        process.wait(timeout=30)
        return process.returncode

    except FileNotFoundError:
        say(
            "[red bold]Codex CLI non trouvé.[/]\n"
            "Installe-le avec: [cyan]npm install -g @openai/codex[/]"
        )
        return 1
    except KeyboardInterrupt:
        say("\n[yellow]⚠ Interrompu par l'utilisateur[/]")
        if process:
            process.terminate()
        return 130
    except subprocess.TimeoutExpired:
        say("\n[red]⚠ Codex CLI process.wait() timeout — kill[/]")
        if process:
            process.kill()
        return 124


def run_claude_cli(prompt: str, cwd: str, log_path: Path) -> int:
    """Lance Claude CLI avec le prompt et capture la sortie.

    Timeout: 30 minutes par défaut pour éviter un blocage indéfini.
    """
    cmd = ["claude", "-p", "--dangerously-skip-permissions"]

    log_path.parent.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    # Force session-auth (keychain/OAuth) rather than inheriting an invalid
    # ANTHROPIC_API_KEY from the parent shell. Without this, the child CLI
    # errors with "Invalid API key · Fix external API key".
    env.pop("ANTHROPIC_API_KEY", None)

    process = None
    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        if process.stdin:
            try:
                process.stdin.write(prompt)
                process.stdin.close()
            except BrokenPipeError:
                pass

        deadline = time.monotonic() + _CODEX_CLI_TIMEOUT

        with log_path.open("w", encoding="utf-8") as log:
            log.write("# NEXOS v3.0 Log\n")
            log.write(f"# Date: {datetime.now().isoformat()}\n")
            log.write(f"# Prompt:\n{prompt}\n\n---\n\n")

            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                log.write(line)
                if time.monotonic() > deadline:
                    say(
                        f"\n[red]⚠ Claude CLI timeout ({_CODEX_CLI_TIMEOUT // 60}min) — interruption[/]"
                    )
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                    return 124

        process.wait(timeout=30)
        return process.returncode

    except FileNotFoundError:
        say(
            "[red bold]Claude CLI non trouvé.[/]\n"
            "Installe-le avec: [cyan]npm install -g @anthropic-ai/claude-cli[/]"
        )
        return 1
    except KeyboardInterrupt:
        say("\n[yellow]⚠ Interrompu par l'utilisateur[/]")
        if process:
            process.terminate()
        return 130
    except subprocess.TimeoutExpired:
        say("\n[red]⚠ Claude CLI process.wait() timeout — kill[/]")
        if process:
            process.kill()
        return 124


def detect_rate_limit_in_log(log_path: Path) -> bool:
    """A-004 fix : détecte un rate limit dans le log d'une session CLI.

    Scrute la queue du log (derniers 4 Ko) pour matcher les patterns
    connus de rate limit Claude/Codex. Retourne True si match.
    """
    if not log_path.exists():
        return False
    try:
        content = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    tail = content[-4000:]
    return any(p.search(tail) for p in _RATE_LIMIT_PATTERNS)


def _is_codex_available() -> bool:
    """Vérifie si codex CLI est installé (pour pivot post-rate-limit Claude)."""
    try:
        subprocess.run(["codex", "--version"], capture_output=True, timeout=2)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _dispatch_cli(host: str, prompt: str, cwd: str, log_path: Path) -> int:
    """Lance le CLI spécifié (sans logique de retry)."""
    say(f"[dim]Using {host} CLI[/]")
    if host == "claude":
        return run_claude_cli(prompt, cwd, log_path)
    if host == "codex":
        return run_codex_cli(prompt, cwd, log_path)
    say("[red]Gemini CLI non supporté pour NEXOS v4.4 (WIP)[/]")
    return 1


def run_cli(prompt: str, cwd: str, log_path: Path) -> int:
    """Dispatche vers le bon CLI avec retry sur rate limit (A-004).

    - Première tentative avec le host par défaut
    - Si exit non-zéro ET log contient un rate limit pattern → retry avec
      backoff exponential (30s, 2min, 8min)
    - Après tous les retries Claude, pivot vers Codex si dispo
    - Si succès en n'importe quelle étape → return 0
    - Sinon return le exit code de la dernière tentative
    """
    host = get_cli_host()
    rc = _dispatch_cli(host, prompt, cwd, log_path)
    if rc == 0:
        return 0

    if not detect_rate_limit_in_log(log_path):
        # Échec pas lié au rate limit → return immédiatement
        return rc

    say("[yellow]⚠ Rate limit détecté dans le log — A-004 retry/pivot enclenché[/]")

    for attempt, backoff_s in enumerate(_RATE_LIMIT_BACKOFF_S, start=1):
        say(
            f"[yellow]  Tentative {attempt + 1}/{len(_RATE_LIMIT_BACKOFF_S) + 1} dans {backoff_s}s...[/]"
        )
        time.sleep(backoff_s)
        rc = _dispatch_cli(host, prompt, cwd, log_path)
        if rc == 0:
            return 0
        if not detect_rate_limit_in_log(log_path):
            return rc  # nouveau type d'échec → propager

    # Tous les retries sur le host actuel ont échoué — pivot Codex si Claude
    if host == "claude" and _is_codex_available():
        say("[yellow]⚠ Rate limit Claude persistant — pivot vers Codex[/]")
        rc = _dispatch_cli("codex", prompt, cwd, log_path)
        if rc == 0:
            return 0

    return rc


__all__ = [
    "_RATE_LIMIT_PATTERNS",
    "detect_rate_limit_in_log",
    "get_cli_host",
    "run_claude_cli",
    "run_cli",
    "run_codex_cli",
]
