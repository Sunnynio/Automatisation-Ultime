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
  - Propriétés présentes au 30/06/2026 : Nom de la tâche, Durée, Support, Pays/Lieu, Statut, Priorité, Catégorie, Échéance, Notes
  - 12 tâches d'exemple créées le 30/06/2026
- **Base "Daily Digest"** :
  - URL : https://app.notion.com/p/30342149a740489f9cb85b99e82e7486
  - Data Source ID : `collection://83292ab8-5336-4e77-90f4-811ef80a9a7f`
  - Propriétés : Date (DATE), Résumé (RICH_TEXT), Tâches terminées (NUMBER), Temps total (RICH_TEXT), Observations (RICH_TEXT)
- **Page "Routines"** (parent) :
  - URL : https://app.notion.com/p/38fcace54fe1811cb644eb50e95fc648
  - **☀️ Routine du Matin** : https://app.notion.com/p/38fcace54fe1819e8b68f3208b6c7d1c
  - **✈️ Avant Aéroport** : https://app.notion.com/p/38fcace54fe1819fa390d727895c733e

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

Scripts Python fonctionnels (code réel, non du markdown). Non testés avec de vrais tokens — nécessite un fichier `.env` configuré.

| Script | Rôle | État |
|---|---|---|
| `scripts/notion_api/fetch_tasks.py` | CLI principal : liste tâches, digest, zombie, session | Fonctionnel, non testé en prod |
| `scripts/notion_api/update_task.py` | Mise à jour d'une tâche Notion | Prototype |
| `scripts/automation/context_filter.py` | Session Planning interactif | Fonctionnel, non testé en prod |
| `scripts/automation/daily_digest.py` | Daily Digest avec stats | Fonctionnel, non testé en prod |
| `scripts/automation/zombie_cleanup.py` | Nettoyage tâches > 21 jours | Fonctionnel, non testé en prod |
| `scripts/utils/config.py` | Chargement .env, client Notion | Fonctionnel |
| `scripts/utils/helpers.py` | Utilitaires Python (get_prop, filtres, tri) | Fonctionnel |
| `scripts/utils/logger.py` | Logger minimal | Fonctionnel |

Dépendances Python : `pip install -r requirements.txt` (notion-client, python-dotenv)

---

## Variables d'environnement requises

Voir `.env.example` à la racine. Aucun token n'est configuré en production (le `.env` n'est pas commité).

---

## Ce qui n'existe pas encore

- Synchronisation Calendar↔Notion — **décision définitive : pas de sync** (voir SESSION_LOG)
- Déploiement cloud (Google Cloud Functions ou autre)
- Base Notion "Routines"
- Intégration Gemini API et Mistral API
- Vues Notion sauvegardées "Session Planning" et "Zombie" (à créer dans l'interface Notion)
