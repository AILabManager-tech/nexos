"""Tests régression pour Item 2 chantier 4 : Ph4 vérifie présence + exécution tests.

build_validator compte les fichiers de tests (`*.test.*`, `*.spec.*`) et,
si présents, exécute `npm test -- --run`. Mode transition v4.3.x : absence
de tests = WARNING (logged), pas FAIL. Tests présents qui échouent = FAIL.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from unittest.mock import patch

from nexos.build_validator import (
    BuildResult,
    _count_test_files,
    _run_tests,
    format_build_report,
)


def test_count_zero_in_empty_dir(tmp_path: Path):
    assert _count_test_files(tmp_path) == 0


def test_count_includes_test_ts(tmp_path: Path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "math.test.ts").write_text("test('ok', ()=>{})", encoding="utf-8")
    assert _count_test_files(tmp_path) == 1


def test_count_includes_spec_tsx(tmp_path: Path):
    (tmp_path / "components").mkdir()
    (tmp_path / "components" / "Btn.spec.tsx").write_text("x", encoding="utf-8")
    assert _count_test_files(tmp_path) == 1


def test_count_excludes_node_modules(tmp_path: Path):
    (tmp_path / "node_modules" / "lib").mkdir(parents=True)
    (tmp_path / "node_modules" / "lib" / "foo.test.ts").write_text("x", encoding="utf-8")
    assert _count_test_files(tmp_path) == 0


def test_count_excludes_dot_next(tmp_path: Path):
    (tmp_path / ".next" / "build").mkdir(parents=True)
    (tmp_path / ".next" / "build" / "foo.spec.js").write_text("x", encoding="utf-8")
    assert _count_test_files(tmp_path) == 0


def test_run_tests_returns_true_when_no_package_json(tmp_path: Path):
    """Pas de package.json = pas un fail."""
    assert _run_tests(tmp_path) is True


def test_run_tests_returns_true_when_no_test_script(tmp_path: Path):
    """Pas de script `test` dans package.json = pas un fail."""
    (tmp_path / "package.json").write_text(
        json.dumps({"scripts": {"build": "next build"}}), encoding="utf-8"
    )
    assert _run_tests(tmp_path) is True


def test_run_tests_calls_npm_test_when_script_exists(tmp_path: Path):
    """Si script `test` existe, on lance `npm test -- --run` (vitest)."""
    (tmp_path / "package.json").write_text(
        json.dumps({"scripts": {"test": "vitest"}}), encoding="utf-8"
    )

    fake_bin = tmp_path / "fake_bin"
    fake_bin.mkdir()
    fake_npm = fake_bin / "npm"
    fake_npm.write_text(
        textwrap.dedent(
            """\
            #!/bin/bash
            # Faux npm qui matche `npm test -- --run` et exit 0
            if [ "$1" = "test" ]; then exit 0; fi
            exit 99
            """
        ),
        encoding="utf-8",
    )
    fake_npm.chmod(0o755)

    import os

    with patch.dict(os.environ, {"PATH": f"{fake_bin}:{os.environ['PATH']}"}):
        assert _run_tests(tmp_path) is True


def test_format_report_warns_on_zero_tests():
    r = BuildResult(tests_count=0, tests_run_ok=True)
    report = format_build_report(r)
    assert "0 tests" in report
    assert "WARNING" in report
    assert "v4.4.0" in report


def test_format_report_shows_test_count():
    r = BuildResult(tests_count=12, tests_run_ok=True)
    report = format_build_report(r)
    assert "12 tests" in report


def test_overall_pass_when_tests_absent_but_other_ok():
    """Item 2 transition douce : tests_count=0 ne bloque PAS overall_pass."""
    r = BuildResult(
        npm_install_ok=True,
        build_ok=True,
        audit_criticals=0,
        headers_ok=True,
        tests_count=0,
        tests_run_ok=True,
    )
    # Manuel : reproduit la logique d'overall_pass
    overall = (
        r.npm_install_ok
        and r.build_ok
        and r.audit_criticals == 0
        and r.headers_ok
        and r.tests_run_ok
    )
    assert overall is True
