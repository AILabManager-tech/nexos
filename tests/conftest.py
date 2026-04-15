"""Fixtures partagées pour la suite de tests NEXOS (chantier2 phase I).

Centralise ce qui était dupliqué dans les test_*.py individuels :
- structure client minimale (`tmp_client_dir`)
- brief valide en mémoire (`sample_brief`)
- garde-fous globaux (env isolé, refus du réseau, mock du session_launcher)

Aucune fixture ne casse les tests existants : `tmp_client_dir` est purement
additif, et `nexos_test_env` (autouse) ne modifie que les variables d'env
qui n'impactent pas les modules déjà importés.
"""

from __future__ import annotations

import json
import socket
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def tmp_client_dir(tmp_path: Path) -> Path:
    """Dossier client isolé pour un test (structure minimale NEXOS)."""
    client = tmp_path / "test-client"
    (client / "site").mkdir(parents=True)
    (client / "tooling").mkdir()
    # Brief conforme au contrat canonique (cf. nexos.brief_contract.validate_brief).
    (client / "brief-client.json").write_text(
        json.dumps(
            {
                "client": {"name": "Test Client Inc.", "slug": "test-client"},
                "legal": {
                    "company_name": "Test Client Inc.",
                    "address": "1 rue Test, Montréal QC",
                    "phone": "+1 514 000 0000",
                    "email": "contact@test.ca",
                    "rpp_name": "Test RPP",
                    "rpp_email": "rpp@test.ca",
                    "rpp_title": "Responsable",
                    "retention": "12 mois",
                    "transfer_outside_qc": False,
                    "cookie_consent": "opt-in",
                },
                "site": {
                    "stack": "nextjs",
                    "type": "vitrine",
                    "pages": ["accueil", "contact"],
                    "languages": ["fr", "en"],
                    "features": [],
                },
            }
        ),
        encoding="utf-8",
    )
    (client / "section-manifest.json").write_text(json.dumps({"sections": []}), encoding="utf-8")
    (client / "soic-gates.json").write_text(json.dumps({"mu": 0.0, "gates": []}), encoding="utf-8")
    return client


@pytest.fixture
def sample_brief() -> dict[str, Any]:
    """Dict brief minimal valide pour les tests qui consomment un brief."""
    return {
        "client": {
            "slug": "sample",
            "sector_declared": "restaurant",
            "positioning": "premium",
        },
        "goals": {"primary_kpi": "conversion"},
    }


@pytest.fixture
def no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """Refuse toute tentative d'appel réseau dans un test (sécurité CI)."""

    def _no_network(*args: Any, **kwargs: Any) -> None:
        raise RuntimeError("Network access forbidden in tests. Mock your HTTP/socket calls.")

    monkeypatch.setattr(socket, "create_connection", _no_network)
    monkeypatch.setattr(socket.socket, "connect", _no_network)


@pytest.fixture(autouse=True)
def nexos_test_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Applique un env isolé à chaque test (autouse=True).

    - Force `NEXOS_LOG_LEVEL=WARNING` pour silencer les logs en test.
    - Force `NEXOS_OUTPUT_DIR` dans `tmp_path` pour isoler les tests qui
      pourraient écrire dans le repo.

    Ne casse rien : `nexos.config.settings` est un singleton immuable
    construit à l'import — ces variables n'auront d'effet que sur les
    modules qui (re)lisent l'environnement explicitement (ex : tests
    de `nexos.config` qui font reload).
    """
    monkeypatch.setenv("NEXOS_LOG_LEVEL", "WARNING")
    monkeypatch.setenv("NEXOS_OUTPUT_DIR", str(tmp_path / "output"))


@pytest.fixture
def mock_run_pipeline(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    """Mock `orchestrator.run_pipeline` pour tester le dispatch CLI sans
    exécuter le pipeline réel (qui invoquerait Codex/Claude/Gemini).

    Retourne la liste des appels capturés pour assertions dans le test.
    """
    calls: list[dict[str, Any]] = []

    def _fake_run_pipeline(*args: Any, **kwargs: Any) -> None:
        calls.append({"args": args, "kwargs": kwargs})

    import orchestrator

    monkeypatch.setattr(orchestrator, "run_pipeline", _fake_run_pipeline)
    return calls


@pytest.fixture
def mock_launch_session(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    """Mock `nexos.session_launcher.launch_session` pour tester le dispatch
    `nexos session` sans réellement lancer un CLI hôte (codex/claude/gemini).
    """
    calls: list[dict[str, Any]] = []

    def _fake_launch(*args: Any, **kwargs: Any) -> int:
        calls.append({"args": args, "kwargs": kwargs})
        return 0

    import nexos.session_launcher as sl

    monkeypatch.setattr(sl, "launch_session", _fake_launch)
    # Patcher aussi la référence locale potentiellement déjà importée
    # dans orchestrator (import lazy : pas besoin pour le moment).
    return calls
