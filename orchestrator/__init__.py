"""NEXOS orchestrator package.

Re-exports the public API previously exposed by the monolithic
`orchestrator.py`. After the chantier2-P refactor, the code lives in
focused submodules — this `__init__` keeps `import orchestrator`,
`from orchestrator import X` and monkeypatch-based test setups
working unchanged.
"""

from __future__ import annotations

# ── Shared helpers (constants + console + profile resolution) ────────────────
from ._shared import (
    AGENTS_DIR,
    CLIENTS_DIR,
    KNOWLEDGE_DIR,
    LOGS_DIR,
    NEXOS_ROOT,
    OUTPUT_MAP,
    PHASES_CREATE,
    PHASES_MAP,
    TOOLS_DIR,
    VALID_NIVEAUX,
    VALID_OBJECTIFS,
    VALID_TYPES,
    _get_default_profile,
    _resolve_profile,
    console,
    logger,
    say,
)

# ── Brief lifecycle ──────────────────────────────────────────────────────────
from .brief import (
    generate_brief,
    generate_brief_from_wizard,
    load_runtime_brief,
    slugify,
)

# ── CLI runners ──────────────────────────────────────────────────────────────
from .cli_runner import run_claude_cli, run_codex_cli

# ── Converge loop (class) ────────────────────────────────────────────────────
from .converge import ConvergeLoop

# ── Gates (class + dataclass) ────────────────────────────────────────────────
from .gates import GateEngine, GateResult

# ── Knowledge agents ─────────────────────────────────────────────────────────
from .knowledge import run_knowledge_agent

# ── Entrypoint ───────────────────────────────────────────────────────────────
from .main import main

# ── Phase runners (procedural) ───────────────────────────────────────────────
from .phases import run_converge, run_pipeline

# ── Pipeline orchestrator (class + dataclasses) ──────────────────────────────
from .pipeline import (
    PhaseRun,
    PhaseStatus,
    PipelineContext,
    PipelineOrchestrator,
)

# ── Preflight tooling ────────────────────────────────────────────────────────
from .preflight import (
    RerunContext,
    run_preflight,
    run_preflight_tooling,
    run_soic_gate,
)

# ── Prompt building ──────────────────────────────────────────────────────────
from .prompts import build_phase_prompt

# ── Output verification ──────────────────────────────────────────────────────
from .verify import verify_phase_output

__all__ = [
    "AGENTS_DIR",
    "CLIENTS_DIR",
    "KNOWLEDGE_DIR",
    "LOGS_DIR",
    "NEXOS_ROOT",
    "OUTPUT_MAP",
    "PHASES_CREATE",
    "PHASES_MAP",
    "TOOLS_DIR",
    "VALID_NIVEAUX",
    "VALID_OBJECTIFS",
    "VALID_TYPES",
    "ConvergeLoop",
    "GateEngine",
    "GateResult",
    "PhaseRun",
    "PhaseStatus",
    "PipelineContext",
    "PipelineOrchestrator",
    "RerunContext",
    "_get_default_profile",
    "_resolve_profile",
    "build_phase_prompt",
    "console",
    "generate_brief",
    "generate_brief_from_wizard",
    "load_runtime_brief",
    "logger",
    "main",
    "run_claude_cli",
    "run_codex_cli",
    "run_converge",
    "run_knowledge_agent",
    "run_pipeline",
    "run_preflight",
    "run_preflight_tooling",
    "run_soic_gate",
    "say",
    "slugify",
    "verify_phase_output",
]
