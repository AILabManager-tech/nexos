"""Port allocator — sous-blocs nommés, zones interdites kernel/privilégiées.

Implémente la règle d'allocation documentée dans `~/.claude/CLAUDE.md` user
(section "Allocation des ports") :

- Allocation séquentielle : premier port libre dans le sous-bloc demandé.
- Pas de purge automatique : si tout le sous-bloc est pris, on lève
  `SubblockSaturatedError`. La purge cyclique (`purge_subblock`) est un appel
  explicite du caller, jamais déclenché en interne.
- Zones interdites : 0-1023 (privilégiés) + 32768-60999 (éphémère kernel sur
  ce poste, cf `/proc/sys/net/ipv4/ip_local_port_range`).

Usage typique côté NEXOS :

    from nexos.port_allocator import allocate_port, NEXOS_ENGINE
    port = allocate_port(NEXOS_ENGINE)  # premier libre dans 20100-20199
"""

from __future__ import annotations

import socket
import subprocess
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class PortSubblock:
    """Sous-bloc de ports nommé. Inclusif aux deux bornes."""

    name: str
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError(f"PortSubblock {self.name}: start ({self.start}) > end ({self.end})")

    def __iter__(self) -> Iterator[int]:
        return iter(range(self.start, self.end + 1))


# --- Sous-blocs documentés dans ~/.claude/CLAUDE.md user ---------------------

NEXOS_TESTS = PortSubblock("NEXOS_TESTS", 20000, 20099)
NEXOS_ENGINE = PortSubblock("NEXOS_ENGINE", 20100, 20199)
NEXOS_SCRAPING = PortSubblock("NEXOS_SCRAPING", 20200, 20299)
NEXOS_CYBERSEC = PortSubblock("NEXOS_CYBERSEC", 20300, 20399)
NEXOS_BUFFER = PortSubblock("NEXOS_BUFFER", 20900, 20999)

GENESIS_TESTS = PortSubblock("GENESIS_TESTS", 21000, 21099)
GENESIS_ENGINE = PortSubblock("GENESIS_ENGINE", 21100, 21199)

GENCORE = PortSubblock("GENCORE", 22000, 22999)
SAAS = PortSubblock("SAAS", 23000, 23999)
CYBERSEC_LABS = PortSubblock("CYBERSEC_LABS", 24000, 24999)
AUDIT_TOOLKIT = PortSubblock("AUDIT_TOOLKIT", 25000, 25999)
GLOBAL_BUFFER = PortSubblock("GLOBAL_BUFFER", 29000, 29999)

ALL_SUBBLOCKS: tuple[PortSubblock, ...] = (
    NEXOS_TESTS,
    NEXOS_ENGINE,
    NEXOS_SCRAPING,
    NEXOS_CYBERSEC,
    NEXOS_BUFFER,
    GENESIS_TESTS,
    GENESIS_ENGINE,
    GENCORE,
    SAAS,
    CYBERSEC_LABS,
    AUDIT_TOOLKIT,
    GLOBAL_BUFFER,
)

# --- Zones interdites (privilégiés OS + éphémère kernel) ---------------------

FORBIDDEN_RANGES: tuple[tuple[int, int], ...] = (
    (0, 1023),
    (32768, 60999),
)


class SubblockSaturatedError(RuntimeError):
    """Tous les ports du sous-bloc sont occupés et `--purge` n'a pas été appelé."""


class ForbiddenZoneError(ValueError):
    """Un sous-bloc chevauche une zone interdite (privilégiés ou éphémère kernel)."""


def _validate_subblock(subblock: PortSubblock) -> None:
    for fstart, fend in FORBIDDEN_RANGES:
        if subblock.start <= fend and subblock.end >= fstart:
            raise ForbiddenZoneError(
                f"Sous-bloc {subblock.name} ({subblock.start}-{subblock.end}) "
                f"chevauche zone interdite {fstart}-{fend}"
            )


# Validation défensive au load : si jamais une constante dérive un jour vers
# une zone interdite, on lève au import et pas à l'usage.
for _sb in ALL_SUBBLOCKS:
    _validate_subblock(_sb)


def is_port_free(port: int) -> bool:
    """Tente un bind éphémère sur localhost:<port>. True si libre."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def allocate_port(subblock: PortSubblock) -> int:
    """Retourne le premier port libre dans `subblock` (probe séquentiel).

    Raise:
        ForbiddenZoneError: si `subblock` chevauche une zone interdite.
        SubblockSaturatedError: si aucun port libre dans tout le sous-bloc.
    """
    _validate_subblock(subblock)
    for port in subblock:
        if is_port_free(port):
            return port
    raise SubblockSaturatedError(
        f"Sous-bloc {subblock.name} ({subblock.start}-{subblock.end}) saturé. "
        f"Appeler purge_subblock({subblock.name}) explicitement pour libérer."
    )


def _pids_listening_in(subblock: PortSubblock) -> dict[int, int]:
    """Retourne {port: pid} pour les sockets LISTEN dans le sous-bloc.

    Utilise `ss -Hltnp` (Linux). Tolère absence de droits (sans sudo, certains
    PIDs peuvent être masqués — on ne retourne que ceux visibles).
    """
    try:
        result = subprocess.run(
            ["ss", "-Hltnp"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {}

    found: dict[int, int] = {}
    for line in result.stdout.splitlines():
        # ss output: State Recv-Q Send-Q Local-Address:Port Peer ...  users:(("name",pid=X,fd=Y))
        parts = line.split()
        if len(parts) < 4:
            continue
        local = parts[3]
        if ":" not in local:
            continue
        try:
            port = int(local.rsplit(":", 1)[1])
        except ValueError:
            continue
        if not (subblock.start <= port <= subblock.end):
            continue
        if "pid=" not in line:
            continue
        try:
            pid_token = line.split("pid=", 1)[1].split(",", 1)[0]
            # `ss` peut emballer dans `pid=X` ou `pid=X))` selon version ; on
            # nettoie en gardant uniquement les chiffres de tête.
            digits = ""
            for ch in pid_token:
                if ch.isdigit():
                    digits += ch
                else:
                    break
            if not digits:
                continue
            pid = int(digits)
        except (IndexError, ValueError):
            continue
        found[port] = pid
    return found


def purge_subblock(subblock: PortSubblock) -> list[int]:
    """Kill les process écoutant dans le sous-bloc. Retourne les PIDs tués.

    APPEL EXPLICITE uniquement — jamais déclenché par `allocate_port()`.
    Utilise SIGTERM (pas SIGKILL) pour laisser les serveurs cleanup.
    """
    _validate_subblock(subblock)
    pids_map = _pids_listening_in(subblock)
    killed: list[int] = []
    for pid in set(pids_map.values()):
        try:
            subprocess.run(["kill", "-TERM", str(pid)], check=False, timeout=5)
            killed.append(pid)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    return killed


__all__ = [
    "ALL_SUBBLOCKS",
    "AUDIT_TOOLKIT",
    "CYBERSEC_LABS",
    "FORBIDDEN_RANGES",
    "GENCORE",
    "GENESIS_ENGINE",
    "GENESIS_TESTS",
    "GLOBAL_BUFFER",
    "NEXOS_BUFFER",
    "NEXOS_CYBERSEC",
    "NEXOS_ENGINE",
    "NEXOS_SCRAPING",
    "NEXOS_TESTS",
    "SAAS",
    "ForbiddenZoneError",
    "PortSubblock",
    "SubblockSaturatedError",
    "allocate_port",
    "is_port_free",
    "purge_subblock",
]
