"""NEXOS v4.0 — Agent Registry: discovery and filtering of agent .md files.

Agents have YAML frontmatter with metadata:
    ---
    id: security-headers
    phase: ph5-qa
    tags: [security, headers, D4]
    stack: [nextjs, nuxt, generic]
    site_types: [vitrine, ecommerce, portfolio, blog, application]
    required: true
    priority: 0
    ---

Agents without frontmatter are treated as universal (required, all stacks/types).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Regex to extract YAML frontmatter between --- markers
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass
class AgentMeta:
    """Metadata for a single NEXOS agent."""

    id: str
    phase: str
    path: Path
    tags: list[str] = field(default_factory=list)
    stack: list[str] = field(default_factory=lambda: ["*"])
    site_types: list[str] = field(default_factory=lambda: ["*"])
    required: bool = True
    priority: int = 0

    @property
    def dimensions(self) -> list[str]:
        """Extract SOIC dimension tags (D1-D9) from tags list."""
        return [t for t in self.tags if re.match(r"^D\d+$", t)]

    @property
    def is_blocking(self) -> bool:
        """True if agent covers D4 (Security) or D8 (Legal)."""
        dims = set(self.dimensions)
        return bool(dims & {"D4", "D8"})


def _parse_frontmatter(content: str) -> dict[str, Any] | None:
    """Parse YAML frontmatter from a .md file content.

    Returns None if no frontmatter found.
    Uses a simple parser to avoid yaml dependency in NEXOS package.
    """
    match = _FRONTMATTER_RE.match(content)
    if not match:
        return None

    raw = match.group(1)
    result: dict[str, Any] = {}

    for line in raw.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()

        # Parse inline lists: [a, b, c]
        if value.startswith("[") and value.endswith("]"):
            items = [v.strip() for v in value[1:-1].split(",") if v.strip()]
            result[key] = items
        # Parse booleans
        elif value.lower() in ("true", "false"):
            result[key] = value.lower() == "true"
        # Parse integers
        elif value.isdigit():
            result[key] = int(value)
        else:
            result[key] = value

    return result


class AgentRegistry:
    """Discovers and indexes NEXOS agents from the agents/ directory."""

    def __init__(self, agents_dir: Path) -> None:
        self.agents_dir = agents_dir
        self._agents: list[AgentMeta] = []
        self._discover()

    def _discover(self) -> None:
        """Scan agents/ for .md files and parse their frontmatter."""
        if not self.agents_dir.is_dir():
            return

        for phase_dir in sorted(self.agents_dir.iterdir()):
            if not phase_dir.is_dir():
                continue
            phase = phase_dir.name

            for md_file in sorted(phase_dir.glob("*.md")):
                # Skip orchestrators and pipeline support files
                if md_file.name.startswith("_"):
                    continue

                content = md_file.read_text(encoding="utf-8")
                meta = _parse_frontmatter(content)

                if meta:
                    agent = AgentMeta(
                        id=meta.get("id", md_file.stem),
                        phase=meta.get("phase", phase),
                        path=md_file,
                        tags=meta.get("tags", []),
                        stack=meta.get("stack", ["*"]),
                        site_types=meta.get("site_types", ["*"]),
                        required=meta.get("required", True),
                        priority=meta.get("priority", 0),
                    )
                else:
                    # Fallback: no frontmatter → universal agent
                    agent = AgentMeta(
                        id=md_file.stem,
                        phase=phase,
                        path=md_file,
                    )

                self._agents.append(agent)

    @property
    def total(self) -> int:
        """Total number of discovered agents."""
        return len(self._agents)

    def get_agents_for_phase(
        self,
        phase: str,
        site_type: str = "vitrine",
        stack: str = "nextjs",
    ) -> list[AgentMeta]:
        """Return agents matching the given phase, site type, and stack.

        Filtering rules:
        - Phase must match exactly
        - Stack: agent matches if its stack contains the target or "*"
        - Site type: agent matches if its site_types contains the target or "*"
        - Results sorted by priority (0=critical first), then by id
        """
        result = []
        for agent in self._agents:
            if agent.phase != phase:
                continue
            if "*" not in agent.stack and stack not in agent.stack:
                continue
            if "*" not in agent.site_types and site_type not in agent.site_types:
                continue
            result.append(agent)

        result.sort(key=lambda a: (a.priority, a.id))
        return result

    def get_required_agents(self, phase: str) -> list[AgentMeta]:
        """Return all required agents for a given phase (regardless of stack/type)."""
        return [a for a in self._agents if a.phase == phase and a.required]

    def get_blocking_agents(self, phase: str) -> list[AgentMeta]:
        """Return agents that cover blocking dimensions (D4, D8)."""
        return [a for a in self._agents if a.phase == phase and a.is_blocking]

    def get_all_phases(self) -> list[str]:
        """Return unique phase names in discovery order."""
        seen: dict[str, None] = {}
        for a in self._agents:
            seen.setdefault(a.phase, None)
        return list(seen)

    def get_by_id(self, agent_id: str) -> AgentMeta | None:
        """Find an agent by its id."""
        for a in self._agents:
            if a.id == agent_id:
                return a
        return None
