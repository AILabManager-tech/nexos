"""Tests de validation runtime contre mission.intake."""

import json
import tempfile
from pathlib import Path

from orchestrator import verify_phase_output


def _write_modify_brief(client_dir: Path) -> None:
    (client_dir / "brief-client.json").write_text(
        json.dumps(
            {
                "_meta": {"mode": "modify"},
                "client": {"name": "Test Corp", "slug": "test-corp"},
                "company": {
                    "address": "123 Rue Test",
                    "phone": "514-555-0000",
                    "email": "info@test.com",
                },
                "legal": {
                    "rpp": {"name": "Jean Test", "email": "rpp@test.com", "title": "RPP"},
                    "data_collected": ["nom"],
                    "purposes": ["communication"],
                    "retention": "24 mois",
                    "transfer_outside_qc": False,
                    "consent_mode": "opt-in (recommandé Loi 25)",
                },
                "site": {
                    "type": "vitrine",
                    "stack": "nextjs",
                    "pages": ["accueil", "contact"],
                    "languages": ["fr"],
                },
                "mission": {
                    "mode": "modify",
                    "intake": {
                        "requested_changes": "Refondre la hero et simplifier le formulaire",
                        "sections_in_scope": "accueil, contact",
                        "must_preserve": "SEO existant",
                    },
                },
            }
        ),
        encoding="utf-8",
    )


def test_verify_phase_output_accepts_report_aligned_with_intake():
    with tempfile.TemporaryDirectory() as tmp:
        client_dir = Path(tmp)
        _write_modify_brief(client_dir)
        report = client_dir / "site-update-report.md"
        report.write_text(
            "# Site update\n\n"
            + (
                "Nous allons refondre la hero, revoir le formulaire de contact et "
                "conserver le SEO existant sur les sections accueil et contact. " * 12
            ),
            encoding="utf-8",
        )
        assert verify_phase_output("site-update", client_dir) is True


def test_verify_phase_output_rejects_generic_report_ignoring_intake():
    with tempfile.TemporaryDirectory() as tmp:
        client_dir = Path(tmp)
        _write_modify_brief(client_dir)
        report = client_dir / "site-update-report.md"
        report.write_text(
            "# Site update\n\n"
            + (
                "Rapport générique sur la qualité globale du site sans mention du scope réel. " * 20
            ),
            encoding="utf-8",
        )
        assert verify_phase_output("site-update", client_dir) is False
