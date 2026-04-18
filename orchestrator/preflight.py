"""Tooling preflight — scans CLI (Lighthouse, a11y, headers, SSL, deps).

Exécute les outils CLI réels AVANT que les agents LLM interprètent les résultats.
- `run_preflight_tooling()`: déclenche `tools/preflight.sh` pour un URL externe.
- `run_preflight()`: build local + serveur Next.js + scans ciblés.
- `run_soic_gate()`: wrapper legacy autour de `soic.gate.evaluate_gate`.
- `RerunContext`: encapsule l'état nécessaire pour re-lancer une phase avec feedback SOIC.
"""

from __future__ import annotations

import contextlib
import os
import signal
import socket
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from ._shared import LOGS_DIR, NEXOS_ROOT, TOOLS_DIR, _get_default_profile, say

_SCAN_SCRIPTS: list[tuple[str, str, int]] = [
    # (script_name, output_filename, timeout_seconds)
    ("lighthouse-scan.sh", "lighthouse.json", 60),
    ("a11y-scan.sh", "a11y.json", 60),
    ("headers-scan.sh", "headers.json", 30),
    ("ssl-scan.sh", "ssl.json", 30),
]

_PREFLIGHT_TOTAL_TIMEOUT = 300  # 5 minutes


def run_preflight_tooling(client_dir: Path, url: str) -> bool:
    """Exécute les outils CLI de mesure AVANT les agents LLM."""
    say("\n[bold cyan]⚡ TOOLING PREFLIGHT[/]")

    preflight_script = TOOLS_DIR / "preflight.sh"
    if not preflight_script.exists():
        say("[yellow]⚠ tools/preflight.sh non trouvé — skip tooling[/]")
        return True

    try:
        result = subprocess.run(
            ["bash", str(preflight_script), url, str(client_dir)],
            cwd=str(NEXOS_ROOT),
            timeout=120,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            say("[green]✓[/] Tooling preflight terminé")
        else:
            say(f"[yellow]⚠[/] Tooling preflight partiel (code {result.returncode})")
            if result.stderr:
                say(f"[dim]{result.stderr[:500]}[/]")
        return True
    except subprocess.TimeoutExpired:
        say("[yellow]⚠ Tooling timeout (120s) — skip[/]")
        return True
    except Exception as e:
        say(f"[red]✗ Tooling error: {e}[/]")
        return True  # Non-bloquant


def run_soic_gate(phase: str, client_dir: Path, profile=None) -> tuple[bool, float]:
    """Exécute le quality gate SOIC pour une phase."""
    from soic.gate import evaluate_gate

    p = profile or _get_default_profile()
    threshold = p.config.phase_thresholds.get(phase)
    if threshold is None:
        # Phase 4 = BUILD PASS (binaire)
        build_log = client_dir / "ph4-build-log.md"
        if build_log.exists():
            content = build_log.read_text()
            passed = "BUILD PASS" in content or "build réussi" in content.lower()
            return passed, 10.0 if passed else 0.0
        return True, 10.0  # Assume pass si pas de log

    try:
        mu = evaluate_gate(phase, client_dir)
        passed = mu >= threshold
        return passed, mu
    except Exception as e:
        say(f"[yellow]⚠ SOIC gate error: {e} — FAIL (score inconnu)[/]")
        return False, 0.0


def _find_free_port() -> int:
    """Find a free TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def run_preflight(site_dir: Path, client_dir: Path) -> dict[str, Path]:
    """Build the site, start a local server, run scan scripts, stop the server.

    Returns a dict mapping tool names to their output JSON paths.
    Missing scripts are logged and skipped (gates will be NOT_EXECUTED).
    """
    results: dict[str, Path] = {}
    tooling_dir = client_dir / "tooling"
    tooling_dir.mkdir(exist_ok=True)

    # 1. Verify build dir
    if not (site_dir / "package.json").exists():
        say(f"[yellow]⚠ Pas de package.json dans {site_dir} — skip preflight[/]")
        return results

    # 2. Build if needed
    next_dir = site_dir / ".next"
    if not next_dir.exists():
        say("[cyan]  Building site (npm run build)...[/]")
        try:
            subprocess.run(
                ["npm", "run", "build"],
                cwd=str(site_dir),
                timeout=180,
                capture_output=True,
                text=True,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            say(f"[yellow]⚠ Build failed: {e} — skip preflight[/]")
            return results

    # 3. Start local Next.js server
    port = _find_free_port()
    local_url = f"http://localhost:{port}"
    say(f"[cyan]  Starting Next.js on port {port}...[/]")
    server_proc = None
    try:
        server_proc = subprocess.Popen(
            ["npx", "next", "start", "-p", str(port)],
            cwd=str(site_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,
        )
        # Wait for server to be ready
        for _ in range(30):
            time.sleep(1)
            try:
                with socket.create_connection(("localhost", port), timeout=1):
                    break
            except OSError:
                continue
        else:
            say("[yellow]⚠ Server did not start in 30s — skip preflight[/]")
            return results

        say(f"[green]  ✓ Server ready at {local_url}[/]")

        # 4. Run scan scripts
        preflight_start = time.monotonic()
        for script_name, output_file, timeout in _SCAN_SCRIPTS:
            elapsed = time.monotonic() - preflight_start
            if elapsed >= _PREFLIGHT_TOTAL_TIMEOUT:
                say("[yellow]⚠ Preflight total timeout (5min) — stopping scans[/]")
                break

            script_path = TOOLS_DIR / script_name
            if not script_path.exists():
                say(f"[dim]  ⊘ {script_name} not found — skip[/]")
                continue

            output_path = tooling_dir / output_file
            try:
                proc = subprocess.run(
                    ["bash", str(script_path), local_url, str(tooling_dir)],
                    cwd=str(NEXOS_ROOT),
                    timeout=timeout,
                    capture_output=True,
                    text=True,
                )
                if proc.stdout and proc.stdout.strip():
                    output_path.write_text(proc.stdout, encoding="utf-8")
                if output_path.exists() and output_path.stat().st_size > 0:
                    results[script_name] = output_path
                    say(f"[green]  ✓ {script_name} → {output_file}[/]")
                else:
                    say(f"[yellow]  ⚠ {script_name} ran but no output[/]")
            except subprocess.TimeoutExpired:
                say(f"[yellow]  ⚠ {script_name} timeout ({timeout}s)[/]")
            except Exception as e:
                say(f"[yellow]  ⚠ {script_name} error: {e}[/]")

        # 5. Deps scan (doesn't need running server)
        deps_script = TOOLS_DIR / "deps-scan.sh"
        if deps_script.exists():
            try:
                subprocess.run(
                    ["bash", str(deps_script), str(site_dir), str(client_dir)],
                    cwd=str(NEXOS_ROOT),
                    timeout=30,
                    capture_output=True,
                    text=True,
                )
                deps_out = tooling_dir / "deps.json"
                if deps_out.exists():
                    results["deps-scan.sh"] = deps_out
                    say("[green]  ✓ deps-scan.sh → deps.json[/]")
            except Exception as e:
                say(f"[yellow]  ⚠ deps-scan.sh error: {e}[/]")

    finally:
        # 6. Kill server
        if server_proc is not None:
            try:
                os.killpg(os.getpgid(server_proc.pid), signal.SIGTERM)
                server_proc.wait(timeout=5)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                with contextlib.suppress(ProcessLookupError):
                    os.killpg(os.getpgid(server_proc.pid), signal.SIGKILL)
            say("[dim]  Server stopped[/]")

    say(f"[cyan]  Preflight: {len(results)}/{len(_SCAN_SCRIPTS) + 1} scans completed[/]")
    return results


@dataclass
class RerunContext:
    """Encapsulates all state needed to re-run a phase with SOIC feedback.

    Replaces the closure approach for testability and robustness.
    """

    phase: str
    client_dir: Path
    site_dir: Path | None
    url: str | None
    timestamp: str
    stack: str = "nextjs"
    site_type: str = "vitrine"

    def rerun(self, phase: str, feedback: str, iteration: int) -> bool:
        """Re-execute the phase with SOIC feedback injected.

        Signature matches RerunCallback: (phase, feedback, iteration) -> bool.
        """
        from .cli_runner import run_cli
        from .prompts import build_phase_prompt

        # Re-run preflight tooling for QA phase
        if phase == "ph5-qa" and self.site_dir is not None:
            run_preflight(self.site_dir, self.client_dir)
        elif phase == "ph5-qa" and self.url:
            run_preflight_tooling(self.client_dir, self.url)

        rerun_prompt = build_phase_prompt(
            phase, self.client_dir, stack=self.stack, site_type=self.site_type
        )
        rerun_prompt += f"\n\n# SOIC FEEDBACK — Iteration {iteration + 1}\n{feedback}"
        rerun_log = LOGS_DIR / f"{self.timestamp}_{phase}_iter{iteration + 1}.log"
        return run_cli(rerun_prompt, str(NEXOS_ROOT), rerun_log) == 0


__all__ = [
    "RerunContext",
    "run_preflight",
    "run_preflight_tooling",
    "run_soic_gate",
]
