#!/bin/bash
# Audit d'intégrité d'un dossier archive/ via .archive-checksum.json (A-009 fix).
# Exit codes : 0=PASS, 1=mauvais usage, 2=manifest manquant, 3=drift détecté.
set -euo pipefail
ARCHIVE_DIR="${1:?Usage: audit-archive-integrity.sh <archive_dir>}"

if [ ! -d "$ARCHIVE_DIR" ]; then
    echo "FAIL: $ARCHIVE_DIR n'est pas un dossier"
    exit 1
fi

CHECKSUM_FILE="$ARCHIVE_DIR/.archive-checksum.json"
if [ ! -f "$CHECKSUM_FILE" ]; then
    echo "FAIL: $CHECKSUM_FILE manquant — archive non gelée correctement"
    exit 2
fi

python3 - "$ARCHIVE_DIR" "$CHECKSUM_FILE" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

archive_dir = Path(sys.argv[1])
checksum_file = Path(sys.argv[2])

manifest = json.loads(checksum_file.read_text())
drift = []
for relpath, expected in manifest["files"].items():
    path = archive_dir / relpath
    if not path.exists():
        drift.append(f"MISSING {relpath}")
        continue
    actual_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_sha != expected["sha256"]:
        drift.append(
            f"DRIFT {relpath} (expected {expected['sha256'][:8]}, got {actual_sha[:8]})"
        )

if drift:
    print(f"FAIL: {len(drift)} drift(s) détecté(s)")
    for d in drift:
        print(f"  {d}")
    sys.exit(3)
print(f"PASS: {len(manifest['files'])} fichiers conformes")
PY
