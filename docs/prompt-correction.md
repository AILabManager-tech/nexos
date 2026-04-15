# PROMPT CLAUDE-CLI — CORRECTION SOIC v3.0 NEXOS

> **Usage** : `cd ~/___00___MARK_SYSTEMS_BIZ___/NEXOS/nexos_v.3.0 && claude`
> **Coller ce prompt dans le terminal.**

---

```
Tu opères dans le répertoire NEXOS v3.0. Le moteur SOIC v3.0 est implémenté (2750 lignes, 10 fichiers dans soic/, orchestrator.py modifié). Il fonctionne mais a des défauts critiques identifiés par audit. Ta mission : corriger ces défauts sans casser l'existant.

Lis d'abord TOUS les fichiers suivants pour comprendre l'état actuel :
- soic/__init__.py
- soic/models.py
- soic/gate_engine.py
- soic/gate_protocol.py
- soic/converger.py
- soic/feedback_router.py
- soic/iterator.py
- soic/persistence.py
- soic/report.py
- soic/domain_grids/__init__.py
- soic/domain_grids/web.py
- soic/domain_grids/phase_early.py
- orchestrator.py

Ensuite, applique les corrections suivantes dans l'ordre. Chaque correction est un commit logique. Ne passe pas à la suivante sans que la précédente compile et fonctionne.

═══════════════════════════════════════════════════════
CORRECTION 1 — ÉLIMINER LES FAUX 5.0 NEUTRES
═══════════════════════════════════════════════════════

Problème : Les gates qui lisent tooling/*.json (Lighthouse, axe-core, headers, etc.) retournent SKIP silencieusement si le fichier n'existe pas. Le score SKIP = 5.0 par défaut, ce qui gonfle artificiellement le μ. Un site non testé obtient un score flatteur.

Correction :
1. Dans soic/models.py : ajouter un statut GateStatus.NOT_EXECUTED distinct de SKIP
2. Dans soic/models.py > PhaseGateReport.compute_score() :
   - NOT_EXECUTED compte comme 0.0, pas 5.0
   - Ajouter un champ `coverage: float` = nombre de gates réellement exécutées / total
   - Si coverage < 0.7 → le rapport est marqué INCOMPLETE et ne peut pas ACCEPT
3. Dans soic/report.py > generate_report_v2() : afficher le taux de couverture et marquer les gates NOT_EXECUTED avec ⊘ au lieu de ✗
4. Dans soic/converger.py > decide() : si coverage < 0.7 → retourner Decision.ABORT avec raison "Couverture insuffisante — exécuter le preflight d'abord"

Validation :
```python
# Gate non exécutée = 0.0, pas 5.0
from soic.models import GateResult, GateStatus, PhaseGateReport
r = PhaseGateReport(phase='ph5-qa')
r.gates = [
    GateResult('W-01','test','D1', GateStatus.PASS, 10.0, 'ok', 0, ''),
    GateResult('W-08','test','D5', GateStatus.NOT_EXECUTED, 0.0, 'tooling missing', 0, ''),
]
r.compute_score()
assert r.gates[1].score == 0.0  # Pas 5.0
assert r.coverage < 1.0
print(f"μ={r.mu}, coverage={r.coverage}")
```

═══════════════════════════════════════════════════════
CORRECTION 2 — SÉQUENCER LE PREFLIGHT DANS L'ORCHESTRATEUR
═══════════════════════════════════════════════════════

Problème : Le gate engine suppose que tooling/*.json existe, mais personne ne lance les scans. Les scripts tools/*.sh ne sont pas appelés par l'orchestrateur.

Correction dans orchestrator.py :
1. Ajouter une fonction `run_preflight(build_dir: str, local_url: str) -> dict` qui :
   - Vérifie que le build existe (build_dir/package.json)
   - Lance `npm run build` si pas de .next/
   - Lance `npx next start` en background sur un port libre
   - Exécute séquentiellement :
     * tools/lighthouse-scan.sh <url> → tooling/lighthouse.json
     * tools/a11y-scan.sh <url> → tooling/a11y.json
     * tools/headers-scan.sh <url> → tooling/headers.json
     * tools/ssl-scan.sh <url> → tooling/ssl.json
     * tools/deps-scan.sh <build_dir> → tooling/deps.json
   - Kill le serveur Next.js
   - Retourne un dict {tool: path_to_json} pour chaque scan réussi
2. Appeler run_preflight() AVANT le gate engine dans la séquence PH5-QA
3. Passer les paths des résultats au gate engine via un contexte partagé
4. Si un scan échoue (script absent, timeout) → log l'erreur, la gate correspondante sera NOT_EXECUTED

Contrainte : timeout de 60 secondes par scan, 5 minutes total pour le preflight.

═══════════════════════════════════════════════════════
CORRECTION 3 — DÉTECTION DE PLATEAU FONCTIONNELLE
═══════════════════════════════════════════════════════

Problème : Avec max_iter=3, il faut 3 points d'historique pour détecter un plateau (2 deltas ≤ 0 consécutifs). La condition ne se déclenche jamais. C'est du code mort.

Correction dans soic/converger.py :
1. Changer la logique : plateau = 1 delta ≤ 0 (pas 2)
   - Si μ(n) ≤ μ(n-1) après une correction → on stagne, inutile de continuer
2. Exception : si le nombre de gates FAIL a diminué même si μ stagne → continuer (on progresse qualitativement)
3. Augmenter max_iter à 4 pour donner une chance réelle à la boucle

```python
def _is_plateau(self, current: PhaseGateReport, history: list) -> bool:
    if len(history) < 1:
        return False
    prev = history[-1]
    mu_stagnant = current.mu <= prev.mu
    fewer_failures = current.fail_count < prev.fail_count
    if mu_stagnant and not fewer_failures:
        return True  # Vrai plateau
    return False
