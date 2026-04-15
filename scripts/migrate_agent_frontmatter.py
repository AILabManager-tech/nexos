#!/usr/bin/env python3
"""R3A Migration: Add YAML frontmatter to all NEXOS agent .md files.

Rules:
- D4/D8 agents → required: true, priority: 0
- Agents without frontmatter → fallback: required: true, stack: ["*"], site_types: ["*"]
- Phase inferred from parent directory
- Skip _orchestrator.md and _pipeline.md
"""

from pathlib import Path

AGENTS_DIR = Path(__file__).parent.parent / "agents"

# ── Dimension/tag mappings for ph5-qa agents ─────────────────────────────────
AGENT_META = {
    # ph5-qa — D4 Security (required, priority 0)
    "xss-scanner": {
        "tags": ["security", "xss", "D4"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": True,
        "priority": 0,
    },
    "security-headers": {
        "tags": ["security", "headers", "D4"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": True,
        "priority": 0,
    },
    "dep-vulnerability": {
        "tags": ["security", "dependencies", "D4"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": True,
        "priority": 0,
    },
    "csp-generator": {
        "tags": ["security", "csp", "D4"],
        "stack": ["nextjs", "nuxt"],
        "required": True,
        "priority": 0,
    },
    "ssl-auditor": {
        "tags": ["security", "ssl", "D4"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": True,
        "priority": 0,
    },
    # ph5-qa — D8 Legal (required, priority 0)
    "legal-compliance": {
        "tags": ["legal", "loi25", "D8"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": True,
        "priority": 0,
    },
    # ph5-qa — D6 Accessibility
    "a11y-auditor": {
        "tags": ["accessibility", "wcag", "D6"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 1,
    },
    "color-contrast-fixer": {
        "tags": ["accessibility", "contrast", "D6"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 1,
    },
    "keyboard-nav-tester": {
        "tags": ["accessibility", "keyboard", "D6"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 1,
    },
    # ph5-qa — D5 Performance
    "lighthouse-runner": {
        "tags": ["performance", "lighthouse", "D5"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 1,
    },
    "image-optimizer": {
        "tags": ["performance", "images", "D5"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 1,
    },
    "bundle-analyzer": {
        "tags": ["performance", "bundle", "D5"],
        "stack": ["nextjs"],
        "required": False,
        "priority": 1,
    },
    "cache-strategy": {
        "tags": ["performance", "cache", "D5"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 1,
    },
    "css-purger": {
        "tags": ["performance", "css", "D5"],
        "stack": ["nextjs", "nuxt"],
        "required": False,
        "priority": 1,
    },
    # ph5-qa — D7 SEO
    "seo-meta-auditor": {
        "tags": ["seo", "meta", "D7"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 1,
    },
    "sitemap-validator": {
        "tags": ["seo", "sitemap", "D7"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 1,
    },
    "jsonld-generator": {
        "tags": ["seo", "structured-data", "D7"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 1,
    },
    "broken-link-checker": {
        "tags": ["seo", "links", "D7"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 1,
    },
    # ph5-qa — D3 Tests
    "test-coverage-gap": {
        "tags": ["tests", "coverage", "D3"],
        "stack": ["nextjs", "nuxt"],
        "required": False,
        "priority": 1,
    },
    # ph5-qa — D2 Content
    "typo-fixer": {
        "tags": ["content", "typography", "D2"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 2,
    },
    # ph5-qa — General/D9
    "visual-qa": {
        "tags": ["qa", "consolidation", "D9"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": True,
        "priority": 1,
    },
    "deploy-master": {
        "tags": ["deployment", "release", "D9"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": True,
        "priority": 1,
    },
    "post-deploy-setup": {
        "tags": ["deployment", "post-deploy"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 2,
    },
    # ph4-build
    "project-bootstrapper": {
        "tags": ["architecture", "scaffold", "D1"],
        "stack": ["nextjs"],
        "required": True,
        "priority": 0,
    },
    "component-builder": {
        "tags": ["architecture", "components", "D1", "D9"],
        "stack": ["nextjs"],
        "required": True,
        "priority": 0,
    },
    "page-assembler": {
        "tags": ["architecture", "pages", "D1"],
        "stack": ["nextjs"],
        "required": True,
        "priority": 0,
    },
    "integration-engineer": {
        "tags": ["architecture", "integration", "D1", "D9"],
        "stack": ["nextjs"],
        "required": True,
        "priority": 0,
    },
    "build-validator": {
        "tags": ["tests", "build", "D3", "D9"],
        "stack": ["nextjs"],
        "required": True,
        "priority": 0,
    },
    "seo-asset-generator": {
        "tags": ["seo", "assets", "D7"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": False,
        "priority": 1,
    },
    # ph3-content
    "copywriter-principal": {
        "tags": ["content", "copywriting", "D2"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "seo-copywriter": {
        "tags": ["content", "seo", "D2", "D7"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "content-architect": {
        "tags": ["content", "i18n", "D1"],
        "stack": ["nextjs"],
        "required": True,
        "priority": 0,
    },
    "translator": {
        "tags": ["content", "i18n", "D2"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "content-reviewer": {
        "tags": ["content", "review", "D2"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    # ph2-design
    "design-system-architect": {
        "tags": ["design", "tokens", "D1"],
        "stack": ["nextjs", "nuxt"],
        "required": True,
        "priority": 0,
    },
    "layout-designer": {
        "tags": ["design", "wireframes", "D1"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "responsive-specialist": {
        "tags": ["design", "responsive", "D6"],
        "stack": ["nextjs", "nuxt", "generic"],
        "required": True,
        "priority": 0,
    },
    "interaction-designer": {
        "tags": ["design", "animations", "D5"],
        "stack": ["nextjs", "nuxt"],
        "required": False,
        "priority": 1,
    },
    "asset-director": {
        "tags": ["design", "assets", "D5"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    # ph1-strategy
    "solution-architect": {
        "tags": ["strategy", "architecture", "D1"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "seo-strategist": {
        "tags": ["strategy", "seo", "D7"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "scaffold-planner": {
        "tags": ["strategy", "scaffold", "D1"],
        "stack": ["nextjs"],
        "required": True,
        "priority": 0,
    },
    "information-architect": {
        "tags": ["strategy", "ia", "D1"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "brand-strategist": {
        "tags": ["strategy", "brand", "D1"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    # ph0-discovery
    "web-scout": {
        "tags": ["discovery", "competitive", "D1"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "ux-analyst": {
        "tags": ["discovery", "ux", "D6"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "tech-inspector": {
        "tags": ["discovery", "tech", "D1"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "design-critic": {
        "tags": ["discovery", "design", "D5"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "content-evaluator": {
        "tags": ["discovery", "content", "D2"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    # site-update
    "site-auditor": {
        "tags": ["audit", "baseline"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "site-modifier": {
        "tags": ["modify", "implementation"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    "repo-manager": {"tags": ["git", "workspace"], "stack": ["*"], "required": True, "priority": 0},
    "qa-reviewer": {"tags": ["qa", "review"], "stack": ["*"], "required": True, "priority": 0},
    "deployer": {
        "tags": ["deployment", "release"],
        "stack": ["*"],
        "required": True,
        "priority": 0,
    },
    # knowledge
    "hexabrief": {
        "tags": ["knowledge", "summary"],
        "stack": ["*"],
        "required": False,
        "priority": 2,
    },
}

DEFAULT_SITE_TYPES = ["vitrine", "ecommerce", "portfolio", "blog", "application"]


def build_frontmatter(agent_id: str, phase: str) -> str:
    """Build YAML frontmatter for an agent."""
    meta = AGENT_META.get(agent_id, {})
    tags = meta.get("tags", [])
    stack = meta.get("stack", ["*"])
    required = meta.get("required", True)
    priority = meta.get("priority", 0)
    site_types = DEFAULT_SITE_TYPES

    lines = [
        "---",
        f"id: {agent_id}",
        f"phase: {phase}",
        f"tags: [{', '.join(tags)}]",
        f"stack: [{', '.join(stack)}]",
        f"site_types: [{', '.join(site_types)}]",
        f"required: {'true' if required else 'false'}",
        f"priority: {priority}",
        "---",
    ]
    return "\n".join(lines)


def migrate_file(md_path: Path, phase: str, dry_run: bool = False) -> bool:
    """Add frontmatter to an agent .md file. Returns True if modified."""
    content = md_path.read_text(encoding="utf-8")

    # Skip if already has frontmatter
    if content.startswith("---"):
        return False

    agent_id = md_path.stem
    frontmatter = build_frontmatter(agent_id, phase)
    new_content = frontmatter + "\n" + content

    if dry_run:
        print(f"  [DRY] {phase}/{agent_id}")
        return True

    md_path.write_text(new_content, encoding="utf-8")
    return True


def main(dry_run: bool = False):
    """Migrate all agents in the agents/ directory."""
    modified = 0
    skipped = 0
    total = 0

    for phase_dir in sorted(AGENTS_DIR.iterdir()):
        if not phase_dir.is_dir():
            continue
        phase = phase_dir.name

        for md_file in sorted(phase_dir.glob("*.md")):
            # Skip orchestrators and pipeline files
            if md_file.name.startswith("_"):
                continue
            total += 1

            if migrate_file(md_file, phase, dry_run=dry_run):
                modified += 1
            else:
                skipped += 1

    action = "Would modify" if dry_run else "Modified"
    print(f"\n{action}: {modified} | Skipped (already has frontmatter): {skipped} | Total: {total}")


if __name__ == "__main__":
    import sys

    dry_run = "--dry-run" in sys.argv
    main(dry_run=dry_run)
