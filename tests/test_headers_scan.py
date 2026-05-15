"""Tests régression pour tools/headers-scan.sh.

Couvre BUG_NEXOS_HEADERS_SCAN_DUPLICATE_KEY (A-007) : sur une URL qui
suit un redirect (ex: middleware next-intl `/` → `/<locale>`), le script
doit émettre un JSON sans clés dupliquées.
"""

from __future__ import annotations

import http.server
import json
import socket
import socketserver
import subprocess
import threading
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
HEADERS_SCAN = REPO_ROOT / "tools" / "headers-scan.sh"


class _RedirectHandler(http.server.BaseHTTPRequestHandler):
    """Simule un middleware i18n qui redirige `/` vers `/fr` avec set complet de
    headers de sécurité, puis répond 200 sur `/fr` avec un set partiellement
    superposé. Curl `-L` accumule les headers des deux hops → cas reproductible
    pour A-007.
    """

    def do_HEAD(self):
        if self.path == "/":
            self.send_response(307)
            self.send_header("Location", "/fr")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Frame-Options", "DENY")
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Strict-Transport-Security", "max-age=31536000")
        self.end_headers()

    def log_message(self, *args, **kwargs):  # silencieux
        return


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def redirect_server():
    port = _free_port()
    server = socketserver.TCPServer(("127.0.0.1", port), _RedirectHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield port
    finally:
        server.shutdown()
        server.server_close()


def _strict_json_loads(raw: str):
    """Parse JSON et lève sur clé dupliquée (object_pairs_hook strict)."""

    def _hook(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                raise ValueError(f"Duplicate key: {k}")
            seen.add(k)
        return dict(pairs)

    return json.loads(raw, object_pairs_hook=_hook)


def test_headers_scan_handles_redirect_no_duplicates(redirect_server):
    """Sur une URL qui redirect, headers-scan.sh doit dédupliquer les clés."""
    url = f"http://127.0.0.1:{redirect_server}/"
    result = subprocess.run(
        ["bash", str(HEADERS_SCAN), url],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"script failed: {result.stderr}"

    data = _strict_json_loads(result.stdout)
    assert data["url"] == url
    # Clés finales attendues (réponse 200 sur /fr)
    assert data["x-content-type-options"] == "nosniff"
    assert data["x-frame-options"] == "DENY"
    assert data["referrer-policy"] == "strict-origin-when-cross-origin"
    assert data["strict-transport-security"] == "max-age=31536000"


def test_headers_scan_keeps_last_value_after_redirect(redirect_server):
    """Sémantique HTTP : la réponse finale prime sur les hops intermédiaires.
    Le serveur 200 envoie strict-transport-security mais pas le 307. Le 307
    envoie x-content-type-options ET x-frame-options qui sont aussi sur le 200
    avec la même valeur. On vérifie que les valeurs sont conservées (pas perdues
    par le dédup)."""
    url = f"http://127.0.0.1:{redirect_server}/"
    result = subprocess.run(
        ["bash", str(HEADERS_SCAN), url],
        capture_output=True,
        text=True,
        timeout=30,
    )
    data = _strict_json_loads(result.stdout)

    # Le set final doit refléter les headers de la réponse 200
    expected_present = {
        "x-content-type-options",
        "x-frame-options",
        "referrer-policy",
        "strict-transport-security",
    }
    assert expected_present.issubset(set(data.keys()))


def test_headers_scan_unreachable_url_emits_error_json():
    """Si curl ne peut pas joindre l'URL, le script doit émettre un JSON
    d'erreur valide (pas un crash).

    Contrat P4d (hardening tools/*.sh) : toujours exit 0 + JSON valide,
    même en erreur. L'erreur est encodée dans le JSON pour consumer.
    """
    port = _free_port()
    url = f"http://127.0.0.1:{port}/"
    result = subprocess.run(
        ["bash", str(HEADERS_SCAN), url],
        capture_output=True,
        text=True,
        timeout=30,
    )
    # P4d : exit 0 toujours + JSON valide contient le champ "error"
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "error" in data
    assert "unable to fetch headers" in data["error"]
    assert data["url"] == url
    # Le champ stderr est toujours présent (string, peut être vide)
    assert "stderr" in data
