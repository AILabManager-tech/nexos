"""Tests d'intégration pour `tools/preflight.sh` (P9 D7).

Le bug original (découvert pendant l'audit Mark Systems 2026-05-17, vu en direct
pendant P8.5 vertex-pmo) : `TOOLING_DIR="$CLIENT_DIR/tooling"` était relatif.
Après `cd "$SITE_DIR"` ligne 44, la redirection `> "$TOOLING_DIR/npm-audit.json"`
cherchait à écrire dans `<SITE_DIR>/<CLIENT_DIR>/tooling/npm-audit.json` (path
résolu relativement au nouveau cwd) qui n'existait pas. Le `|| true` masquait
l'erreur et le script affichait `✓` à tort. Le fichier `npm-audit.json` n'était
jamais écrit, et les phases SOIC suivantes lisaient un état périmé.

Fix : résoudre `CLIENT_DIR` / `TOOLING_DIR` / `TOOLS_DIR` en chemins absolus via
`realpath` dès l'entête, AVANT tout `cd`.
"""

import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PREFLIGHT = REPO_ROOT / "tools" / "preflight.sh"


def _build_mock_npm(fake_bin: Path) -> None:
    """Installe un shim `npm` qui renvoie un JSON valide pour `npm audit`."""
    fake_bin.mkdir(exist_ok=True)
    npm = fake_bin / "npm"
    npm.write_text(
        "#!/bin/bash\n"
        'if [[ "$1" == "audit" && "$2" == "--json" ]]; then\n'
        '  echo \'{"metadata":{"vulnerabilities":{"high":0,"critical":0}}}\'\n'
        "  exit 0\n"
        "fi\n"
        "exit 0\n"
    )
    npm.chmod(0o755)


def _run_preflight(client_dir_relative: str, cwd: Path, env_override):
    """Lance preflight.sh depuis `cwd`, avec CLIENT_DIR passé EN RELATIF.

    Le bug D7 ne se déclenche qu'avec un CLIENT_DIR relatif (`cd "$SITE_DIR"`
    casse la résolution). Passer un chemin absolu masque le bug. Le test
    reproduit donc l'usage réel : `bash tools/preflight.sh URL clients/<slug>`
    depuis la racine repo.
    """
    env = os.environ.copy()
    env.update(env_override)
    return subprocess.run(
        ["bash", str(PREFLIGHT), "http://localhost:1", client_dir_relative],
        env=env,
        capture_output=True,
        text=True,
        cwd=str(cwd),
        timeout=60,
    )


class TestPreflightShPathResolution:
    """P9 D7 — preflight.sh doit résoudre les paths en absolu."""

    def _setup_client(self, tmp_path: Path) -> Path:
        """Structure minimale : tmp/client/site/package.json."""
        client = tmp_path / "client_factice"
        site = client / "site"
        site.mkdir(parents=True)
        (site / "package.json").write_text('{"name":"test","version":"1.0.0"}')
        return client

    def test_npm_audit_json_written_with_relative_client_dir(self, tmp_path):
        """Le bug original : CLIENT_DIR relatif → npm-audit.json non écrit."""
        self._setup_client(tmp_path)  # crée tmp_path/client_factice/site/...
        fake_bin = tmp_path / "fake_bin"
        _build_mock_npm(fake_bin)
        env = {"PATH": f"{fake_bin}:{os.environ.get('PATH', '')}"}

        # CLIENT_DIR PASSÉ EN RELATIF (déclencheur du bug D7)
        result = _run_preflight("client_factice", tmp_path, env)

        audit_path = tmp_path / "client_factice" / "tooling" / "npm-audit.json"
        assert audit_path.exists(), (
            f"npm-audit.json absent — bug D7 régressé. stderr: {result.stderr[:500]}"
        )
        data = json.loads(audit_path.read_text())
        assert "metadata" in data, f"npm-audit.json corrompu: {data}"

    def test_no_redirection_error_in_stderr(self, tmp_path):
        """Garde-fou : aucun message 'Aucun fichier ou dossier' (= erreur de
        redirection bash) ne doit apparaître. Le bug original émettait
        précisément ce message sur stderr."""
        self._setup_client(tmp_path)
        fake_bin = tmp_path / "fake_bin"
        _build_mock_npm(fake_bin)
        env = {"PATH": f"{fake_bin}:{os.environ.get('PATH', '')}"}

        result = _run_preflight("client_factice", tmp_path, env)

        assert "Aucun fichier ou dossier" not in result.stderr, (
            f"preflight.sh émet une erreur de redirection bash. stderr: {result.stderr[:500]}"
        )
        assert "No such file or directory" not in result.stderr, (
            "preflight.sh émet une erreur de redirection bash (anglais). "
            f"stderr: {result.stderr[:500]}"
        )

    def test_preflight_exit_code_zero_on_partial_tools(self, tmp_path):
        """Pattern hardening P4d : preflight ne fail jamais (tous outils
        optionnels). Doit retourner 0 même si lighthouse/pa11y/ssl absents."""
        self._setup_client(tmp_path)
        fake_bin = tmp_path / "fake_bin"
        _build_mock_npm(fake_bin)
        env = {"PATH": f"{fake_bin}:{os.environ.get('PATH', '')}"}

        result = _run_preflight("client_factice", tmp_path, env)

        assert result.returncode == 0, (
            f"preflight exit {result.returncode}, stderr: {result.stderr[:500]}"
        )

    def test_tooling_dir_created_inside_client_dir(self, tmp_path):
        """Verifie la création du dossier `tooling/` au bon endroit."""
        client = self._setup_client(tmp_path)
        fake_bin = tmp_path / "fake_bin"
        _build_mock_npm(fake_bin)
        env = {"PATH": f"{fake_bin}:{os.environ.get('PATH', '')}"}

        _run_preflight("client_factice", tmp_path, env)

        assert (client / "tooling").is_dir(), "tooling/ doit être créé sous CLIENT_DIR"
        # Pas créé sous site/ (test anti-régression du bug original)
        assert not (client / "site" / "tooling").exists(), (
            "tooling/ ne doit PAS apparaître sous site/ (= bug D7)"
        )
