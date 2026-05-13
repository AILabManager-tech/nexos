"""Entry point CLI NEXOS — dispatch des modes vers leurs implémentations."""

from __future__ import annotations

import sys
from pathlib import Path

from ._shared import _NEXOS_V4, NEXOS_ROOT, say
from .banner import print_banner
from .brief import generate_brief_from_wizard, load_runtime_brief
from .cli_args import parse_cli_args


def main(argv: list[str] | None = None) -> int:
    """NEXOS orchestrator entry point.

    Accepts an optional argv list (defaults to sys.argv[1:]) and returns the
    process exit code. Extracted from the legacy `if __name__ == "__main__":`
    block so that `nexos_cli.py` can import and call it without exec().
    """
    print_banner()
    args = parse_cli_args(argv)

    if not args.mode:
        from nexos.session_launcher import launch_session

        return int(launch_session(NEXOS_ROOT) or 0)

    if args.mode == "session":
        from nexos.session_launcher import launch_session

        return int(
            launch_session(
                NEXOS_ROOT,
                explicit_host=args.host,
                print_prompt_only=args.print_prompt,
            )
            or 0
        )

    # NEXOS v4.0 — commandes standalone
    if args.mode == "doctor":
        if _NEXOS_V4:
            from nexos.cli_commands import run_doctor

            run_doctor()
        else:
            say("[red]nexos doctor requiert les modules v4.0 (nexos/)[/]")
        return 0
    if args.mode == "module":
        if _NEXOS_V4:
            from nexos.cli_commands import run_module_command

            return int(
                run_module_command(
                    args.module_action,
                    module_id=getattr(args, "module_id", None),
                    payload_path=getattr(args, "payload", None),
                )
            )
        say("[red]nexos module requiert les modules v4.0 (nexos/)[/]")
        return 1
    if args.mode == "workflow":
        if _NEXOS_V4:
            from nexos.cli_commands import run_workflow_command

            return int(
                run_workflow_command(
                    args.workflow_action,
                    workflow_id=getattr(args, "workflow_id", None),
                    payload_path=getattr(args, "payload", None),
                )
            )
        say("[red]nexos workflow requiert les modules v4.0 (nexos/)[/]")
        return 1
    if args.mode == "fix":
        if _NEXOS_V4:
            from nexos.cli_commands import run_fix

            run_fix(args.client_dir, dry_run=args.dry_run)
        else:
            say("[red]nexos fix requiert les modules v4.0 (nexos/)[/]")
        return 0
    if args.mode == "report":
        if _NEXOS_V4:
            from nexos.cli_commands import run_report

            run_report(args.client_dir)
        else:
            say("[red]nexos report requiert les modules v4.0 (nexos/)[/]")
        return 0

    if args.mode == "knowledge":
        # Lazy import via package so tests can monkeypatch if needed.
        import orchestrator as _pkg

        _pkg.run_knowledge_agent(
            agent_id=args.agent,
            source=args.source,
            content_type=args.content_type,
            objectif=args.objectif,
            niveau=args.niveau,
            score_only=args.score_only,
        )
        return 0

    if args.mode == "converge":
        import orchestrator as _pkg

        _pkg.run_converge(
            client_dir=args.client_dir,
            target=args.target,
            max_iter=args.max_iter,
            timeout_minutes=args.timeout,
            url=args.url,
            dry_run=args.dry_run,
        )
        return 0

    # Pipeline modes: create / audit / modify / content / analyze
    if hasattr(args, "client_dir") and args.client_dir:
        client_dir = args.client_dir
    elif hasattr(args, "brief") and args.brief and not getattr(args, "interactive", False):
        brief_path = Path(args.brief)
        brief_data = load_runtime_brief(brief_path, mode=args.mode)
        client_dir = generate_brief_from_wizard(args.mode, brief_data)
    elif _NEXOS_V4:
        from nexos.brief_wizard import generate_minimal_brief, interactive_brief

        if getattr(args, "name", None):
            say(f"[cyan]ℹ Génération rapide du brief pour : {args.name}[/]")
            brief_data = generate_minimal_brief(args.name, args.mode)
            client_dir = generate_brief_from_wizard(args.mode, brief_data)
        elif getattr(args, "interactive", False) or sys.stdin.isatty():
            brief_data = interactive_brief(args.mode)
            client_dir = generate_brief_from_wizard(args.mode, brief_data)
        else:
            say("[red]Erreur: --client-dir, --brief ou --name requis (non-TTY)[/]")
            return 1
    else:
        say("[red]Erreur: --client-dir ou --brief requis[/]")
        say("[dim]Astuce : lancez nexos create en terminal pour le wizard interactif[/]")
        return 1

    # Resolve SOIC profile: --profile > --stack > brief > default
    from ._shared import _resolve_profile

    cli_profile = _resolve_profile(
        stack=getattr(args, "stack", None),
        profile_name=getattr(args, "profile", None),
    )
    if cli_profile is None:
        brief_path = client_dir / "brief-client.json"
        if brief_path.exists():
            brief_data = load_runtime_brief(brief_path)
            brief_stack = brief_data.get("stack") or brief_data.get("site", {}).get("stack")
            if brief_stack:
                cli_profile = _resolve_profile(stack=brief_stack)

    # Parse --colors if provided
    _raw_colors = getattr(args, "colors", None)
    _color_overrides = None
    if _raw_colors:
        from nexos.pipeline_config import parse_color_args

        try:
            _color_overrides = parse_color_args(_raw_colors)
            say(f"[cyan]🎨 Palette couleurs : {_color_overrides}[/]")
        except ValueError as e:
            say(f"[red]Erreur --colors : {e}[/]")
            return 1

    # Lazy call via package so tests can monkeypatch orchestrator.run_pipeline.
    import orchestrator as _pkg

    _pkg.run_pipeline(
        args.mode,
        client_dir,
        url=getattr(args, "url", None),
        profile=cli_profile,
        target_sections=getattr(args, "section", None),
        color_overrides=_color_overrides,
    )

    return 0


__all__ = ["main"]
