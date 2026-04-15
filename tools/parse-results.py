#!/usr/bin/env python3
"""
Agrège tous les résultats de tooling en un seul rapport.
Usage: python parse-results.py <tooling_dir>
"""

import json
import sys
from pathlib import Path


def parse_tooling(tooling_dir: Path) -> dict:
    """Parse tous les JSON de tooling et produit un résumé."""
    summary = {"tools_run": [], "scores": {}, "findings": []}

    # Lighthouse
    lh_path = tooling_dir / "lighthouse.json"
    if lh_path.exists():
        try:
            lh = json.loads(lh_path.read_text())
            cats = lh.get("categories", {})
            summary["scores"]["lighthouse"] = {
                cat: round(info.get("score", 0) * 100) for cat, info in cats.items()
            }
            summary["tools_run"].append("lighthouse")
        except Exception:
            pass

    # Headers
    headers_path = tooling_dir / "headers.json"
    if headers_path.exists():
        try:
            headers = json.loads(headers_path.read_text())
            required = [
                "x-content-type-options",
                "x-frame-options",
                "referrer-policy",
                "permissions-policy",
                "strict-transport-security",
                "content-security-policy",
            ]
            present = [h for h in required if h in {k.lower() for k in headers}]
            missing = [h for h in required if h not in {k.lower() for k in headers}]
            summary["scores"]["security_headers"] = {
                "present": len(present),
                "total": len(required),
                "missing": missing,
            }
            summary["tools_run"].append("curl-headers")
        except Exception:
            pass

    # npm audit
    audit_path = tooling_dir / "npm-audit.json"
    if audit_path.exists():
        try:
            audit = json.loads(audit_path.read_text())
            vulns = audit.get("metadata", {}).get("vulnerabilities", {})
            summary["scores"]["npm_audit"] = vulns
            summary["tools_run"].append("npm-audit")
        except Exception:
            pass

    # pa11y
    pa11y_path = tooling_dir / "pa11y.json"
    if pa11y_path.exists():
        try:
            pa11y = json.loads(pa11y_path.read_text())
            if isinstance(pa11y, list):
                by_type = {}
                for issue in pa11y:
                    t = issue.get("type", "unknown")
                    by_type[t] = by_type.get(t, 0) + 1
                summary["scores"]["pa11y"] = by_type
            summary["tools_run"].append("pa11y")
        except Exception:
            pass

    return summary


if __name__ == "__main__":
    tooling_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path()
    result = parse_tooling(tooling_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))
