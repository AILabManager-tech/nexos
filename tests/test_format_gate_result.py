"""Tests régression pour orchestrator.phases.format_gate_result (A-003).

Couvre BUG_NEXOS_ORCHESTRATOR_ABORT_DISPLAY : l'ancien message affichait
toujours `μ < seuil` pour tout non-converged, induisant l'opérateur en
erreur quand l'ABORT venait d'une autre cause (rate limit, callback
subprocess failed, plateau de convergence) avec μ effectif ≥ seuil.
"""

from __future__ import annotations

from orchestrator.gate_display import format_gate_result


def test_accept_high_mu():
    """μ supérieur au seuil + converged → message ACCEPT avec ≥."""
    msg = format_gate_result(
        converged=True, mu=9.47, threshold=8.5, decision="ACCEPT", iterations=1
    )
    assert "✓" in msg
    assert "ACCEPT" in msg
    assert "≥" in msg
    assert "9.47" in msg
    assert "8.5" in msg


def test_abort_max_iter_with_mu_above_threshold_does_not_say_below():
    """A-003 cas central : ABORT_MAX_ITER avec μ ≥ seuil ne doit JAMAIS
    afficher `μ < seuil` (cas SESSION_04 Nobert : μ=8.53 ≥ 8.0)."""
    msg = format_gate_result(
        converged=False, mu=8.53, threshold=8.0, decision="ABORT_MAX_ITER", iterations=1
    )
    # Aucune occurrence du comparateur trompeur
    assert "< 8.0" not in msg
    assert "< 8" not in msg
    # Decision visible
    assert "ABORT_MAX_ITER" in msg
    # Le seuil est affiché en référence, pas en comparaison
    assert "seuil=8.0" in msg or "seuil=8" in msg
    assert "boucle interrompue" in msg


def test_abort_plateau_displays_correctly():
    """ABORT_PLATEAU avec μ < seuil ne doit pas dire `μ < seuil` non plus,
    car le plateau n'est pas un échec de seuil mais un échec de convergence."""
    msg = format_gate_result(
        converged=False, mu=6.11, threshold=7.0, decision="ABORT_PLATEAU", iterations=3
    )
    assert "< 7.0" not in msg
    assert "ABORT_PLATEAU" in msg
    assert "boucle interrompue" in msg


def test_reject_displays_below_comparator():
    """REJECT = vrai franchissement insuffisant → afficher μ < seuil reste correct."""
    msg = format_gate_result(
        converged=False, mu=5.5, threshold=8.0, decision="REJECT", iterations=2
    )
    assert "REJECT" in msg
    assert "<" in msg
    assert "5.5" in msg
    assert "8.0" in msg


def test_format_includes_iterations():
    """Le nombre d'itérations doit toujours être affiché."""
    msg = format_gate_result(converged=True, mu=9.0, threshold=8.0, decision="ACCEPT", iterations=3)
    assert "3 iter" in msg

    msg2 = format_gate_result(
        converged=False, mu=8.5, threshold=8.0, decision="ABORT_MAX_ITER", iterations=4
    )
    assert "4 iter" in msg2


def test_abort_max_iter_below_threshold_still_correct():
    """Cas où ABORT_MAX_ITER coïncide avec μ < seuil : ne doit pas non plus
    afficher la comparaison trompeuse (decision claire est suffisante)."""
    msg = format_gate_result(
        converged=False, mu=7.5, threshold=8.0, decision="ABORT_MAX_ITER", iterations=3
    )
    assert "< 8.0" not in msg
    assert "ABORT_MAX_ITER" in msg
