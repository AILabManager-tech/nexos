"""NEXOS — Configuration logging centralisee.

Configure le module ``logging`` de la stdlib avec :
- Formatter unifie (timestamp ISO + level + name + message + contexte optionnel)
- Level pilotable via ``NEXOS_LOG_LEVEL`` (cf ``nexos.config.settings``)
- Handler console (stderr) par defaut
- Hook idempotent (safe a appeler plusieurs fois)

Usage:
    from nexos.logging_config import get_logger, bind_context

    logger = get_logger(__name__)
    logger.info("Starting phase %s", phase_id)

    with bind_context(logger, client="clinique-aura", phase="ph2") as scoped:
        scoped.info("Running design agent")
"""

from __future__ import annotations

import logging
import sys
from collections.abc import Iterator
from contextlib import contextmanager

_CONFIGURED = False


def configure_logging(level: str | int = "INFO", *, force: bool = False) -> None:
    """Configure le logging global. Idempotent (safe a appeler plusieurs fois).

    Args:
        level: ``INFO`` / ``DEBUG`` / ``WARNING`` / ``ERROR`` ou niveau numerique.
        force: reconfigurer meme si deja fait.
    """
    global _CONFIGURED
    if _CONFIGURED and not force:
        return

    if isinstance(level, str):
        numeric_level = getattr(logging, level.upper(), logging.INFO)
    else:
        numeric_level = int(level)

    fmt = "%(asctime)s | %(levelname)-7s | %(name)-30s | %(message)s"
    datefmt = "%Y-%m-%dT%H:%M:%S"

    root = logging.getLogger()
    root.setLevel(numeric_level)
    root.handlers.clear()

    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setLevel(numeric_level)
    handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
    root.addHandler(handler)

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Recupere un logger normalise. Configure logging au premier appel."""
    if not _CONFIGURED:
        try:
            from nexos.config import settings

            configure_logging(settings.log_level)
        except Exception:
            configure_logging("INFO")
    return logging.getLogger(name)


class _ContextualAdapter(logging.LoggerAdapter):
    """Injecte du contexte (client, phase, ...) dans chaque log."""

    def process(self, msg, kwargs):
        if self.extra:
            extras = " ".join(f"{k}={v}" for k, v in self.extra.items())
            msg = f"[{extras}] {msg}"
        return msg, kwargs


@contextmanager
def bind_context(logger: logging.Logger, **context) -> Iterator[logging.LoggerAdapter]:
    """Ajoute temporairement du contexte (client, phase...) aux logs.

    Example:
        with bind_context(logger, client="clinique-aura", phase="ph2") as log:
            log.info("agent running")
    """
    adapter = _ContextualAdapter(logger, context)
    yield adapter


__all__ = ["bind_context", "configure_logging", "get_logger"]
