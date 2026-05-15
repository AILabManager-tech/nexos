"""Test E2E minimal pour orchestrator.main() — chantier2 phase I.

Ce test est LE FILET DE SÉCURITÉ avant les phases O et P (refactor god-object
de orchestrator.py). Il valide qu'un scénario `create` minimal traverse le
dispatch argparse → résolution profil → run_pipeline sans exception, en
mockant tous les appels CLI externes (Codex/Claude/Gemini) et la machinerie
lourde de `run_pipeline`.

Si ce test casse pendant le refactor O/P, on sait immédiatement que le contrat
comportemental observable depuis l'extérieur (CLI → main) a dérivé.

Stratégie de mocking :
- `orchestrator.run_pipeline` : remplacé par un fake qui capture les appels.
  C'est la frontière saine entre le dispatch CLI (testable) et la machinerie
  pipeline lourde (qui invoquerait Codex/Claude, lit les agents .md, etc.).
- `nexos.session_launcher.launch_session` : idem pour le mode `session`.
- `subprocess.run` : interdit indirectement par `no_network` quand utilisé,
  et globalement stubé pour les modes `doctor`/`fix` qui touchent au shell.

Marqueurs : `@pytest.mark.e2e` permet `pytest -m "not e2e"` en dev rapide.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest


@pytest.mark.e2e
def test_main_create_dispatches_to_run_pipeline(
    mock_run_pipeline: list[dict[str, Any]],
    tmp_client_dir: Path,
) -> None:
    """`nexos create --client-dir <dir>` doit invoquer run_pipeline avec mode=create."""
    import orchestrator

    rc = orchestrator.main(["create", "--client-dir", str(tmp_client_dir)])

    assert rc == 0, f"main() retourne {rc}, attendu 0"
    assert len(mock_run_pipeline) == 1, "run_pipeline doit être appelé exactement 1 fois"
    call = mock_run_pipeline[0]
    # run_pipeline(mode, client_dir, url=..., profile=..., target_sections=..., color_overrides=...)
    assert call["args"][0] == "create"
    assert Path(call["args"][1]) == tmp_client_dir


@pytest.mark.e2e
def test_main_audit_dispatches_to_run_pipeline(
    mock_run_pipeline: list[dict[str, Any]],
    tmp_client_dir: Path,
) -> None:
    """`nexos audit --client-dir <dir> --url <url>` propage l'URL à run_pipeline."""
    import orchestrator

    rc = orchestrator.main(
        ["audit", "--client-dir", str(tmp_client_dir), "--url", "https://example.com"]
    )

    assert rc == 0
    assert len(mock_run_pipeline) == 1
    call = mock_run_pipeline[0]
    assert call["args"][0] == "audit"
    assert call["kwargs"].get("url") == "https://example.com"


@pytest.mark.e2e
def test_main_modify_propagates_section_targeting(
    mock_run_pipeline: list[dict[str, Any]],
    tmp_client_dir: Path,
) -> None:
    """`nexos modify --section S-001 S-003` doit transmettre target_sections."""
    import orchestrator

    rc = orchestrator.main(
        [
            "modify",
            "--client-dir",
            str(tmp_client_dir),
            "--section",
            "S-001",
            "S-003",
        ]
    )

    assert rc == 0
    assert len(mock_run_pipeline) == 1
    assert mock_run_pipeline[0]["kwargs"].get("target_sections") == ["S-001", "S-003"]


@pytest.mark.e2e
def test_main_create_propagates_colors(
    mock_run_pipeline: list[dict[str, Any]],
    tmp_client_dir: Path,
) -> None:
    """`--colors primary=#1A2B3C accent=#FFD700` doit produire un dict color_overrides."""
    import orchestrator

    rc = orchestrator.main(
        [
            "create",
            "--client-dir",
            str(tmp_client_dir),
            "--colors",
            "primary=#1A2B3C",
            "accent=#FFD700",
        ]
    )

    assert rc == 0
    assert len(mock_run_pipeline) == 1
    overrides = mock_run_pipeline[0]["kwargs"].get("color_overrides")
    assert overrides == {"primary": "#1A2B3C", "accent": "#FFD700"}


@pytest.mark.e2e
def test_main_session_dispatches_to_launch_session(
    mock_launch_session: list[dict[str, Any]],
) -> None:
    """`nexos session --print-prompt` doit invoquer launch_session sans pipeline."""
    import orchestrator

    rc = orchestrator.main(["session", "--host", "claude", "--print-prompt"])

    assert rc == 0
    assert len(mock_launch_session) == 1
    kwargs = mock_launch_session[0]["kwargs"]
    assert kwargs.get("explicit_host") == "claude"
    assert kwargs.get("print_prompt_only") is True


@pytest.mark.e2e
def test_main_doctor_runs_without_pipeline(
    mock_run_pipeline: list[dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`nexos doctor` doit appeler run_doctor et NE PAS invoquer run_pipeline."""
    import orchestrator

    doctor_called = {"value": False}

    def _fake_doctor(client: str | None = None) -> None:
        # Signature mise à jour pour matcher run_doctor(client=None) après
        # ajout du flag --client (audit dette 2026-05-15 item K, commit 0c6f1fa).
        doctor_called["value"] = True

    # `from nexos.cli_commands import run_doctor` est lazy dans main()
    import nexos.cli_commands as cli

    monkeypatch.setattr(cli, "run_doctor", _fake_doctor)

    rc = orchestrator.main(["doctor"])

    assert rc == 0
    assert doctor_called["value"] is True
    assert len(mock_run_pipeline) == 0, "doctor ne doit pas invoquer run_pipeline"


@pytest.mark.e2e
def test_main_create_without_client_dir_fails_in_non_tty(
    mock_run_pipeline: list[dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """En non-TTY, sans --client-dir / --brief / --name → exit 1."""
    import orchestrator

    # Forcer non-TTY
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)

    rc = orchestrator.main(["create"])

    assert rc == 1
    assert len(mock_run_pipeline) == 0


@pytest.mark.e2e
def test_main_create_invalid_color_format_fails(
    mock_run_pipeline: list[dict[str, Any]],
    tmp_client_dir: Path,
) -> None:
    """`--colors primary=NOTHEX` doit échouer (format invalide) avec exit 1."""
    import orchestrator

    rc = orchestrator.main(
        [
            "create",
            "--client-dir",
            str(tmp_client_dir),
            "--colors",
            "primary=NOTHEX",
        ]
    )

    assert rc == 1
    assert len(mock_run_pipeline) == 0
