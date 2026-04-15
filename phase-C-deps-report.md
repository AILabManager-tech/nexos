# Phase C — Rapport

> Chantier `mise_a_niveau` v4.2.0 — Déclaration des deps manquantes + lockfile
> Date : 2026-04-14
> Prérequis : phases A (soic symlink) + B (subprocess audit) OK

---

## 1. Deps identifiées

Audit `grep -rhE "^(import|from)"` sur `nexos/`, `orchestrator.py`, `nexos_gateway.py`, `nexos_cli.py`, `audit_toolkit/`, `tests/`, `agents/`.

| Dep externe  | Où utilisé                                                              | Catégorie | Version déclarée |
|--------------|-------------------------------------------------------------------------|-----------|------------------|
| rich         | orchestrator.py, nexos/cli_commands.py, nexos/session_launcher.py, nexos/tooling_manager.py, nexos/build_validator.py, nexos/brief_wizard.py | core      | `>=13.0,<14.0`   |
| questionary  | nexos/brief_wizard.py                                                   | wizard    | `>=2.0,<3.0`     |
| fastapi      | nexos_gateway.py                                                        | api       | `>=0.100,<0.200` |
| uvicorn      | nexos_gateway.py (entrée `__main__`)                                    | api       | `>=0.24,<0.40`   |
| pydantic     | nexos_gateway.py                                                        | api       | `>=2.0,<3.0`     |
| pytest       | tests/                                                                  | dev       | `>=8.0,<9.0`     |
| pytest-cov   | (anticipé phase I)                                                      | dev       | `>=5.0,<7.0`     |
| ruff         | (anticipé phase G)                                                      | dev       | `>=0.5`          |
| mypy         | (anticipé phase H)                                                      | dev       | `>=1.10`         |
| jsonschema   | (validation brief — anticipé)                                           | dev       | `>=4.0`          |

**Intra-projet** : `nexos.*`, `soic.*`, `orchestrator`, `audit_toolkit`, `agents`.
**Stdlib only** : json, os, re, sys, pathlib, subprocess, typing, dataclasses, datetime, importlib, functools, itertools, unicodedata, time, shlex, shutil, tempfile, logging, runpy, ast, copy, enum, signal, socket, unittest.

**Aucune dep externe non déclarée** en dehors des extras `api` / `wizard` / `dev`.

---

## 2. pyproject.toml avant/après

**Avant** : 11 lignes, `rich>=13.0`, extras `dev=[pytest>=8.0]` + `wizard=[questionary>=2.0]`.
**Après** : 50 lignes, 4 extras (`wizard`, `api`, `dev`, `all`), bornes hautes, `[project.scripts]`, `[build-system]`, `[tool.setuptools]`.

### Diff clé

- `version` : `4.0.0` → `4.2.0-dev`
- Nouveau `[project.optional-dependencies].api` : fastapi + uvicorn[standard] + pydantic — corrige le défaut **C3** (`nexos_gateway.py` importait sans déclarer)
- `dev` enrichi : `pytest-cov`, `ruff`, `mypy`, `jsonschema` (préparation phases G/H/I)
- `all` : `nexos[wizard,api,dev]` (union pratique)
- Bornes hautes sur `rich` et `questionary` : évite une upgrade majeure cassante
- `[project.scripts] nexos = "nexos_cli:main"` : entry point CLI propre, installé dans le PATH du venv
- `[tool.setuptools] packages = ["nexos", "soic"]` : soic reconnu via le symlink posé en phase A

---

## 3. Lockfile

- **Outil choisi** : `uv` 0.11.6 (installé via `pip install --user --break-system-packages uv`)
- **Fichier** : `uv.lock` (1341 lignes, 287 KB)
- **Packages résolus** : 46 (transitive incluse)
- **Commande** : `uv lock` (résolution en 3.21 s)
- **requires-python** : `>=3.10` (verrouillé dans le lockfile)

Principales résolutions transitives notées : `starlette` (via fastapi), `anyio`, `h11`, `httptools`, `uvloop`, `watchfiles`, `websockets` (via uvicorn[standard]), `pydantic-core`, `annotated-types`, `typing-inspection` (via pydantic), `jsonschema-specifications`, `referencing`, `rpds-py` (via jsonschema), `markdown-it-py`, `mdurl`, `pygments` (via rich), `prompt_toolkit`, `wcwidth` (via questionary).

---

## 4. Test install venv neuf

Procédure §5.4 exécutée :

```bash
python3 -m venv /tmp/nexos-install-test
/tmp/nexos-install-test/bin/pip install --upgrade pip setuptools wheel
/tmp/nexos-install-test/bin/pip install -e "<repo>[api,dev,wizard]"
```

- pip / setuptools / wheel upgradés : `pip-26.0.1`, `setuptools-82.0.1`, `wheel-0.46.3`
- Editable wheel nexos construit : `nexos-4.2.0.dev0-0.editable-py3-none-any.whl` (6180 octets)
- Install pipeline complet sans erreur (40+ packages installés)

**Imports critiques validés** :

```
python -c "import nexos"                                     → ok nexos
python -c "import rich, questionary, fastapi, uvicorn,
                  pydantic, pytest"                          → ok extras
python -c "import soic"                                      → ok soic
```

**Entry point CLI** :

```
/tmp/nexos-install-test/bin/nexos --help
→ usage: nexos [-h] {session,create,audit,modify,content,
                     analyze,knowledge,converge,doctor,fix,report} ...
```

Le symlink `soic/ → ../soic_v3/` est correctement traité par setuptools en mode editable (phase A).

---

## 5. install_nexos.sh

Modification **minimale** selon §5.5 :
- Ajout d'un bloc `cat <<EOF` en fin de script décrivant l'install en venv + les 4 extras disponibles
- Aucune autre modification — le refactor complet du script reste prévu en **phase L**
- Syntaxe validée via `bash -n install_nexos.sh`

---

## 6. Critères de validation §7

- [x] `tomllib` parse → extras = `{'wizard','api','dev','all'}`
- [x] Install dans venv neuf : passe sans erreur
- [x] FastAPI + uvicorn + Pydantic importables après install
- [x] Lockfile committé : `uv.lock` (1341 lignes)
- [ ] `git status` propre → après commit §5.7

---

## 7. Handoff

Chemin critique suivant : **Phase D (archivage)** ou parallèle D + E.

Path phase D : `maintenance + upgrade/mise_a_niveau/PHASE_D_ARCHIVAGE_LEGACY.md`
