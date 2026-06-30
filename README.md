# Automatisation-Ultime

> **Statut** : Phase d'élaboration — Brainstorming multi-IA en cours  
> **Démarré** : 30 juin 2026  
> **Repo** : [Sunnynio/Automatisation-Ultime](https://github.com/Sunnynio/Automatisation-Ultime)

Centre de Commande Personnel combinant Notion, Google Calendar et agents IA (Claude, Gemini, Mistral) pour un grand voyageur multi-supports.

---

## Ordre de lecture pour toute nouvelle session IA

Lire dans cet ordre avant de proposer quoi que ce soit :

| # | Fichier | Contenu |
|---|---|---|
| 1 | [`docs/PROJECT_BRIEF.md`](docs/PROJECT_BRIEF.md) | Vision, architecture cible, schéma Master Board, 4 workflows — **doc stable** |
| 2 | [`docs/SESSION_LOG.md`](docs/SESSION_LOG.md) | Ce qui a réellement été fait, session par session |
| 3 | [`docs/OPEN_QUESTIONS.md`](docs/OPEN_QUESTIONS.md) | 5 points non tranchés à garder en tête |
| 4 | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | État technique réel aujourd'hui (URLs Notion, statut connecteurs) |

Pour aller plus loin : [`docs/architecture.md`](docs/architecture.md) (diagrammes Mermaid), [`docs/notion_structure.md`](docs/notion_structure.md) (schéma Notion complet), [`docs/api_guide.md`](docs/api_guide.md) (exemples de code API), [`brainstorming/decisions.md`](brainstorming/decisions.md) (décisions validées / rejetées).

---

## État actuel du système (résumé)

- Workspace Notion : **Espace de Franck Savin**
- Base **Master Board** créée le 30/06/2026 — vue Kanban groupée par Statut
  - URL : https://app.notion.com/p/0de619a1e693410d94946c4f5fdaf30a
- Connecteur Notion actif (Claude web) ; Calendar et GitHub non connectés côté Claude web
- Scripts Python dans `/scripts/` : prototypes, non testés avec des tokens réels
- Aucune sync Calendar↔Notion configurée, aucun déploiement cloud

---

## Règle de contribution (toutes IA)

Toute session qui prend une **décision structurante** ou modifie l'**état réel du système** (Notion, scripts, connecteurs) doit ajouter une entrée dans [`docs/SESSION_LOG.md`](docs/SESSION_LOG.md) avec :
- La date
- L'IA impliquée et l'interface utilisée
- Les actions réellement effectuées
- Les décisions prises
- Ce qui reste en attente de validation

---

## Structure du repo

```
Automatisation-Ultime/
├── README.md                        # Ce fichier : index de navigation
├── .env.example                     # Template tokens API (ne jamais commiter .env)
├── .gitignore
│
├── docs/
│   ├── PROJECT_BRIEF.md             # Brief stable du projet (vision, schema, workflows)
│   ├── SESSION_LOG.md               # Log chronologique des actions réelles
│   ├── OPEN_QUESTIONS.md            # 5 questions non tranchées
│   ├── ARCHITECTURE.md              # État technique réel (URLs, connecteurs)
│   ├── architecture.md              # Design doc : diagrammes Mermaid, flux de données
│   ├── notion_structure.md          # Structure détaillée des bases Notion
│   └── api_guide.md                 # Exemples de code API (Notion, Google, Mistral)
│
├── brainstorming/
│   ├── idees.md                     # Idées et questions ouvertes pour le brainstorming
│   ├── decisions.md                 # Décisions validées / rejetées / en discussion
│   └── sessions/
│       └── 2026-06-30.md            # Compte-rendu session Mistral (Vibe) du 30/06
│
├── scripts/
│   ├── notion_api/                  # fetch_tasks.py, update_task.py
│   ├── automation/                  # context_filter.py
│   └── utils/                       # config.py, helpers.py, logger.py
│
└── notion/
    ├── templates/master_board.json  # Template JSON du Master Board
    └── README.md
```
