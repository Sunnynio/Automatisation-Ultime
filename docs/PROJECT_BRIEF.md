# PROJECT_BRIEF — Automatisation-Ultime

> Document de référence stable. Ne pas modifier sans décision explicite.
> Dernière mise à jour : 2026-06-30

---

## Vision

Créer un **Centre de Commande Personnel** pour un grand voyageur (Franck, profil multi-pays / multi-supports) qui combine :
- **Capture rapide** des tâches (vocale ou écrite, avec tri différé par l'IA)
- **Exécution intelligente** : session planning selon le temps disponible, le support et la localisation
- **Interface visuelle minimaliste** (widgets sur téléphone/PC) sans interaction obligatoire
- **Délégation manuelle** aux agents IA pour les tâches qui le méritent

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
```

> **Principe acté** : Calendar et Notion sont deux espaces distincts, pas synchronisés. Calendar gère les événements fixes (réunions, vols, rendez-vous). Notion gère les tâches et projets. Pas de sync bidirectionnelle — trop fragile, trop de maintenance.

| Composant | Rôle |
|---|---|
| **Notion** | Source de vérité unique (Master Board + Projets + Routines), widgets visuels |
| **Google Calendar** | Événements fixes uniquement — time blocking manuel |
| **Gemini** | Interface quotidienne, filtrage GPS, accès écosystème Google |
| **Mistral / Claude** | Analyse, daily digest, nettoyage zombie, exécution à la demande |

---

## Architecture Notion — deux niveaux

```
Master Board (toutes les tâches — perso + pro)
       │
       │  propriété RELATION "Projet"
       │
       ▼
Projets DB (gros projets multi-étapes)
   - Nom du projet
   - Client (SELECT)
   - Statut projet
   - Priorité projet
   - Budget / Deadline
   - Tâches (RELATION inverse → Master Board)
```

**Règles d'usage** :
- Une **action isolée** (email, appel, doc court) → Master Board uniquement, sans Projet rattaché
- Un **gros projet** (plusieurs semaines, plusieurs étapes, client identifié) → créer une entrée Projets + y rattacher toutes les tâches du Master Board
- Les tâches **perso** restent dans le Master Board, sans Projet (relation vide = OK)

**Projets actifs** (au 30/06/2026) :
- **PTT LNG** — Client : PTT, statut : En cours
- **Siam Paragon** — Client : Siam Paragon, statut : En cours

---

## Schéma des bases Notion

### Master Board

Propriétés minimales requises pour le filtrage contextuel (garder la liste courte — risque de friction à la saisie) :

| Propriété | Type | Valeurs |
|---|---|---|
| **Nom** | Titre | Libre |
| **Durée** | Sélection | 10 min / 30 min / 1h / 1h30 / 2h / Demi-journée / 1 jour + |
| **Support** | Sélection multiple | PC Portable / PC Fixe / Téléphone / Tablette / Global |
| **Pays/Lieu** | Sélection | Global / Thaïlande / France / Saudi Arabia / Avion / Hôtel / … |
| **Statut** | Kanban | Pas commencé / En cours / En pause / À déléguer à l'IA / En attente validation / Terminé |
| **Priorité** | Sélection | 🔴 Urgent / 🟠 Important / 🟡 Secondaire / ⚪ Optionnel |
| **Catégorie** | Sélection | Travail / Perso / Voyage / Admin / … |
| **Projet** | Relation | → base Projets (vide pour les tâches perso, requis pour tâches pro rattachées à un projet) |
| **Échéance** | Date | JJ/MM/AAAA |
| **Notes** | Texte | Libre |

Propriétés optionnelles (ajouter seulement si le besoin est prouvé) : Récurrence, Contexte, Heure de la journée, Dépendances, Délégable à l'IA, Statut IA, Livrable.

> Propriétés Points et Temps Réel (gamification) : **à supprimer** — la gamification par points est abandonnée au profit du Daily Digest.

### Base Projets

| Propriété | Type | Notes |
|---|---|---|
| **Nom du projet** | Titre | Libre |
| **Client** | Sélection | PTT / Siam Paragon / … (upgradable en RELATION si collaboration) |
| **Statut projet** | Sélection | Prospect / En cours / En pause / Terminé / Archivé |
| **Priorité projet** | Sélection | 🔴 Urgent / 🟠 Important / 🟡 Secondaire |
| **Budget** | Texte | Libre (pas de calcul automatique pour l'instant) |
| **Deadline** | Date | Date cible de livraison |
| **Notes** | Texte | Contexte, historique, liens utiles |
| **Tâches** | Relation | ← Master Board (sens inverse automatique de la propriété Projet) |

---

## Workflows validés (scope actuel)

### Principe transversal : Notion natif d'abord
Tester les filtres et vues sauvegardés dans Notion avant d'écrire tout script Python. Un filtre Notion "téléphone + global + < 30 min + pas commencé" couvre 80 % du besoin à 0 % de maintenance.

---

### 1. Capture d'abord, tri ensuite
**Besoin** : capturer une tâche sans friction, même en déplacement.

**Fonctionnement** :
- Saisie minimale : Nom + Durée (les autres propriétés restent vides)
- Triage différé : une fois par semaine (ou à la demande), l'IA parcourt les entrées sans propriétés et propose des valeurs inférées
- Franck valide en batch

**Outils** : Notion (saisie rapide), IA (enrichissement des propriétés par batch)

---

### 2. Session Planning ("J'ai 3h devant moi")
**Besoin** : structurer une session de travail complète, pas juste trouver une tâche.

**Fonctionnement** :
1. Franck indique son contexte : temps total, support, localisation
2. L'IA interroge Notion (filtres Durée + Support + Pays + Statut ≠ Terminé)
3. L'IA construit un mini-agenda pour toute la session (ex: tâche A 1h → pause → tâche B 45 min → tâche C 30 min)
4. Tri : Priorité > Durée > Échéance

**Algorithme de tri** : Priorité > Durée > Échéance (décidé le 30/06)

---

### 3. Routines (Matin / Soir / Voyage)
**Besoin** : checklists réutilisables sans recréer les tâches.

**Fonctionnement** :
- Base Notion dédiée "Routines", liée au Master Board
- Types : Matin, Soir, Voyage, Pré-départ, Post-arrivée
- Widgets Notion pour cocher sur mobile

---

### 4. Daily Digest (remplace la gamification par points)
**Besoin** : garder une vision sur ce qui a été fait chaque jour, ajustable dans le temps.

**Fonctionnement** :
- En fin de journée (ou à la demande), l'IA analyse les tâches `Statut = Terminé` du jour
- Génère un résumé court en langage naturel : ce qui a été fait, ce qui reste, patterns émergents
- Piloté manuellement via IA (Franck demande le digest quand il le souhaite — pas de déclencheur automatique au départ)
- Stocké dans une base Notion "Daily Digest"
- **Flexible** : la fréquence (quotidien → hebdo → autre) s'adapte à l'usage réel

> Point de départ : quotidien. On adapte selon ce qui colle vraiment.

---

### 5. Nettoyage zombie
**Besoin** : éviter l'accumulation de tâches obsolètes qui démoralisent.

**Fonctionnement** :
- Une fois par semaine, l'IA remonte les tâches `Statut = Pas commencé` depuis > 21 jours
- Pour chaque tâche : Garder / Archiver / Décomposer en sous-tâches ?
- Franck valide en 5-10 minutes

---

### 6. Délégation manuelle ("À déléguer à l'IA")
**Besoin** : confier une tâche à une IA sans la faire soi-même.

**Fonctionnement** :
- Franck bascule manuellement le statut "À déléguer à l'IA" et interpelle l'IA de son choix
- L'IA exécute (email, analyse, rapport), met à jour Notion (lien livrable)
- Franck valide le livrable

**Scope actuel** : délégation entièrement manuelle. Pas de détection autonome, pas de polling. L'autonomisation est hors scope pour l'instant.

---

## Documents liés

| Fichier | Contenu |
|---|---|
| `docs/architecture.md` | Diagrammes techniques détaillés, flux de données, sécurité |
| `docs/notion_structure.md` | Structure complète des bases Notion |
| `docs/api_guide.md` | Exemples de code API (Notion, Google, Mistral) |
| `brainstorming/decisions.md` | Toutes les décisions validées / en discussion / rejetées |
| `brainstorming/idees.md` | Idées et questions ouvertes pour le brainstorming |
