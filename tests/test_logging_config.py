"""Tests pour nexos.logging_config (chantier2 phase F)."""

from __future__ import annotations

import logging


def test_configure_idempotent():
    from nexos.logging_config import configure_logging

    configure_logging("DEBUG")
    handlers_before = len(logging.getLogger().handlers)
    configure_logging("DEBUG")
    handlers_after = len(logging.getLogger().handlers)
    assert handlers_before == handlers_after, "configure_logging n'est pas idempotent"


def test_get_logger_returns_logger():
    from nexos.logging_config import get_logger

    log = get_logger("test.nexos")
    assert isinstance(log, logging.Logger)


def test_bind_context_injects_prefix(caplog):
    from nexos.logging_config import bind_context, get_logger

    log = get_logger("test.ctx")
    with (
        caplog.at_level(logging.INFO, logger="test.ctx"),
        bind_context(log, client="clinique-aura", phase="ph2") as scoped,
    ):
        scoped.info("hello")

    messages = [r.getMessage() for r in caplog.records]
    assert any("client=clinique-aura" in m and "phase=ph2" in m and "hello" in m for m in messages)


def test_no_remaining_print_in_nexos_package():
    """Anti-regression: budget print() residuels apres phase F."""
    import pathlib
    import re

    repo = pathlib.Path(__file__).resolve().parents[1]
    nexos_pkg = repo / "nexos"
    orchestrator_pkg = repo / "orchestrator"

    def count_prints(path: pathlib.Path) -> int:
        text = path.read_text(errors="replace")
        lines = [line for line in text.splitlines() if not line.lstrip().startswith("#")]
        return sum(1 for line in lines if re.search(r"\bprint\s*\(", line))

    prints_nexos = sum(count_prints(p) for p in nexos_pkg.glob("*.py"))
    prints_orch = sum(count_prints(p) for p in orchestrator_pkg.glob("*.py"))

    assert prints_nexos <= 15, f"Trop de print() dans nexos/ ({prints_nexos} > 15)"
    assert prints_orch <= 5, f"Trop de print() dans orchestrator/ ({prints_orch} > 5)"
