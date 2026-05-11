"""Tests régression pour tools/freeze-archive.sh + audit-archive-integrity.sh.

Implémentation Phase 1 du RFC_FIXTURE_DRIFT.md (A-009) : empêcher la dérive
silencieuse des fixtures `archive/*` en gelant un manifest sha256 et en
auditant l'intégrité à la demande.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FREEZE = REPO_ROOT / "tools" / "freeze-archive.sh"
AUDIT = REPO_ROOT / "tools" / "audit-archive-integrity.sh"


def _make_archive(tmp_path: Path, files: dict[str, str]) -> Path:
    """Crée un faux dossier archive/ avec les fichiers donnés."""
    archive_dir = tmp_path / "archive_test"
    archive_dir.mkdir()
    for relpath, content in files.items():
        path = archive_dir / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return archive_dir


def test_freeze_creates_checksum_manifest(tmp_path: Path):
    archive_dir = _make_archive(tmp_path, {"a.txt": "alpha", "sub/b.md": "bravo"})
    result = subprocess.run(
        ["bash", str(FREEZE), str(archive_dir), "test source"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0
    manifest_path = archive_dir / ".archive-checksum.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text())
    assert manifest["source"] == "test source"
    assert set(manifest["files"].keys()) == {"a.txt", "sub/b.md"}
    assert all("sha256" in f and "size_bytes" in f for f in manifest["files"].values())


def test_audit_passes_on_unchanged_archive(tmp_path: Path):
    archive_dir = _make_archive(tmp_path, {"a.txt": "alpha", "b.md": "bravo"})
    subprocess.run([str(FREEZE), str(archive_dir), "src"], check=True, timeout=10)

    result = subprocess.run(
        ["bash", str(AUDIT), str(archive_dir)], capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0
    assert "PASS" in result.stdout
    assert "2 fichiers conformes" in result.stdout


def test_audit_fails_on_modified_file(tmp_path: Path):
    archive_dir = _make_archive(tmp_path, {"a.txt": "alpha"})
    subprocess.run([str(FREEZE), str(archive_dir), "src"], check=True, timeout=10)

    # Modifier le fichier après le freeze
    (archive_dir / "a.txt").write_text("alpha MODIFIED", encoding="utf-8")

    result = subprocess.run(
        ["bash", str(AUDIT), str(archive_dir)], capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 3
    assert "FAIL" in result.stdout
    assert "DRIFT" in result.stdout


def test_audit_fails_on_missing_file(tmp_path: Path):
    archive_dir = _make_archive(tmp_path, {"a.txt": "alpha", "b.md": "bravo"})
    subprocess.run([str(FREEZE), str(archive_dir), "src"], check=True, timeout=10)

    # Supprimer un fichier après le freeze
    (archive_dir / "b.md").unlink()

    result = subprocess.run(
        ["bash", str(AUDIT), str(archive_dir)], capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 3
    assert "MISSING" in result.stdout


def test_audit_fails_when_manifest_absent(tmp_path: Path):
    archive_dir = tmp_path / "no_manifest"
    archive_dir.mkdir()
    (archive_dir / "a.txt").write_text("x", encoding="utf-8")

    result = subprocess.run(
        ["bash", str(AUDIT), str(archive_dir)], capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 2
    assert "manifest" in result.stdout.lower() or "checksum" in result.stdout.lower()


def test_audit_fails_when_archive_dir_missing(tmp_path: Path):
    result = subprocess.run(
        ["bash", str(AUDIT), str(tmp_path / "does_not_exist")],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 1


def test_freeze_ignores_existing_checksum_file(tmp_path: Path):
    """Le freeze ne doit pas hasher son propre fichier manifest."""
    archive_dir = _make_archive(tmp_path, {"a.txt": "alpha"})
    subprocess.run([str(FREEZE), str(archive_dir), "src1"], check=True, timeout=10)

    # Re-freeze
    subprocess.run([str(FREEZE), str(archive_dir), "src2"], check=True, timeout=10)
    manifest = json.loads((archive_dir / ".archive-checksum.json").read_text())
    assert ".archive-checksum.json" not in manifest["files"]
    assert manifest["source"] == "src2"
