# CLAUDE.md — Automatisation-Ultime

**Projet** : Centre de Commande Personnel pour Franck Savin (voyageur multi-pays, multi-supports) combinant Notion + Google Calendar + agents IA (Claude, Gemini, Mistral).

---

## Décisions figées (ne pas rouvrir)

- **Pas de sync Calendar↔Notion** — deux espaces distincts. Calendar = événements fixes. Notion = tâches. Décision définitive.
- **Délégation IA manuelle** — Franck bascule lui-même le statut "À déléguer à l'IA". Pas d'autonomie/polling dans le scope actuel.
- **Notion natif d'abord** — tester les vues/filtres Notion avant tout script Python.
- **Gamification par points abandonnée** — remplacée par le Daily Digest.

---

## Ordre de lecture minimum pour démarrer

| # | Fichier | Contenu |
|---|---|---|
| 1 | `docs/PROJECT_BRIEF.md` | Vision, architecture, schéma Master Board, 6 workflows validés |
| 2 | `docs/ARCHITECTURE.md` | État réel aujourd'hui (URLs Notion, statut scripts) |
| 3 | `docs/OPEN_QUESTIONS.md` | Ce qui reste à décider |
| 4 | `docs/SESSION_LOG.md` | Ce qui a réellement été fait (log chronologique) |
| 5 | `docs/STANDARDS.md` | Conventions de saisie pour tous les agents |

---

## Règle de contribution (obligatoire)

Toute session qui prend une décision structurante ou modifie l'état réel du système → **ajouter une entrée dans `docs/SESSION_LOG.md`** avec : date, IA impliquée, interface utilisée, actions réelles, décisions prises, ce qui reste en attente de validation.

---

## Bases Notion actives

| Base | URL |
|---|---|
| Master Board | https://app.notion.com/p/0de619a1e693410d94946c4f5fdaf30a |
| Projets | https://app.notion.com/p/a1b22b74a7414247a190eb999423a5d8 |
| Daily Digest | https://app.notion.com/p/30342149a740489f9cb85b99e82e7486 |
| Routines | https://app.notion.com/p/38fcace54fe1811cb644eb50e95fc648 |

---

## Stack technique

- Python 3 · `notion-client` · `python-dotenv` → `pip install -r requirements.txt`
- Scripts dans `scripts/` — fonctionnels, non testés avec tokens réels en prod
- Variables d'env : copier `.env.example` → `.env` (jamais commité)
- Déploiement : aucun — tout en local pour l'instant
