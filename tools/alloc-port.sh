#!/usr/bin/env bash
# alloc-port.sh — wrapper CLI autour de nexos.port_allocator.
#
# Implémente la règle ~/.claude/CLAUDE.md user (Allocation des ports) :
# - Allocation séquentielle premier port libre dans le sous-bloc nommé
# - Purge cyclique via --purge EXPLICITE (jamais automatique)
# - Zones interdites : 0-1023 et 32768-60999 refusées par le helper Python
#
# Usage :
#     alloc-port.sh <SUBBLOCK_NAME> [--purge]
#     alloc-port.sh --list
#     alloc-port.sh --help
#
# Sortie JSON sur stdout en cas de succès : {"port": N, "subblock": "X"}.
# Erreurs sur stderr. Voir codes de sortie dans --help.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

usage() {
    cat <<'EOF'
Usage: alloc-port.sh <SUBBLOCK_NAME> [--purge]
       alloc-port.sh --list
       alloc-port.sh --help

Allocate first free port in named subblock (per ~/.claude/CLAUDE.md user).

Options:
    --purge     Kill listeners in subblock BEFORE allocating. Use only when
                subblock is saturated (allocator never purges automatically).
    --list      List all 12 subblocks with their port ranges.
    --help      Show this help.

Subblocks NEXOS:
    NEXOS_TESTS     20000-20099   tests éphémères
    NEXOS_ENGINE    20100-20199   pipeline engine (preflight Next.js, etc.)
    NEXOS_SCRAPING  20200-20299   scraping & automation
    NEXOS_CYBERSEC  20300-20399   cybersec interne pipeline
    NEXOS_BUFFER    20900-20999   ad-hoc NEXOS

Examples:
    alloc-port.sh NEXOS_ENGINE
    # {"port": 20100, "subblock": "NEXOS_ENGINE"}

    alloc-port.sh NEXOS_ENGINE --purge
    # {"port": 20100, "subblock": "NEXOS_ENGINE", "purged_pids": [4242]}

Exit codes:
    0   success
    1   invalid args
    2   unknown subblock
    3   subblock saturated (try --purge)
    4   forbidden zone overlap (defensive, should never trigger)
EOF
}

PURGE=0
SUBBLOCK=""
ACTION=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h)
            usage
            exit 0
            ;;
        --list)
            ACTION="list"
            shift
            ;;
        --purge)
            PURGE=1
            shift
            ;;
        --*)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
        *)
            if [[ -z "$SUBBLOCK" ]]; then
                SUBBLOCK="$1"
                shift
            else
                echo "Too many positional arguments: '$1'" >&2
                usage >&2
                exit 1
            fi
            ;;
    esac
done

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

if [[ "$ACTION" == "list" ]]; then
    exec python3 -c '
from nexos.port_allocator import ALL_SUBBLOCKS
for sb in ALL_SUBBLOCKS:
    print(f"{sb.name:<16s} {sb.start}-{sb.end}")
'
fi

if [[ -z "$SUBBLOCK" ]]; then
    echo "Missing required argument: SUBBLOCK_NAME" >&2
    usage >&2
    exit 1
fi

# Inputs traversent par env vars (pas d'interpolation shell dans le Python).
SUBBLOCK="$SUBBLOCK" PURGE="$PURGE" exec python3 - <<'PYEOF'
import json
import os
import sys

from nexos.port_allocator import (
    ALL_SUBBLOCKS,
    ForbiddenZoneError,
    SubblockSaturatedError,
    allocate_port,
    purge_subblock,
)

name = os.environ["SUBBLOCK"]
do_purge = os.environ.get("PURGE") == "1"

by_name = {sb.name: sb for sb in ALL_SUBBLOCKS}
if name not in by_name:
    print(
        json.dumps(
            {
                "error": "unknown_subblock",
                "name": name,
                "available": sorted(by_name),
            }
        ),
        file=sys.stderr,
    )
    sys.exit(2)

subblock = by_name[name]

purged: list[int] = []
if do_purge:
    try:
        purged = purge_subblock(subblock)
    except ForbiddenZoneError as exc:
        print(json.dumps({"error": "forbidden_zone", "detail": str(exc)}), file=sys.stderr)
        sys.exit(4)

try:
    port = allocate_port(subblock)
except SubblockSaturatedError as exc:
    print(
        json.dumps(
            {
                "error": "saturated",
                "subblock": name,
                "hint": str(exc),
                "purged_pids": purged,
            }
        ),
        file=sys.stderr,
    )
    sys.exit(3)
except ForbiddenZoneError as exc:
    print(json.dumps({"error": "forbidden_zone", "detail": str(exc)}), file=sys.stderr)
    sys.exit(4)

result: dict = {"port": port, "subblock": name}
if purged:
    result["purged_pids"] = purged
print(json.dumps(result))
PYEOF
