#!/bin/bash
# Génère .archive-checksum.json pour un dossier archive/ (A-009 fix Phase 1).
# Usage : freeze-archive.sh <archive_dir> [source_description]
set -euo pipefail
ARCHIVE_DIR="${1:?Usage: freeze-archive.sh <archive_dir> [source]}"
SOURCE_DESC="${2:-unknown source}"

if [ ! -d "$ARCHIVE_DIR" ]; then
    echo "FAIL: $ARCHIVE_DIR n'est pas un dossier"
    exit 1
fi

python3 - "$ARCHIVE_DIR" "$SOURCE_DESC" <<'PY'
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

archive_dir = Path(sys.argv[1])
source = sys.argv[2]

files = {}
for path in sorted(archive_dir.rglob("*")):
    if path.is_file() and not path.name.startswith(".archive-checksum"):
        rel = path.relative_to(archive_dir).as_posix()
        files[rel] = {
            "size_bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }

manifest = {
    "frozen_at": datetime.now(timezone.utc).isoformat(),
    "source": source,
    "files": files,
}
(archive_dir / ".archive-checksum.json").write_text(
    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
)
print(f"Frozen {len(files)} files in {archive_dir}")
PY
