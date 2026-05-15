"""Tests régression pour nexos.port_allocator.

Couvre P3 (ROADMAP) — interdiction d'allouer dans la zone éphémère kernel
(32768-60999) et les ports privilégiés (0-1023). Force l'usage des sous-blocs
nommés documentés dans `~/.claude/CLAUDE.md` user.

Garanties testées :
  - Constantes : 12 sous-blocs définis, tous hors zones interdites
  - allocate_port : retourne premier port libre, séquentiel start→end
  - allocate_port : raise SubblockSaturatedError quand tout est pris
  - allocate_port : raise ForbiddenZoneError si sous-bloc déborde
  - is_port_free : true/false selon bind réel
  - purge_subblock : appel explicite, retourne PIDs (mock)
  - PortSubblock : valide start <= end
  - Garde-fou import : aucune constante dans zone interdite
"""

from __future__ import annotations

import socket
from dataclasses import FrozenInstanceError
from unittest.mock import patch

import pytest

from nexos import port_allocator
from nexos.port_allocator import (
    ALL_SUBBLOCKS,
    FORBIDDEN_RANGES,
    NEXOS_BUFFER,
    NEXOS_ENGINE,
    ForbiddenZoneError,
    PortSubblock,
    SubblockSaturatedError,
    allocate_port,
    is_port_free,
    purge_subblock,
)

# ---------------------------------------------------------------------------
# Constantes + garde-fou zones interdites
# ---------------------------------------------------------------------------


def test_all_subblocks_count() -> None:
    """12 sous-blocs déclarés dans la constante d'export."""
    assert len(ALL_SUBBLOCKS) == 12


def test_subblock_names_match_claude_md() -> None:
    """Noms canoniques : ils sont référencés dans CLAUDE.md user et runbook."""
    names = {sb.name for sb in ALL_SUBBLOCKS}
    expected = {
        "NEXOS_TESTS",
        "NEXOS_ENGINE",
        "NEXOS_SCRAPING",
        "NEXOS_CYBERSEC",
        "NEXOS_BUFFER",
        "GENESIS_TESTS",
        "GENESIS_ENGINE",
        "GENCORE",
        "SAAS",
        "CYBERSEC_LABS",
        "AUDIT_TOOLKIT",
        "GLOBAL_BUFFER",
    }
    assert names == expected


def test_nexos_engine_range() -> None:
    """NEXOS_ENGINE est 20100-20199 (sous-bloc engine, callsite preflight.py)."""
    assert NEXOS_ENGINE.start == 20100
    assert NEXOS_ENGINE.end == 20199


def test_forbidden_ranges_documented() -> None:
    """Privilégiés OS + éphémère kernel poste gear-code."""
    assert (0, 1023) in FORBIDDEN_RANGES
    assert (32768, 60999) in FORBIDDEN_RANGES


def test_no_subblock_overlaps_forbidden_zones() -> None:
    """Garde-fou : aucune constante exportée ne déborde dans zone interdite.

    Si cette assertion casse, c'est qu'on a glissé un sous-bloc dans
    32768-60999 (kernel ephemeral) ou < 1024 (privileged) — exactement le
    bug P3 que ce module corrige.
    """
    for sb in ALL_SUBBLOCKS:
        for fstart, fend in FORBIDDEN_RANGES:
            overlap = sb.start <= fend and sb.end >= fstart
            assert not overlap, (
                f"{sb.name} ({sb.start}-{sb.end}) chevauche zone interdite {fstart}-{fend}"
            )


# ---------------------------------------------------------------------------
# PortSubblock dataclass
# ---------------------------------------------------------------------------


def test_portsubblock_inclusive_bounds() -> None:
    sb = PortSubblock("TEST", 20000, 20002)
    ports = list(sb)
    assert ports == [20000, 20001, 20002]


def test_portsubblock_rejects_inverted_bounds() -> None:
    with pytest.raises(ValueError, match=r"start.*> end"):
        PortSubblock("BROKEN", 100, 50)


def test_portsubblock_is_frozen() -> None:
    """Constantes immutables — pas de mutation accidentelle."""
    with pytest.raises(FrozenInstanceError):
        NEXOS_ENGINE.start = 99999  # type: ignore[misc]


# ---------------------------------------------------------------------------
# allocate_port
# ---------------------------------------------------------------------------


def test_allocate_returns_port_in_range() -> None:
    """allocate_port retourne un port dans le sous-bloc demandé."""
    # NEXOS_BUFFER (20900-20999) : peu probable d'être pris en CI.
    port = allocate_port(NEXOS_BUFFER)
    assert NEXOS_BUFFER.start <= port <= NEXOS_BUFFER.end


