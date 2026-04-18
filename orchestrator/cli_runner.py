"""Exécution CLI — lance l'agent LLM (Claude, Codex, ou Gemini) et capture sa sortie."""

from __future__ import annotations

import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from ._shared import say

_CODEX_CLI_TIMEOUT = 1800  # 30 minutes par phase


def get_cli_host() -> str:
    """Détermine quel CLI hôte utiliser.

    Ordre de préférence :
    1. NEXOS_LLM_HOST env var (claude, codex, gemini)
    2. Détection automatique : claude > codex > gemini
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

    # Fallback : default to codex
    return "codex"


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
    cmd = ["claude", "eval", "-"]

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


def run_cli(prompt: str, cwd: str, log_path: Path) -> int:
    """Dispatche vers le bon CLI (claude, codex, ou gemini) en fonction de l'env."""
    host = get_cli_host()
    say(f"[dim]Using {host} CLI[/]")
    if host == "claude":
        return run_claude_cli(prompt, cwd, log_path)
    elif host == "codex":
        return run_codex_cli(prompt, cwd, log_path)
    else:  # gemini
        say("[red]Gemini CLI non supporté pour NEXOS v4.0 (WIP)[/]")
        return 1


__all__ = ["get_cli_host", "run_claude_cli", "run_cli", "run_codex_cli"]
