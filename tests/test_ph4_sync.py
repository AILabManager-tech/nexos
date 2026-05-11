"""Tests régression pour orchestrator.ph4_sync (A-002).

Couvre BUG_NEXOS_PH4_RACE_CONDITION : sans cette barrière, le checker SOIC
ph4 tournait sur un état intermédiaire (agent encore en train d'écrire).
La fonction `wait_for_ph4_sync` attend la quiescence filesystem avant
d'autoriser l'évaluation des gates.
"""

from __future__ import annotations

import threading
import time
from pathlib import Path

from orchestrator.ph4_sync import _get_latest_mtime, wait_for_ph4_sync


def test_returns_false_when_site_dir_missing(tmp_path: Path):
    """Site dir inexistant → False immédiat (pas d'attente)."""
    missing = tmp_path / "does_not_exist"
    start = time.monotonic()
    result = wait_for_ph4_sync(missing, max_wait=10.0)
    assert result is False
    assert time.monotonic() - start < 1.0


def test_returns_true_for_stable_dir(tmp_path: Path):
    """Site dir non-modifié → True après idle_seconds."""
    (tmp_path / "page.tsx").write_text("export default function() {}", encoding="utf-8")
    time.sleep(0.5)  # laisser le mtime se "stabiliser"

    start = time.monotonic()
    result = wait_for_ph4_sync(tmp_path, idle_seconds=2.0, max_wait=10.0, poll_interval=0.5)
    elapsed = time.monotonic() - start

    assert result is True
    # Doit avoir attendu au moins idle_seconds, mais pas beaucoup plus
    assert elapsed >= 1.5
    assert elapsed < 5.0


def test_waits_when_files_being_written(tmp_path: Path):
    """Si un fichier est créé pendant l'attente, le compteur idle redémarre."""
    (tmp_path / "page.tsx").write_text("a", encoding="utf-8")

    # Un thread qui crée un nouveau fichier après 1s
    def write_late():
        time.sleep(1.0)
        (tmp_path / "component.tsx").write_text("b", encoding="utf-8")

    threading.Thread(target=write_late, daemon=True).start()

    start = time.monotonic()
    result = wait_for_ph4_sync(tmp_path, idle_seconds=2.0, max_wait=15.0, poll_interval=0.5)
    elapsed = time.monotonic() - start

    assert result is True
    # Doit avoir attendu au moins ~3s (1s avant écriture + 2s idle après)
    assert elapsed >= 2.5


def test_returns_false_on_timeout(tmp_path: Path):
    """Si les fichiers continuent d'être modifiés au-delà de max_wait → False."""
    (tmp_path / "page.tsx").write_text("a", encoding="utf-8")
    stop_event = threading.Event()

    def write_continuously():
        i = 0
        while not stop_event.is_set():
            (tmp_path / f"file_{i}.tsx").write_text(str(i), encoding="utf-8")
            i += 1
            time.sleep(0.3)

    t = threading.Thread(target=write_continuously, daemon=True)
    t.start()

    try:
        start = time.monotonic()
        result = wait_for_ph4_sync(tmp_path, idle_seconds=2.0, max_wait=3.0, poll_interval=0.3)
        elapsed = time.monotonic() - start
        assert result is False
        assert elapsed >= 2.5  # doit avoir attendu près de max_wait
    finally:
        stop_event.set()
        t.join(timeout=2.0)


def test_excludes_node_modules_from_mtime(tmp_path: Path):
    """Les changements dans node_modules/.next ne doivent pas réveiller le poll."""
    (tmp_path / "page.tsx").write_text("a", encoding="utf-8")
    nm = tmp_path / "node_modules" / "react"
    nm.mkdir(parents=True)
    (nm / "index.js").write_text("module", encoding="utf-8")

    # Note le mtime initial
    initial_mtime = _get_latest_mtime(tmp_path)

    # Modifier node_modules (devrait être exclu)
    time.sleep(0.1)
    (nm / "index.js").write_text("module modified", encoding="utf-8")

    new_mtime = _get_latest_mtime(tmp_path)
    # Le mtime ne devrait pas avoir bougé (node_modules est exclu)
    assert new_mtime == initial_mtime