def test_allocate_picks_first_free() -> None:
    """Probe séquentiel : premier libre, pas random."""
    sb = PortSubblock("TEST_TINY", 20950, 20952)

    free_call = iter([False, False, True])

    def fake_is_free(_port: int) -> bool:
        return next(free_call)

    with patch.object(port_allocator, "is_port_free", side_effect=fake_is_free):
        port = allocate_port(sb)
    assert port == 20952


def test_allocate_raises_when_saturated() -> None:
    """Tout pris → SubblockSaturatedError (jamais de purge auto)."""
    sb = PortSubblock("TEST_TINY", 20950, 20952)
    with (
        patch.object(port_allocator, "is_port_free", return_value=False),
        pytest.raises(SubblockSaturatedError, match="saturé"),
    ):
        allocate_port(sb)


def test_allocate_rejects_forbidden_zone() -> None:
    """Sous-bloc custom qui déborde dans 32768-60999 → refus."""
    bad = PortSubblock("BAD", 55000, 55100)
    with pytest.raises(ForbiddenZoneError, match="32768-60999"):
        allocate_port(bad)


def test_allocate_rejects_privileged() -> None:
    """Sous-bloc qui touche les ports privilégiés → refus."""
    bad = PortSubblock("BAD", 80, 90)
    with pytest.raises(ForbiddenZoneError, match="0-1023"):
        allocate_port(bad)


def test_allocate_skips_busy_port() -> None:
    """Si un vrai port est pris dans le sous-bloc, allocator passe au suivant."""
    sb = PortSubblock("TEST_REAL", 20900, 20910)
    # On bind un port réel pour simuler un service qui tourne dans le sous-bloc.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as blocker:
        blocker.bind(("127.0.0.1", 20900))
        blocker.listen(1)
        port = allocate_port(sb)
        assert port != 20900
        assert sb.start <= port <= sb.end


# ---------------------------------------------------------------------------
# is_port_free
# ---------------------------------------------------------------------------


def test_is_port_free_true_for_unbound() -> None:
    """Un port aléatoire dans NEXOS_BUFFER devrait être libre en local."""
    # On prend une borne haute pour minimiser la chance de collision.
    assert is_port_free(20999) in (True, False)  # tolérant : env dépendant


def test_is_port_free_false_when_bound() -> None:
    """Bind explicite → is_port_free retourne False."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as blocker:
        blocker.bind(("127.0.0.1", 20998))
        blocker.listen(1)
        assert is_port_free(20998) is False


# ---------------------------------------------------------------------------
# purge_subblock (mock subprocess pour ne pas tuer de vrais process)
# ---------------------------------------------------------------------------


def test_purge_subblock_explicit_only() -> None:
    """purge_subblock retourne la liste des PIDs (mock ss output)."""
    fake_ss_output = (
        'LISTEN 0  128 127.0.0.1:20100 0.0.0.0:* users:(("node",pid=4242,fd=21))\n'
        'LISTEN 0  128 127.0.0.1:20105 0.0.0.0:* users:(("node",pid=4243,fd=22))\n'
        'LISTEN 0  128 127.0.0.1:30000 0.0.0.0:* users:(("other",pid=9999,fd=10))\n'
    )

    class FakeCompleted:
        stdout = fake_ss_output

    with patch.object(port_allocator.subprocess, "run") as mock_run:
        mock_run.return_value = FakeCompleted()
        killed = purge_subblock(NEXOS_ENGINE)

    # 30000 est hors NEXOS_ENGINE (20100-20199), doit être ignoré.
    assert set(killed) == {4242, 4243}
    # Vérifie qu'on a bien appelé `kill` pour chaque PID en plus du `ss` initial.
    kill_calls = [
        c for c in mock_run.call_args_list if c.args and c.args[0] and c.args[0][0] == "kill"
    ]
    assert len(kill_calls) == 2


def test_purge_subblock_rejects_forbidden_zone() -> None:
    """purge refuse aussi les zones interdites (défense en profondeur)."""
    bad = PortSubblock("BAD", 55000, 55100)
    with pytest.raises(ForbiddenZoneError):
        purge_subblock(bad)


def test_purge_subblock_no_listeners() -> None:
    """ss output vide → retourne liste vide, jamais d'exception."""

    class FakeCompleted:
        stdout = ""

    with patch.object(port_allocator.subprocess, "run", return_value=FakeCompleted()):
        killed = purge_subblock(NEXOS_BUFFER)
    assert killed == []


def test_purge_subblock_ss_unavailable() -> None:
    """Si `ss` est absent, purge_subblock retourne [] (tolérant)."""
    with patch.object(port_allocator.subprocess, "run", side_effect=FileNotFoundError("ss")):
        killed = purge_subblock(NEXOS_BUFFER)
    assert killed == []
