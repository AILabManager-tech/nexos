"""Procédures haut-niveau du pipeline : run_pipeline + run_converge.

Ce module encapsule les deux entrypoints procéduraux legacy :
- `run_pipeline(mode, client_dir, ...)` : itère les phases d'un mode avec
  gates SOIC, convergence iterative et auto-fix entre les phases.
- `run_converge(client_dir, ...)` : boucle autonome SOIC sur un client
  existant (correct + re-evaluate jusqu'à convergence ou abort).

Les tests E2E montent `orchestrator.run_pipeline` via monkeypatch, donc
`run_pipeline` doit rester accessible via le package (re-exporté par
`orchestrator/__init__.py`).
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from rich.panel import Panel

from ._shared import (
    _HAS_AUDIT_TOOLKIT,
    _HAS_CHANGELOG,
    _NEXOS_V4,
    LOGS_DIR,
    NEXOS_ROOT,
    OUTPUT_MAP,
    PHASES_MAP,
    _get_default_profile,
    _resolve_profile,
    say,
)
from .brief import load_runtime_brief
from .cli_runner import run_codex_cli
from .preflight import RerunContext, run_preflight, run_preflight_tooling
from .prompts import build_phase_prompt
from .verify import _fix_report_to_dict, verify_phase_output


def run_pipeline(
    mode: str,
    client_dir: Path,
    url: str | None = None,
    profile=None,
    target_sections: list[str] | None = None,
    color_overrides: dict[str, str] | None = None,
):
    """Exécute le pipeline complet pour un mode donné."""
    # Resolve phases via PipelineConfig (dynamic) or PHASES_MAP (fallback)
    brief_path = client_dir / "brief-client.json"
    brief = None
    if brief_path.exists():
        brief = load_runtime_brief(brief_path, mode=mode)

    try:
        from nexos.pipeline_config import PipelineConfig

        pipeline_cfg = PipelineConfig.from_brief(brief, mode, nexos_root=NEXOS_ROOT)
        if target_sections:
            pipeline_cfg.target_sections = target_sections
        if color_overrides:
            pipeline_cfg.color_overrides = color_overrides
        phases = pipeline_cfg.phases
    except Exception:
        pipeline_cfg = None
        phases = PHASES_MAP[mode]

    # Auto-resolve profile from pipeline stack if not provided
    if profile is None and pipeline_cfg is not None and pipeline_cfg.stack != "nextjs":
        profile = _resolve_profile(stack=pipeline_cfg.stack) or _get_default_profile()
    if profile is None:
        profile = _get_default_profile()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    gate_history = []

    # NEXOS v4.0 — Vérification tooling au démarrage
    if _NEXOS_V4:
        from nexos.tooling_manager import ensure_tooling

        ensure_tooling(interactive=False)

    say(
        Panel(
            f"[bold]Mode:[/] {mode}\n"
            f"[bold]Client:[/] {client_dir.name}\n"
            f"[bold]Phases:[/] {' → '.join(phases)}",
            title="[bold cyan]⚡ NEXOS v4.0[/]",
            border_style="cyan",
        )
    )

    if _HAS_CHANGELOG:
        from nexos.changelog import EventType, log_event

        log_event(
            client_dir,
            EventType.PIPELINE_START,
            agent="orchestrator",
            details={"mode": mode, "phases": phases},
        )

    for i, phase in enumerate(phases):
        say(f"\n[bold]{'━' * 60}[/]")
        say(f"[bold cyan]PHASE {i}: {phase.upper()}[/]")
        say(f"[bold]{'━' * 60}[/]\n")

        if _HAS_CHANGELOG:
            from nexos.changelog import EventType, log_event

            log_event(client_dir, EventType.PHASE_START, phase=phase, agent="orchestrator")

        # Detect site directory for preflight
        site_dir = client_dir / "site"
        if not (site_dir / "package.json").exists():
            site_dir = None

        # NEXOS v4.0 — Auto-fix D4/D8 avant QA (garantir compliance)
        if phase == "ph5-qa" and _NEXOS_V4 and site_dir:
            from nexos.auto_fixer import auto_fix

            brief_path = client_dir / "brief-client.json"
            brief = load_runtime_brief(brief_path, mode=mode) if brief_path.exists() else None
            fix_report = auto_fix(site_dir, client_dir, brief)
            if fix_report.total_fixes > 0:
                say(f"[cyan]  Auto-fix: {fix_report.total_fixes} corrections appliquées[/]")

        # Preflight tooling avant ph5
        if phase == "ph5-qa":
            say("[bold cyan]⚡ PREFLIGHT TOOLING[/]")
            if site_dir is not None:
                run_preflight(site_dir, client_dir)
            elif url:
                run_preflight_tooling(client_dir, url)
            else:
                say("[yellow]⚠ Pas de site_dir ni URL — preflight skip[/]")

        # NEXOS v4.0 — Audit Toolkit source-code scan (post-preflight)
        if phase == "ph5-qa" and _HAS_AUDIT_TOOLKIT and site_dir:
            say("[bold cyan]🔍 AUDIT TOOLKIT — Source Code Scan[/]")
            try:
                from audit_toolkit.config import AuditConfig
                from audit_toolkit.report import generate_json
                from audit_toolkit.scanner import run_full_audit

                toolkit_config = AuditConfig(
                    target_url=url or "",
                    source_path=str(site_dir),
                )
                audit_report = run_full_audit(str(site_dir), url or "", toolkit_config)
                tooling_dir = client_dir / "tooling"
                tooling_dir.mkdir(exist_ok=True)

                (tooling_dir / "audit-toolkit.json").write_text(
                    json.dumps(generate_json(audit_report), indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                say(
                    f"  μ={audit_report.composite_score}/10 | "
                    f"{audit_report.total_issues} issues | "
                    f"CRITICAL/HIGH: {len(audit_report.critical_issues)}"
                )
                dims = audit_report.to_dimension_scores()
                if dims:
                    dim_str = " ".join(f"{k}={v}" for k, v in sorted(dims.items()))
                    say(f"  Dimensions: {dim_str}")
                if _HAS_CHANGELOG:
                    from nexos.changelog import EventType, log_event

                    log_event(
                        client_dir,
                        EventType.TOOLING_COMPLETE,
                        phase=phase,
                        agent="audit_toolkit",
                        details={
                            "composite_score": audit_report.composite_score,
                            "total_issues": audit_report.total_issues,
                            "dimensions": dims,
                        },
                    )
            except Exception as e:
                say(f"[yellow]⚠ Audit Toolkit error: {e}[/]")
                if _HAS_CHANGELOG:
                    from nexos.changelog import EventType, log_event

                    log_event(
                        client_dir,
                        EventType.TOOLING_ERROR,
                        phase=phase,
                        agent="audit_toolkit",
                        details={"error": str(e)},
                    )

        # Resolve stack/site_type from pipeline config
        _stack = pipeline_cfg.stack if pipeline_cfg else "nextjs"
        _site_type = pipeline_cfg.site_type if pipeline_cfg else "vitrine"

        # Construire le prompt
        prompt = build_phase_prompt(
            phase,
            client_dir,
            stack=_stack,
            site_type=_site_type,
            target_sections=pipeline_cfg.target_sections if pipeline_cfg else None,
            color_overrides=pipeline_cfg.color_overrides if pipeline_cfg else None,
        )
        log_path = LOGS_DIR / f"{timestamp}_{phase}.log"

        # Exécuter Codex CLI
        returncode = run_codex_cli(prompt, str(NEXOS_ROOT), log_path)

        if returncode != 0:
            say(f"[red]✗ Phase {phase} échouée (code {returncode})[/]")
            if _HAS_CHANGELOG:
                from nexos.changelog import EventType, log_event

                log_event(
                    client_dir,
                    EventType.PHASE_FAIL,
                    phase=phase,
                    agent="orchestrator",
                    details={"returncode": returncode},
                )
            break

        # Vérifier que l'output existe et est valide
        if phase in OUTPUT_MAP and not verify_phase_output(phase, client_dir):
            say(f"[red]✗ Phase {phase} n'a pas produit de rapport valide — ARRÊT[/]")
            if _HAS_CHANGELOG:
                from nexos.changelog import EventType, log_event

                log_event(
                    client_dir,
                    EventType.PHASE_FAIL,
                    phase=phase,
                    agent="orchestrator",
                    details={"reason": "missing_output"},
                )
            break

        # Quality gate with convergence loop
        phase_thresholds = profile.config.phase_thresholds
        if phase in phase_thresholds or phase == "ph4-build":
            threshold = phase_thresholds.get(phase)

            # Phase 4 = BUILD PASS (binary check, no convergence)
            if threshold is None:
                if _NEXOS_V4 and site_dir:
                    from nexos.auto_fixer import auto_fix
                    from nexos.build_validator import format_build_report, validate_build

                    build_result = validate_build(site_dir)
                    build_ok = build_result.overall_pass
                    if not build_ok:
                        say("[cyan]  Build FAIL — tentative auto-fix...[/]")
                        brief_path = client_dir / "brief-client.json"
                        brief = (
                            load_runtime_brief(brief_path, mode=mode)
                            if brief_path.exists()
                            else None
                        )
                        fix_report = auto_fix(site_dir, client_dir, brief)
                        say(f"[cyan]  Auto-fix: {fix_report.total_fixes} corrections[/]")
                        if _HAS_CHANGELOG:
                            from nexos.changelog import EventType, log_event

                            log_event(
                                client_dir,
                                EventType.AUTOFIX_END,
                                phase=phase,
                                agent="auto_fixer",
                                details=_fix_report_to_dict(fix_report),
                            )
                        build_result = validate_build(site_dir)
                        build_ok = build_result.overall_pass
                    say(format_build_report(build_result))
                    if _HAS_CHANGELOG:
                        from nexos.changelog import EventType, log_event

                        evt = EventType.BUILD_PASS if build_ok else EventType.BUILD_FAIL
                        log_event(client_dir, evt, phase=phase, agent="build_validator")
                else:
                    build_log = client_dir / "ph4-build-log.md"
                    if build_log.exists():
                        content = build_log.read_text()
                        build_ok = "BUILD PASS" in content or "build réussi" in content.lower()
                    else:
                        build_ok = True
                gate_history.append(
                    {
                        "phase": phase,
                        "mu": 10.0 if build_ok else 0.0,
                        "threshold": "BUILD_PASS",
                        "converged": build_ok,
                        "iterations": 1,
                        "decision": "ACCEPT" if build_ok else "FAIL",
                        "timestamp": datetime.now().isoformat(),
                    }
                )
                if not build_ok:
                    say("[red]✗ BUILD FAIL — ARRÊT[/]")
                    break
                say("[green]✓ BUILD PASS[/]")
                continue

            # Convergence loop via PhaseIterator
            from soic.iterator import PhaseIterator
            from soic.persistence import RunStore

            store = RunStore(client_dir)
            iterator = PhaseIterator(
                phase=phase,
                client_dir=str(client_dir),
                max_iter=4,
                store=store,
                site_dir=str(site_dir) if site_dir else None,
            )

            ctx = RerunContext(
                phase=phase,
                client_dir=client_dir,
                site_dir=site_dir,
                url=url,
                timestamp=timestamp,
                stack=_stack,
                site_type=_site_type,
            )

            def _on_iteration(iteration: int, result) -> None:
                """Display iteration progress."""
                decision = result.decision.value
                mu = result.report.mu
                cov = result.report.coverage
                say(
                    f"  [bold]Iteration {iteration}:[/] μ={mu:.2f} "
                    f"(coverage={cov:.0%}) → {decision}"
                )

            say(f"\n[bold cyan]🔄 SOIC Convergence Loop ({phase})[/]")
            loop = iterator.run(rerun_phase=ctx.rerun, on_iteration=_on_iteration)

            gate_history.append(
                {
                    "phase": phase,
                    "mu": loop.final_mu,
                    "threshold": threshold,
                    "converged": loop.converged,
                    "iterations": loop.total_iterations,
                    "decision": loop.final_decision.value,
                    "abort_reason": loop.abort_reason,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            if _HAS_CHANGELOG:
                from nexos.changelog import EventType, log_event

                gate_evt = EventType.SOIC_GATE_PASS if loop.converged else EventType.SOIC_GATE_FAIL
                log_event(
                    client_dir,
                    gate_evt,
                    phase=phase,
                    agent="soic",
                    details={
                        "mu": loop.final_mu,
                        "threshold": threshold,
                        "iterations": loop.total_iterations,
                    },
                )

            if loop.converged:
                say(
                    f"[green]✓ SOIC GATE: μ={loop.final_mu:.2f} ≥ {threshold} "
                    f"— ACCEPT ({loop.total_iterations} iter)[/]"
                )
            else:
                say(
                    f"[red]✗ SOIC GATE: μ={loop.final_mu:.2f} < {threshold} "
                    f"— {loop.final_decision.value} ({loop.total_iterations} iter)[/]"
                )
                if loop.abort_reason:
                    say(f"[red]  Raison: {loop.abort_reason}[/]")
                break

    # Sauvegarder l'historique des gates (enrichi avec convergence)
    gates_path = client_dir / "soic-gates.json"
    gates_path.write_text(json.dumps(gate_history, indent=2), encoding="utf-8")

    if _HAS_CHANGELOG:
        from nexos.changelog import EventType, log_event

        log_event(
            client_dir,
            EventType.PIPELINE_END,
            agent="orchestrator",
            details={"gates": len(gate_history), "mode": mode},
        )

    say(
        Panel(
            f"[green]Pipeline terminé[/]\n"
            f"[dim]Client: {client_dir}[/]\n"
            f"[dim]Gates: {len(gate_history)} évaluées[/]",
            title="[bold green]✓ NEXOS v3.0 TERMINÉ[/]",
            border_style="green",
        )
    )


def run_converge(
    client_dir: Path,
    target: float = 8.5,
    max_iter: int = 4,
    timeout_minutes: int = 15,
    url: str | None = None,
    dry_run: bool = False,
    profile=None,
) -> None:
    """Run the SOIC convergence loop on an existing client directory.

    Default: full autonomous loop — evaluate → correct → re-evaluate → repeat.
    With --dry-run: evaluate once, produce report + corrective plan, touch nothing.
    """
    from soic import Converger, FeedbackRouter, GateEngine, PhaseIterator
    from soic.persistence import RunStore
    from soic.report import generate_report_v2

    if profile is None:
        profile = _get_default_profile()

    phase = "ph5-qa"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    converge_profile = type(profile)(
        name=f"{profile.name}@converge",
        config=profile.config.with_threshold(phase, target),
        parent=profile,
    )

    site_dir = client_dir
    if (client_dir / "site" / "package.json").exists():
        site_dir = client_dir / "site"
    elif not (client_dir / "package.json").exists():
        site_dir = None

    say(
        Panel(
            f"[bold]Mode:[/] converge\n"
            f"[bold]Client:[/] {client_dir.name}\n"
            f"[bold]Target:[/] μ ≥ {target}\n"
            f"[bold]Max iterations:[/] {max_iter}\n"
            f"[bold]Timeout:[/] {timeout_minutes}min\n"
            f"[bold]Mode:[/] {'DRY-RUN (evaluate only)' if dry_run else 'AUTONOMOUS (correct + re-evaluate)'}",
            title="[bold cyan]🔄 NEXOS SOIC Convergence[/]",
            border_style="cyan",
        )
    )

    if dry_run:
        say(f"\n[bold cyan]⚡ Evaluation SOIC — {phase}[/]\n")

        if site_dir is not None and (site_dir / "package.json").exists():
            say("[bold cyan]⚡ PREFLIGHT TOOLING[/]")
            run_preflight(site_dir, client_dir)
        elif url:
            say("[bold cyan]⚡ PREFLIGHT TOOLING (URL)[/]")
            run_preflight_tooling(client_dir, url)

        engine = GateEngine(
            phase=phase,
            client_dir=str(client_dir),
            site_dir=str(site_dir) if site_dir else str(client_dir),
            profile=converge_profile,
        )
        report = engine.run_all_gates(iteration=1)

        report_txt = generate_report_v2(report, config=converge_profile.config)
        say(report_txt)

        report_path = client_dir / "soic-converge-report.txt"
        report_path.write_text(report_txt, encoding="utf-8")

        router = FeedbackRouter(config=converge_profile.config)
        if report.fail_count > 0:
            feedback = router.generate(report)
            say(f"\n[bold yellow]{'━' * 60}[/]")
            say("[bold yellow]PLAN DE CONVERGENCE[/]")
            say(f"[bold yellow]{'━' * 60}[/]\n")
            say(feedback)

            full_feedback = router.generate_full(report)
            feedback_path = client_dir / "soic-converge-feedback.md"
            feedback_path.write_text(full_feedback, encoding="utf-8")
            say(f"\n[dim]Feedback complet sauvegardé: {feedback_path}[/]")

        converger = Converger(phase=phase, max_iter=max_iter, config=converge_profile.config)
        decision = converger.decide(report, iteration=1)
        summary = converger.get_summary(decision, iteration=1)

        say(f"\n[bold]{'━' * 60}[/]")
        if decision.value == "ACCEPT":
            say(f"[bold green]✓ CONVERGED — μ={report.mu:.2f} ≥ {target}[/]\n[green]{summary}[/]")
        else:
            delta = target - report.mu
            say(
                f"[bold red]✗ NOT CONVERGED — μ={report.mu:.2f} < {target} (Δ={delta:.2f})[/]\n"
                f"[red]{summary}[/]"
            )
            say(
                f"\n[dim]Pour lancer la correction automatique :[/]\n"
                f"[cyan]  nexos converge {client_dir} --target {target} "
                f"--max-iter {max_iter} --timeout {timeout_minutes}[/]"
            )
        say(f"[bold]{'━' * 60}[/]")

        store = RunStore(client_dir)
        store.save_run(report)

    else:
        store = RunStore(client_dir)
        iterator = PhaseIterator(
            phase=phase,
            client_dir=str(client_dir),
            max_iter=max_iter,
            store=store,
            site_dir=str(site_dir) if site_dir else None,
            timeout_minutes=timeout_minutes,
            profile=converge_profile,
        )

        ctx = RerunContext(
            phase=phase,
            client_dir=client_dir,
            site_dir=site_dir,
            url=url,
            timestamp=timestamp,
        )

        def _on_iteration(iteration: int, result) -> None:
            mu = result.report.mu
            cov = result.report.coverage
            dec = result.decision.value
            dur = result.duration_s
            say(
                f"  [bold]Iteration {iteration}:[/] μ={mu:.2f} "
                f"(coverage={cov:.0%}, {dur:.0f}s) → {dec}"
            )
            if result.feedback and dec == "ITERATE":
                for line in result.feedback.split("\n")[:5]:
                    if line.strip():
                        say(f"    [dim]{line}[/]")

        say(f"\n[bold cyan]🔄 Convergence Loop — target μ ≥ {target}[/]\n")
        loop = iterator.run(rerun_phase=ctx.rerun, on_iteration=_on_iteration)

        if loop.iterations:
            last_report = loop.iterations[-1].report
            report_txt = generate_report_v2(last_report, config=converge_profile.config)
            report_path = client_dir / "soic-converge-report.txt"
            report_path.write_text(report_txt, encoding="utf-8")

        say(f"\n[bold]{'━' * 60}[/]")
        if loop.converged:
            say(
                f"[bold green]✓ CONVERGED — μ={loop.final_mu:.2f} ≥ {target} "
                f"in {loop.total_iterations} iteration(s)[/]"
            )
        else:
            say(
                f"[bold red]✗ NOT CONVERGED — μ={loop.final_mu:.2f} < {target} "
                f"after {loop.total_iterations} iteration(s)[/]\n"
                f"[red]  Reason: {loop.abort_reason or loop.final_decision.value}[/]"
            )
        say(f"[bold]{'━' * 60}[/]")


__all__ = ["run_converge", "run_pipeline"]
