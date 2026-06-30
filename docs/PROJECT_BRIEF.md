# PROJECT_BRIEF — Automatisation-Ultime

> Document de référence stable. Ne pas modifier sans décision explicite.
> Dernière mise à jour : 2026-06-30

---

## Vision

Créer un **Centre de Commande Personnel** pour un grand voyageur (Franck, profil multi-pays / multi-supports) qui combine :
- **Capture rapide** des tâches (vocale ou écrite via une IA interface)
- **Exécution intelligente** : filtrage contextuel selon le temps disponible, le support et la localisation
- **Interface visuelle minimaliste** (widgets sur téléphone/PC) sans interaction obligatoire
- **Délégation partielle** aux agents IA pour les tâches automatisables

---

## Architecture cible

```
Google Calendar  <──── sync bidirectionnelle ────>  Notion (Master Board)
                                                           │
                                                    Notion API / Make.com
                                                           │
                                              ┌────────────┴────────────┐
                                         Gemini                      Mistral
                                    (interface principale)       (automatisation)
                                    voix/texte, GPS, Google      scripts Python,
                                    Calendar, Gmail, Drive        analyse, livrables
```

| Composant | Rôle |
|---|---|
| **Notion** | Source de vérité unique (Master Board), widgets visuels |
| **Google Calendar** | Time Blocking, synchronisation avec Notion |
| **Gemini** | Interface quotidienne, filtrage GPS, accès écosystème Google |
| **Mistral** | Exécution en arrière-plan, analyse de données, préparation de livrables |
| **Make.com** | Orchestration no-code (prototype de sync Calendar↔Notion) |

---

## Schéma de la base Notion "Master Board"

Chaque tâche doit inclure les propriétés suivantes pour permettre le filtrage contextuel par les IA :

| Propriété | Type | Valeurs |
|---|---|---|
| **Nom** | Titre | Libre |
| **Durée** | Sélection | 10 min / 30 min / 1h / 1h30 / 2h / Demi-journée / 1 jour+ |
| **Support** | Sélection multiple | PC Portable / PC Fixe / Téléphone / Tablette / Global |
| **Pays/Lieu** | Sélection | Global / Thaïlande / France / Saudi Arabia / Avion / Hôtel / … |
| **Statut** | Kanban | Pas commencé / En cours / En pause / À déléguer à l'IA / En attente validation / Terminé |
| **Catégorie** | Sélection | À définir — propriété ajoutée par Claude le 30/06/2026, à valider |
| **Échéance** | Date | JJ/MM/AAAA |
| **Notes** | Texte | Libre — propriété ajoutée par Claude le 30/06/2026, à valider |
| **Priorité** | Sélection | Urgent / Important / Secondaire / Optionnel |
| **Récurrence** | Sélection | Unique / Quotidienne / Hebdomadaire / Mensuelle / Voyage / … |
| **Contexte** | Texte | Mots-clés (ex: "Admin", "Client X", "Apprentissage Thai") |

Propriétés supplémentaires validées (voir `brainstorming/decisions.md`) : Heure de la journée, Dépendances, Délégable à l'IA, Statut IA, Livrable, Date de Délégation, Date de Complétion, Temps Réel, Points.

---

## 4 Workflows cibles

### 1. Filtre contextuel ("J'ai 1 heure à tuer")
L'utilisateur indique son contexte (temps disponible, support, localisation). L'IA interroge Notion, croise avec Calendar, et retourne les 3 meilleures tâches triées par Priorité > Durée > Échéance.

### 2. Routines (Matin / Soir / Voyage)
Checklists réutilisables dans une base Notion dédiée, liées au Master Board. Mistral génère un résumé de complétion en fin de journée et l'envoie par email.

### 3. Gamification (Journal de Bord)
Suivi quotidien des tâches terminées (temps, points : 10 pts / 30 min). Résumé généré par Mistral et archivé dans une base "Journal de Bord" Notion. Bonus +50 % pour les tâches Urgent/Important.

### 4. Délégation IA ("À déléguer à l'IA")
Mistral détecte les tâches avec `Statut = À déléguer à l'IA`, les exécute (email, analyse, rapport), met à jour Notion (`Statut IA = Terminée`, lien livrable), et notifie l'utilisateur pour validation.

---

## Documents liés

| Fichier | Contenu |
|---|---|
| `docs/architecture.md` | Diagrammes techniques détaillés, flux de données, sécurité |
| `docs/notion_structure.md` | Structure complète des bases Notion (Master Board, Routines, Journal de Bord) |
| `docs/api_guide.md` | Exemples de code pour Notion API, Google Calendar API, Mistral API |
| `brainstorming/decisions.md` | Toutes les décisions validées / en discussion / rejetées |
| `brainstorming/idees.md` | Idées et questions ouvertes pour le brainstorming |
