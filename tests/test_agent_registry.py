"""Tests for nexos.agent_registry — discovery, parsing, filtering."""

import tempfile
from pathlib import Path

from nexos.agent_registry import AgentMeta, AgentRegistry, _parse_frontmatter


class TestParseFrontmatter:
    def test_valid_frontmatter(self):
        content = """---
id: test-agent
phase: ph5-qa
tags: [security, D4]
stack: [nextjs, nuxt]
required: true
priority: 0
---
# Agent content here
"""
        result = _parse_frontmatter(content)
        assert result is not None
        assert result["id"] == "test-agent"
        assert result["tags"] == ["security", "D4"]
        assert result["required"] is True
        assert result["priority"] == 0

    def test_no_frontmatter(self):
        content = "# Just a normal markdown file\nWith content."
        assert _parse_frontmatter(content) is None

    def test_empty_content(self):
        assert _parse_frontmatter("") is None


class TestAgentMeta:
    def test_dimensions(self):
        a = AgentMeta(id="test", phase="ph5-qa", path=Path(), tags=["security", "D4", "headers"])
        assert a.dimensions == ["D4"]

    def test_is_blocking_d4(self):
        a = AgentMeta(id="test", phase="ph5-qa", path=Path(), tags=["D4"])
        assert a.is_blocking is True

    def test_is_blocking_d8(self):
        a = AgentMeta(id="test", phase="ph5-qa", path=Path(), tags=["D8"])
        assert a.is_blocking is True

    def test_not_blocking(self):
        a = AgentMeta(id="test", phase="ph5-qa", path=Path(), tags=["D5", "D6"])
        assert a.is_blocking is False


class TestAgentRegistryDiscovery:
    """Test with the real agents/ directory."""

    def test_discovers_all_agents(self):
        agents_dir = Path(__file__).parent.parent / "agents"
        if not agents_dir.exists():
            return  # Skip if not in NEXOS tree
        r = AgentRegistry(agents_dir)
        assert r.total >= 50  # At least 50 agents

    def test_all_phases_present(self):
        agents_dir = Path(__file__).parent.parent / "agents"
        if not agents_dir.exists():
            return
        r = AgentRegistry(agents_dir)
        phases = r.get_all_phases()
        for expected in [
            "ph0-discovery",
            "ph1-strategy",
            "ph2-design",
            "ph3-content",
            "ph4-build",
            "ph5-qa",
        ]:
            assert expected in phases, f"Missing phase: {expected}"

    def test_blocking_agents_exist(self):
        agents_dir = Path(__file__).parent.parent / "agents"
        if not agents_dir.exists():
            return
        r = AgentRegistry(agents_dir)
        blocking = r.get_blocking_agents("ph5-qa")
        ids = [a.id for a in blocking]
        assert "xss-scanner" in ids
        assert "security-headers" in ids
        assert "legal-compliance" in ids

    def test_stack_filtering(self):
        agents_dir = Path(__file__).parent.parent / "agents"
        if not agents_dir.exists():
            return
        r = AgentRegistry(agents_dir)
        nextjs = r.get_agents_for_phase("ph5-qa", "vitrine", "nextjs")
        nuxt = r.get_agents_for_phase("ph5-qa", "vitrine", "nuxt")
        # nextjs should have >= nuxt (some agents are nextjs-only)
        assert len(nextjs) >= len(nuxt)


class TestAgentRegistryWithTempDir:
    """Test with a synthetic agents/ directory."""

    def _create_agents(self, tmpdir: Path):
        phase_dir = tmpdir / "ph5-qa"
        phase_dir.mkdir(parents=True)

        # Agent with frontmatter
        (phase_dir / "test-security.md").write_text("""---
id: test-security
phase: ph5-qa
tags: [security, D4]
stack: [nextjs]
required: true
priority: 0
---
# Test Security Agent
""")
        # Agent without frontmatter
        (phase_dir / "no-meta.md").write_text("# Agent without frontmatter\nContent.")

        # Orchestrator (should be skipped)
        (phase_dir / "_orchestrator.md").write_text("# Orchestrator")

    def test_discovers_both_types(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._create_agents(Path(tmpdir))
            r = AgentRegistry(Path(tmpdir))
            assert r.total == 2  # test-security + no-meta

    def test_fallback_for_no_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._create_agents(Path(tmpdir))
            r = AgentRegistry(Path(tmpdir))
            agent = r.get_by_id("no-meta")
            assert agent is not None
            assert agent.required is True  # Fallback
            assert agent.stack == ["*"]  # Universal

    def test_skips_orchestrators(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._create_agents(Path(tmpdir))
            r = AgentRegistry(Path(tmpdir))
            assert r.get_by_id("_orchestrator") is None

    def test_filtering_by_stack(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._create_agents(Path(tmpdir))
            r = AgentRegistry(Path(tmpdir))
            nextjs = r.get_agents_for_phase("ph5-qa", "vitrine", "nextjs")
            nuxt = r.get_agents_for_phase("ph5-qa", "vitrine", "nuxt")
            # test-security is nextjs-only, no-meta is universal
            assert len(nextjs) == 2
            assert len(nuxt) == 1  # Only no-meta (stack: *)

    def test_nonexistent_dir(self):
        r = AgentRegistry(Path("/nonexistent/path"))
        assert r.total == 0
