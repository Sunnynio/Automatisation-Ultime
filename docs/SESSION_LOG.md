# SESSION_LOG — Historique des actions réelles

Log chronologique des actions **réellement effectuées** (pas juste discutées).

> Règle : toute session qui prend une décision structurante ou modifie l'état réel du système doit ajouter une entrée ici avec date + IA impliquée.

Format d'une entrée :
```
## AAAA-MM-JJ — [Nom de l'IA] ([interface utilisée])

### Actions effectuées
- ...

### Décisions prises
- ...

### En attente de validation
- ...
```

---

## 2026-06-30 — Claude (claude.ai web)

### Actions effectuées
- Création de la base Notion "Master Board" dans le workspace "Espace de Franck Savin"
  - URL : https://app.notion.com/p/0de619a1e693410d94946c4f5fdaf30a
  - Data source : `collection://afa424a0-5fe7-47c5-8a66-06a6e413cda0`
  - Propriétés créées conformément au schéma cible : Durée, Support, Pays/Lieu, Statut (type Kanban)
  - 3 propriétés supplémentaires ajoutées par Claude : **Catégorie**, **Échéance**, **Notes** — à valider par Franck
- Création d'une vue Kanban groupée par Statut dans le Master Board
- Tentative de connexion au repo GitHub depuis claude.ai web → **échec** (aucun connecteur GitHub disponible côté interface web Claude)

### Décisions prises
- Ouvrir une session **Claude Code** pour la documentation du repo (contournement de l'absence du connecteur GitHub web)

### En attente de validation
- **Catégorie** : propriété ajoutée par Claude — valider son utilité et ses valeurs possibles
- **Échéance** : Claude l'a ajoutée ; vérifier si elle n'est pas redondante avec la propriété "Date Limite" déjà prévue au schéma
- **Notes** : propriété ajoutée par Claude — valider

---

## 2026-06-30 — Claude (Claude Code / session distante)

### Actions effectuées
- Analyse de l'état du repo (fichiers existants, historique git)
- Fusion et création de la structure de documentation multi-IA :
  - `README.md` — refactorisé en index de navigation
  - `docs/PROJECT_BRIEF.md` — créé (brief stable du projet)
  - `docs/SESSION_LOG.md` — créé (ce fichier)
  - `docs/OPEN_QUESTIONS.md` — créé (5 questions non tranchées)
  - `docs/ARCHITECTURE.md` — créé (état technique réel, distinct du doc de design)

### Décisions prises
- Maintien de `docs/architecture.md` (doc de design avec diagrammes Mermaid) sans modification
- Ajout de `docs/ARCHITECTURE.md` (état réel) comme document séparé
- README.md converti en index de navigation léger (contenu riche préservé dans docs/)

---

## 2026-06-30 — Franck + Claude (Claude Code — session brainstorming scope)

### Décisions prises

**Architecture**
- **Pas de sync bidirectionnelle Calendar↔Notion** — décision définitive. Google Calendar = événements fixes. Notion = tâches. Deux espaces distincts, pas reliés techniquement. Make.com non utilisé pour la sync.
- La taxonomie de propriétés du Master Board est à surveiller : ne pas la laisser grossir sans contrôle, risque de friction à la saisie.

**Délégation IA**
- La délégation reste **manuelle** pour l'instant : Franck bascule lui-même le statut "À déléguer à l'IA", puis interpelle l'IA de son choix. Pas de polling/webhook autonome dans le scope actuel.

**Scope des workflows — validés et reformulés**

| Workflow | Statut | Notes |
|---|---|---|
| Session Planning (ex-filtre contextuel) | Validé | "J'ai 3h" → l'IA construit un mini-agenda pour toute la session, pas juste une tâche |
| Capture d'abord, tri ensuite | Validé | Mode saisie ultra-rapide (titre seul), enrichissement des propriétés différé via IA |
| Routines (Matin / Soir / Voyage) | Validé | Inchangé |
| Weekly Digest (remplace Gamification) | Validé | Résumé hebdo des patterns réels ("tu travailles 3x mieux le matin"), pas de points/badges |
| Nettoyage zombie | Validé | Remontée hebdo des tâches "Pas commencé" depuis > 21 jours pour archiver ou décomposer |
| Délégation manuelle | Validé | Franck délègue manuellement, l'IA exécute à la demande — pas d'autonomie |
| Notion natif en premier | Validé | Tester les filtres sauvegardés Notion avant d'écrire tout script Python |

### En attente de validation
- Propriétés Catégorie, Échéance, Notes (créées par Claude web) — toujours à valider
- Supprimer ou archiver les propriétés Points / Temps Réel du schéma Master Board (gamification supprimée)
