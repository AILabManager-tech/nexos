#!/usr/bin/env python3
"""NEXOS CLI entry point.

Thin wrapper around orchestrator.main() — no exec(), no arbitrary code
execution. Replaces the legacy `exec(open(orchestrator.py).read())` pattern
with a proper import (chantier2 phase B).

Usage: nexos [command] [args...]
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Resolve symlinks so the CLI can be invoked from /usr/local/bin/nexos etc.
REPO_ROOT = Path(os.path.realpath(__file__)).parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Keep CWD stable for agents / pipeline that assume NEXOS root as cwd.
os.chdir(REPO_ROOT)
# Rename argv[0] so argparse / --help display `nexos`, not the full path.
sys.argv[0] = "nexos"


def main(argv: list[str] | None = None) -> int:
    """Entry point for the `nexos` CLI.

    Returns the exit code of the orchestrator. Prefers orchestrator.main()
    when available; falls back to runpy.run_path() as a last resort (still
    safer than exec(open().read()) since runpy compiles, sets __name__
    correctly, and does not pollute the caller namespace).
    """
    from nexos.config import settings
    from nexos.logging_config import configure_logging, get_logger

    configure_logging(settings.log_level)

    log = get_logger("nexos.cli")
    argv = argv if argv is not None else sys.argv[1:]
    log.debug("nexos cli start argv=%s log_level=%s", argv, settings.log_level)

    import orchestrator

    runner = getattr(orchestrator, "main", None)
    if callable(runner):
        rc = runner(argv)
        return int(rc) if rc is not None else 0

    import runpy

    orchestrator_path = REPO_ROOT / "orchestrator.py"
    old_argv = sys.argv[:]
    sys.argv = ["orchestrator", *argv]
    try:
        runpy.run_path(str(orchestrator_path), run_name="__main__")
    finally:
        sys.argv = old_argv
    return 0


if __name__ == "__main__":
    sys.exit(main())