```

═══════════════════════════════════════════════════════
CORRECTION 4 — FEEDBACK PRIORISÉ (TOP 3 CRITIQUES)
═══════════════════════════════════════════════════════

Problème : Si 16 gates FAIL, le feedback injecté dans le prompt Claude est ~2000+ chars. Ça dilue le prompt principal et le LLM essaie de tout corriger à la fois (mal).

Correction dans soic/feedback_router.py :
1. Ajouter une priorité par dimension :
   - CRITIQUE (toujours inclus) : D4 Sécurité, D8 Conformité légale
   - HAUTE : D6 Accessibilité, D5 Performance
   - NORMALE : D1, D2, D3, D7, D9
2. La méthode generate_feedback() :
   - Trie les gates FAIL par priorité puis par score croissant
   - Retourne max 5 corrections (les plus critiques d'abord)
   - Ajoute en footer : "N autres corrections mineures reportées à l'itération suivante"
3. Chaque correction fait max 3 lignes : gate_id, diagnostic, action concrète

Format cible du feedback :
```
## Corrections requises (Itération N+1) — 5 prioritaires sur 12 FAIL

[D4/W-05] npm-audit — CRITIQUE
→ 3 vulnérabilités high dans express@4.17.1
→ Action : npm audit fix --force, vérifier que le build passe

[D8/W-14] legal-compliance — CRITIQUE
→ Politique de confidentialité : durée de conservation manquante
→ Action : Ajouter section "Durée de conservation" avec les durées par catégorie de RP

[D6/W-10] a11y-axe — HAUTE
→ 4 violations contrast-ratio sur la page d'accueil
→ Action : Augmenter le contraste des textes gris sur fond blanc (ratio min 4.5:1)

