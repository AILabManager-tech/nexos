"""Tests pour nexos.config (phase E chantier2)."""
from __future__ import annotations

from pathlib import Path


def test_settings_import():
    from nexos.config import settings
    assert settings is not None


def test_auto_detected_repo_root():
    from nexos.config import settings
    assert settings.repo_root.is_dir()
    assert (settings.repo_root / "nexos").is_dir(), (
        "repo_root should contain the nexos package"
    )


def test_defaults_are_paths():
    from nexos.config import settings
    for attr in (
        "repo_root", "workspace_root", "clients_dir", "soic_path",
        "templates_dir", "tools_dir", "output_dir",
    ):
        val = getattr(settings, attr)
        assert isinstance(val, Path), f"settings.{attr} is not a Path"


def test_env_var_override(monkeypatch, tmp_path):
    """Une env var doit override le default."""
    custom = tmp_path / "my_repo"
    custom.mkdir()
    monkeypatch.setenv("NEXOS_REPO_ROOT", str(custom))

    # Force un rebuild via re-import
    import importlib
    import nexos.config as cfg_mod
    importlib.reload(cfg_mod)

    assert cfg_mod.settings.repo_root == custom.resolve()

    # Nettoyage : recharger sans l'override pour ne pas polluer les autres tests
    monkeypatch.delenv("NEXOS_REPO_ROOT", raising=False)
    importlib.reload(cfg_mod)


def test_no_hardcoded_jarvis_in_code():
    """Protège contre la réintroduction de chemins absolus hors-projet."""
    repo = Path(__file__).resolve().parents[1]
    # Concaténation pour éviter que ce fichier de test se déclenche lui-même.
    forbidden = "/home/" + "jarvis"
    offenders = []
    for py in repo.rglob("*.py"):
        parts = set(py.parts)
        if parts & {"__pycache__", ".venv", "archive", "node_modules"}:
            continue
        text = py.read_text(errors="replace")
        if forbidden in text:
            offenders.append(str(py.relative_to(repo)))
    assert not offenders, f"Hardcoded path found in: {offenders}"
