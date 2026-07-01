# PROJECT_BRIEF — Automatisation-Ultime

> Document de référence stable. Ne pas modifier sans décision explicite.
> Dernière mise à jour : 2026-07-01

---

## Vision

Créer un **Centre de Commande Personnel** pour un grand voyageur (Franck, profil multi-pays / multi-supports) qui combine :
- **Capture rapide** des tâches (vocale ou écrite, avec tri différé par l'IA)
- **Exécution intelligente** : session planning selon le temps disponible, le support, la localisation et l'énergie
- **Interface visuelle minimaliste** (widgets sur téléphone/PC) sans interaction obligatoire
- **Délégation** aux agents IA pour les tâches qui le méritent

---

## Architecture cible

```
Google Calendar                    Notion (Master Board)
(événements fixes)                 (tâches, source de vérité)
       │                                      │
  Time Blocking                         Notion API
  (créneaux bloqués)                         │
                                  ┌───────────┴───────────┐
                               Gemini                  Mistral / Claude
                          (interface principale)    (automatisation, analyse)
                          voix/texte, GPS, Google   scripts Python, livrables,
                          Calendar, Gmail, Drive     daily digest, zombie cleanup
                                       │
                                   Make.com
                             (reset routines, détection
                              IA vs physique, orchestration)
```

> **Principe acté** : Calendar et Notion sont deux espaces distincts, pas synchronisés. Calendar gère les événements fixes. Notion gère les tâches et projets. Pas de sync bidirectionnelle.

| Composant | Rôle |
|---|---|
| **Notion** | Source de vérité unique (Master Board + Projets + Routines + Daily Digest + Notes), widgets visuels |
| **Google Calendar** | Événements fixes uniquement — time blocking manuel |
| **Gemini** | Interface quotidienne, filtrage GPS, accès écosystème Google |
| **Mistral / Claude** | Analyse, daily digest, nettoyage zombie, exécution à la demande |
| **Make.com** | Orchestration : reset automatique des routines, détection IA vs physique |

---

## Architecture Notion — trois niveaux

```
Master Board (toutes les tâches — actionnables)
       │
       │  propriété RELATION "Projet"
       │
       ▼
Projets DB (gros projets multi-étapes)

Notes (pages Notion libres — mémos non-actionnables)
```

**Règles d'usage** :
- Une **action isolable** → Master Board uniquement
- Un **gros projet** (plusieurs semaines, plusieurs étapes) → créer une entrée Projets + y rattacher les tâches
- Les **mémos, notes, infos** (non-actionnables) → pages Notes, pas dans le Master Board

**Projets actifs** (au 30/06/2026) : PTT LNG, Siam Paragon.

---

## Schéma des bases Notion

### Master Board

| Propriété | Type | Valeurs |
|---|---|---|
| **Nom** | Titre | Libre |
| **Durée** | Sélection | 10 min / 30 min / 1h / 1h30 / 2h / Demi-journée / 1 jour + |
| **Support** | Sélection multiple | PC Portable / PC Fixe / Téléphone / Tablette / Global |
| **Pays/Lieu** | Sélection | Global / Thaïlande / France / Saudi Arabia / Avion / Hôtel / … |
| **Statut** | Kanban | Pas commencé / En cours / En pause / À déléguer à l'IA / En attente validation / Terminé |
| **🚨 Urgence** | Sélection | 🔴 Urgent / 🟡 Normal / ⚪ Non urgent |
| **💡 Importance** | Sélection | 🔴 Critique / 🟠 Important / 🟡 Secondaire / ⚪ Optionnel |
| **🔋 Énergie** | Sélection | Faible / Moyenne / Élevée |
| **Catégorie** | Sélection | Travail / Perso / Voyage / Admin / … |
| **Projet** | Relation | → base Projets (vide pour les tâches perso) |
| **Échéance** | Date | JJ/MM/AAAA |
| **Notes** | Texte | Libre |

> **Remplacement de `Priorité`** : l'ancien champ unique est remplacé par `Urgence` (deadline/temps) et `Importance` (impact). Logique Eisenhower : Urgent+Critique → maintenant ; Non urgent+Critique → planifier ; Urgent+Secondaire → déléguer ; Non urgent+Optionnel → éliminer.

Propriétés optionnelles (ajouter seulement si le besoin est prouvé) : Récurrence, Contexte, Heure de la journée, Dépendances, Délégable à l'IA, Statut IA, Livrable.

### Base Projets

| Propriété | Type | Notes |
|---|---|---|
| **Nom du projet** | Titre | Libre |
| **Client** | Sélection | PTT / Siam Paragon / … |
| **Statut projet** | Sélection | Prospect / En cours / En pause / Terminé / Archivé |
| **Priorité projet** | Sélection | 🔴 Urgent / 🟠 Important / 🟡 Secondaire |
| **Budget** | Texte | Libre |
| **Deadline** | Date | Date cible de livraison |
| **Notes** | Texte | Contexte, historique, liens utiles |
| **Tâches** | Relation | ← Master Board |

> Note : `Priorité projet` est un champ de niveau projet (pas de tâche) — non affecté par la migration Eisenhower du Master Board. À décider si ce champ doit également être splitté en Urgence+Importance.

### Pages Notes (hors bases)

Structure libre — pages Notion nommées par thème, pas une base de données :
- **Salons d'aéroport** — une sous-page par salon : contenu consommé, remboursement Dragon Pass
- **Mémos voyage** — notes vrac par destination/date
- Remplacement de WhatsApp pour les notes personnelles non-actionnables

### Base Daily Digest

| Propriété | Type | Notes |
|---|---|---|
| **Date** | Date | |
| **Résumé** | Texte | Généré par l'IA |
| **Tâches terminées** | Nombre | Tâches planifiées + capture libre |
| **Temps total** | Texte | |
| **Observations** | Texte | Patterns, remarques |

---

## Workflows validés

### Principe transversal : Notion natif d'abord
Tester les filtres et vues sauvegardés dans Notion avant d'écrire tout script Python.

---

### 1. Capture d'abord, tri ensuite
**Besoin** : capturer une tâche sans friction, même en déplacement.

**Fonctionnement** :
- Saisie minimale : Nom + Durée (les autres propriétés restent vides)
- Triage différé : une fois par semaine (ou à la demande), l'IA parcourt les entrées sans propriétés et propose des valeurs inférées
- Franck valide en batch

---

### 2. Session Planning ("J'ai 3h devant moi")
**Besoin** : structurer une session de travail complète.

**Fonctionnement** :
1. Franck indique son contexte : temps total, support, localisation, **niveau d'énergie**
2. L'IA interroge Notion (filtres Durée + Support + Pays + Énergie + Statut ≠ Terminé)
3. L'IA construit un mini-agenda pour toute la session (ex: tâche A 1h → pause → tâche B 45 min)
4. Tri : Urgence > Importance > Durée > Échéance

---

### 3. Routines (Matin / Soir / Voyage) avec reset automatique
**Besoin** : checklists réutilisables remises à zéro automatiquement.

**Fonctionnement** :
- Pages Notion sous "Routines", cases à cocher, widgets sur mobile
- Types : Matin, Soir, Voyage, Pré-départ, Post-arrivée

**Reset automatique (Make.com)** :
- **Routine du Matin** — reset chaque nuit à une heure définie (ex: 3h00) → toutes les cases décochées automatiquement
- **Liste Avant Aéroport** — reset 24h après le dernier check (ou à la demande manuelle)
- Mécanisme : scénario Make.com avec cron/scheduling + appel Notion API pour décocher les cases

---

### 4. Daily Digest
**Besoin** : vision sur ce qui a été fait chaque jour.

**Fonctionnement** :
- En fin de journée (ou à la demande), l'IA analyse les tâches `Statut = Terminé` du jour — qu'elles soient planifiées ou capturées librement (voir Workflow 7)
- Génère un résumé court : ce qui a été fait, ce qui reste, patterns émergents
- Stats simples : nombre de tâches, temps estimé, distribution Urgence/Importance
- Piloté manuellement via IA — pas de cron au départ
- Stocké dans la base Notion "Daily Digest"

---

### 5. Nettoyage zombie
**Besoin** : éviter l'accumulation de tâches obsolètes.

**Fonctionnement** :
- Une fois par semaine, l'IA remonte les tâches `Statut = Pas commencé` depuis > 21 jours
- Pour chaque tâche : Garder / Archiver / Décomposer ?
- Franck valide en 5-10 minutes

---

### 6. Délégation avec détection IA vs physique
**Besoin** : identifier ce qui est exécutable par une IA vs ce qui nécessite une action physique.

**Fonctionnement** :
1. Franck décrit ses tâches à faire à l'IA (ou Make.com les reçoit)
2. L'IA analyse chaque tâche et détermine :
   - **Délégable à l'IA** (rédiger un email, analyser un doc, développer du code) → tag automatique `À déléguer à l'IA` + ajouté à la queue de l'agent
   - **Action physique requise** (sortir les poubelles, aller au bureau) → reste dans le Master Board, statut normal
3. L'agent IA traite sa queue, produit un livrable, met à jour Notion (lien livrable + `Statut = En attente validation`)
4. Franck valide le livrable

**Scope actuel** : la détection peut être faite par l'IA à la demande. L'automatisation via Make.com est en cours de mise en place.

---

### 7. Capture libre → log automatique
**Besoin** : enregistrer ce qui a été fait sans avoir tout planifié à l'avance.

**Fonctionnement** :
1. Franck dit à l'IA : "Ce matin j'ai fait ça, ça, ça"
2. L'IA cherche chaque item dans le Master Board :
   - **Tâche trouvée** → `Statut = Terminé` + date de complétion
   - **Tâche non trouvée** → créée dans le Master Board + `Statut = Terminé` immédiatement
3. Toutes les tâches capturées alimentent le Daily Digest du soir
4. Aucune planification préalable requise — saisie après coup

---

## Documents liés

| Fichier | Contenu | Statut |
|---|---|---|
| `CLAUDE.md` | Init Claude Code : décisions figées, agents, lecture rapide | ✓ |
| `docs/STANDARDS.md` | Conventions de saisie pour tous les agents | ✓ |
| `docs/ARCHITECTURE.md` | État technique réel (URLs Notion, statut scripts) | ✓ |
| `docs/SESSION_LOG.md` | Log chronologique des actions réelles | ✓ |
| `docs/OPEN_QUESTIONS.md` | Questions non tranchées | ✓ |
| `prompts/DISPATCH_AGENT.md` | System prompt de l'agent dispatch | ✓ |
| `docs/architecture.md` | Diagrammes Mermaid, flux de données (design doc original) | ✓ (non modifié) |
| `docs/notion_structure.md` | Structure détaillée des bases Notion | À créer si besoin |
| `docs/api_guide.md` | Exemples de code API (Notion, Google, Mistral) | À créer si besoin |
| `brainstorming/decisions.md` | Décisions validées / rejetées | À créer si besoin |
| `brainstorming/idees.md` | Idées et questions pour le brainstorming | À créer si besoin |