(+ 9 corrections mineures reportées)
```

═══════════════════════════════════════════════════════
CORRECTION 5 — W-14 LEGAL-COMPLIANCE : DÉTAIL PAR CHECK
═══════════════════════════════════════════════════════

Problème : W-14 affiche "3/6 checks" sans dire lesquels passent et lesquels échouent. Le feedback est inutilisable.

Correction dans soic/domain_grids/web.py > gate W-14 :
1. Les 6 checks doivent être explicites dans l'evidence :
   - CHECK 1 : Page /politique-de-confidentialite existe (HTTP 200)
   - CHECK 2 : Lien vers la politique dans le footer de chaque page
   - CHECK 3 : Mots-clés obligatoires présents dans la politique :
     * "responsable de la protection" ou "RPRP"
     * "renseignements personnels" ou "données personnelles"
     * "finalité" ou "fins de"
     * "durée de conservation" ou "période de conservation"
     * "droit d'accès" ET "rectification" ET "suppression"
     * "plainte" ou "recours"
   - CHECK 4 : Formulaires ont une checkbox consentement non pré-cochée
   - CHECK 5 : Mention de finalité visible avant le bouton submit
   - CHECK 6 : Lien politique de confidentialité dans/près du formulaire
2. L'evidence doit lister chaque check individuellement :
   ```
   CHECK 1: PASS — /politique-de-confidentialite → 200
   CHECK 2: FAIL — footer link missing on /services
   CHECK 3: PASS — 6/6 keywords found
   CHECK 4: FAIL — checkbox on /contact is pre-checked
   CHECK 5: PASS — purpose statement found
   CHECK 6: FAIL — no privacy link near form on /contact
   ```
3. Le score = (checks passés / 6) × 10

═══════════════════════════════════════════════════════
CORRECTION 6 — GATE COOKIES LOI 25 (NOUVELLE : W-17)
═══════════════════════════════════════════════════════

Problème : Aucune gate ne vérifie le comportement runtime des cookies. La conformité Loi 25 exige qu'aucun cookie non essentiel ne soit posé avant consentement explicite. Ça ne se vérifie pas en analysant le code source.

Ajouter dans soic/domain_grids/web.py :
1. Nouvelle gate W-17 cookie-consent, dimension D8, poids critique
2. Implémentation avec Playwright (npx playwright) ou à défaut curl :
   - Lancer le site localement
   - Charger la page d'accueil SANS interagir
   - Lister tous les cookies posés → doivent être 0 ou strictement nécessaires (session, CSRF)
   - Vérifier qu'aucune requête réseau vers des domaines tiers analytics/marketing n'a été émise (google-analytics, facebook, hotjar, etc.)
   - Si bannière cookies présente : cliquer "Refuser tout" → vérifier qu'aucun cookie marketing n'apparaît
   - Si bannière cookies absente ET cookies non essentiels détectés → FAIL immédiat
3. Liste de domaines tiers à bloquer :
   ```python
   TRACKER_DOMAINS = [
       'google-analytics.com', 'googletagmanager.com',
       'facebook.net', 'facebook.com/tr',
       'hotjar.com', 'clarity.ms',
       'doubleclick.net', 'googlesyndication.com',
       'linkedin.com/px', 'twitter.com/i/adsct',
       'tiktok.com/i/pixel', 'snap.licdn.com',
   ]
   ```
4. Fallback si Playwright non installé : vérifier dans le code source que les scripts tiers sont wrappés dans un conditionnel de consentement (analyse statique = score max 7.0, pas 10.0)

Mettre à jour soic/domain_grids/__init__.py pour inclure W-17 dans le set ph5-qa (17 gates au lieu de 16).

═══════════════════════════════════════════════════════
CORRECTION 7 — CLOSURE _RERUN → OBJET EXPLICITE
═══════════════════════════════════════════════════════

Problème : Le callback _rerun dans orchestrator.py capture url, client_dir, timestamp via closure. Si quelqu'un refactore run_pipeline, la closure casse silencieusement.

Correction dans orchestrator.py :
1. Créer une dataclass RerunContext :
   ```python
   @dataclass
   class RerunContext:
       url: str
       client_dir: str
       build_dir: str
       timestamp: str

       def rerun(self, feedback: str) -> PhaseGateReport:
           """Relance Claude CLI avec le feedback, puis réexécute les gates."""
           # ... logique actuellement dans la closure
   ```
2. Remplacer la closure par `ctx = RerunContext(...)` et passer `ctx.rerun` comme callback
3. Le RerunContext est testable indépendamment

═══════════════════════════════════════════════════════
CORRECTION 8 — TIMEOUT GLOBAL SUR LA BOUCLE
═══════════════════════════════════════════════════════

Problème : 4 itérations × (17 gates + appel Claude CLI ~5min) = potentiellement 25+ minutes sans garde-fou.

Correction dans soic/iterator.py > PhaseIterator :
1. Ajouter un paramètre `timeout_minutes: int = 15` au constructeur
2. Vérifier le temps écoulé avant chaque itération
3. Si timeout atteint → retourner LoopResult avec decision=ABORT et reason="Timeout global atteint ({timeout_minutes}min)"
4. Log le temps par itération pour diagnostic

═══════════════════════════════════════════════════════
CORRECTION 9 — TESTS UNITAIRES
═══════════════════════════════════════════════════════

Créer tests/test_soic/ avec les fichiers suivants :

1. test_models.py :
   - GateStatus.NOT_EXECUTED existe
   - PhaseGateReport.compute_score() avec mix PASS/FAIL/NOT_EXECUTED
   - NOT_EXECUTED → score 0.0
   - coverage calculé correctement

2. test_converger.py :
   - D4 FAIL + μ=9.5 → ITERATE (blocking)
   - D8 FAIL + μ=9.5 → ITERATE (blocking)
   - Tout PASS + μ≥seuil → ACCEPT
   - coverage < 0.7 → ABORT
   - Plateau détecté (μ stagne + même nombre de FAIL) → ABORT
   - μ stagne mais FAIL diminue → ITERATE (pas plateau)

3. test_feedback_router.py :
   - 16 gates FAIL → max 5 dans le feedback
   - D4/D8 toujours inclus même si score > autres
   - Format du feedback conforme

4. test_gate_engine.py :
   - Phase ph5-qa → 17 gates instanciées
   - Phase ph0-discovery → 4 gates
   - Gate manquante → NOT_EXECUTED

5. test_report.py :
   - ⊘ pour NOT_EXECUTED dans le rapport
   - Coverage affiché
   - INCOMPLETE si coverage < 0.7

Commande de validation :
```bash
cd ~/___00___MARK_SYSTEMS_BIZ___/NEXOS/nexos_v.3.0
python -m pytest tests/test_soic/ -v --tb=short
```
Tous les tests doivent passer.

═══════════════════════════════════════════════════════
ORDRE D'EXÉCUTION
═══════════════════════════════════════════════════════

1. CORRECTION 1 (faux 5.0) — fondation, tout le reste en dépend
2. CORRECTION 3 (plateau) — simple, isolé
3. CORRECTION 7 (closure) — simple, isolé
4. CORRECTION 8 (timeout) — simple, isolé
5. CORRECTION 4 (feedback priorisé) — dépend des modèles corrigés
6. CORRECTION 5 (W-14 détail) — dépend du feedback
7. CORRECTION 6 (W-17 cookies) — nouvelle gate
8. CORRECTION 2 (preflight orchestrateur) — intégration finale
9. CORRECTION 9 (tests) — valide tout

═══════════════════════════════════════════════════════
RÈGLES
═══════════════════════════════════════════════════════

- Ne casse PAS la backward compat (soic.gate.evaluate_gate, soic.dimensions.calculate_mu)
- Chaque correction : modifier → valider compilation → valider import → passer à la suivante
- Si une correction bloque, documente le problème dans soic/CORRECTIONS_LOG.md et passe à la suivante
- À la fin, exécute la validation complète :
  ```bash
  python -c "
  from soic import GateEngine, PhaseIterator, Converger
  from soic.models import GateStatus
  assert hasattr(GateStatus, 'NOT_EXECUTED')
  from soic.domain_grids import get_phase_gates
  assert len(get_phase_gates('ph5-qa')) == 17
  print('ALL CORRECTIONS VALIDATED')
  "
  ```
- Crée soic/CORRECTIONS_LOG.md avec pour chaque correction : statut (DONE/PARTIAL/BLOCKED), fichiers modifiés, tests passés

Signal de complétion :
```
══════════════════════════════════════
✅ SOIC v3.0 CORRECTIONS — TERMINÉ
══════════════════════════════════════
Corrections : 9/9
Tests        : X/X passed
Gates ph5-qa : 17
Coverage     : enforced (< 0.7 = ABORT)
Timeout      : 15min global
Feedback     : top 5 priorisé
W-17 cookies : actif
══════════════════════════════════════
```
```
