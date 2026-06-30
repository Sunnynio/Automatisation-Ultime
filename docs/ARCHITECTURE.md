# ARCHITECTURE — État technique réel

> Ce fichier documente ce qui **existe réellement aujourd'hui**, pas ce qui est prévu.
> Pour l'architecture cible (diagrammes Mermaid, flux de données), voir `docs/architecture.md`.
> Dernière mise à jour : 2026-06-30

---

## Workspace Notion

- **Workspace** : Espace de Franck Savin
- **Base "Master Board"** :
  - URL : https://app.notion.com/p/0de619a1e693410d94946c4f5fdaf30a
  - Data Source ID : `collection://afa424a0-5fe7-47c5-8a66-06a6e413cda0`
  - Vue active : Kanban groupé par Statut
  - Propriétés présentes au 30/06/2026 : Durée, Support, Pays/Lieu, Statut, Catégorie\*, Échéance\*, Notes\*
  - \* Ajoutées par Claude (claude.ai web) — à valider par Franck

---

## Statut des connecteurs (au 30/06/2026)

| Connecteur | Interface | Statut | Notes |
|---|---|---|---|
| Notion | Claude web | Actif | Utilisé pour créer le Master Board |
| Google Calendar | Claude web | Non connecté | Pas de connecteur disponible côté web Claude |
| GitHub | Claude web | Non connecté | Raison de l'ouverture de cette session Claude Code |
| GitHub | Claude Code | Actif | Utilisé pour cette session de documentation |

---

## Infrastructure scripts

Rien de déployé en production à ce jour. Les scripts présents dans `/scripts/` sont des prototypes non testés avec des tokens réels.

| Script | État | Testé |
|---|---|---|
| `scripts/notion_api/fetch_tasks.py` | Prototype | Non |
| `scripts/notion_api/update_task.py` | Prototype | Non |
| `scripts/automation/context_filter.py` | Prototype | Non |
| `scripts/utils/` | Utilitaires | Non |

---

## Variables d'environnement requises

Voir `.env.example` à la racine. Aucun token n'est configuré en production (le `.env` n'est pas commité).

---

## Ce qui n'existe pas encore

- Synchronisation Calendar↔Notion (aucun scénario Make.com configuré)
- Script de résumé quotidien
- Déploiement cloud (Google Cloud Functions ou autre)
- Base Notion "Routines" et "Journal de Bord"
- Intégration Gemini API et Mistral API
