"""Tests pour l'injection de mission.intake dans les prompts de phase."""

import json
import tempfile
from pathlib import Path

from orchestrator import build_phase_prompt


class TestPromptIntakeInjection:
    def test_modify_intake_is_injected_in_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            client_dir = Path(tmp)
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
                            "pages": ["accueil"],
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

            prompt = build_phase_prompt("site-update", client_dir)
            assert "CADRAGE MÉTIER PRIORITAIRE" in prompt
            assert "Refondre la hero" in prompt
            assert "SEO existant" in prompt
            assert "intervention ciblée sur un existant" in prompt
