# STANDARDS — Conventions de saisie multi-agents

> Ce document est la référence unique pour tout agent (Claude, Gemini, Mistral, humain) qui crée ou modifie des données dans ce système.
> Dernière mise à jour : 2026-06-30

---

## Pourquoi ce document existe

Les tâches arrivent de sources différentes (agents IA distincts, saisie manuelle, briefings). Sans convention explicite, chaque source invente ses propres labels, produit des incohérences dans Notion, et casse les filtres.

**Règle** : tout ajout dans le Master Board ou la base Projets doit respecter ces standards, sans exception.

---

## 1. Priorité — table de correspondance canonique

Valeurs **Notion** (toujours utiliser ces libellés exacts, emoji inclus) :

| Valeur Notion | Signification | Aliases acceptés en entrée |
|---|---|---|
| `🔴 Urgent` | Bloquant, deadline proche ou critique | HAUTE, P1, Urgente, 🔴, rouge |
| `🟠 Important` | À faire cette semaine, impact fort | MOYENNE, P2, ⚠️, orange |
| `🟡 Secondaire` | À faire ce mois, non bloquant | BASSE, P3, Low, 🟡, jaune |
| `⚪ Optionnel` | Nice-to-have, aucune deadline | P4, Optionnel |

**Règle de conversion** : quand un agent reçoit un label externe (HAUTE, 🔴, ⚠️…), il le traduit en valeur Notion canonique **avant** la saisie. Ne jamais écrire "HAUTE" ou "P1" dans Notion.

---

## 2. Durée — estimation par défaut

Valeurs **Notion** disponibles : `10 min` / `30 min` / `1h` / `1h30` / `2h` / `Demi-journée` / `1 jour +`

Guide d'estimation :

| Type de tâche | Durée suggérée |
|---|---|
| Appel de coordination / sync | 30 min |
| Réunion / review / présentation | 1h |
| Configuration technique, debug | 1h30 – 2h |
| Rédaction / rapport / analyse | 2h – Demi-journée |
| Test terrain / démo client | Demi-journée |
| Développement / projet complexe | 1 jour + |

---

## 3. Support

Valeurs **Notion** disponibles (MULTI_SELECT) : `PC Portable` / `PC Fixe` / `Téléphone` / `Tablette` / `Global`

| Contexte | Support |
|---|---|
| Tâche technique, dev, rédaction | PC Portable |
| Appel, coordination à distance | Téléphone |
| Tâche réalisable sur n'importe quel device | Global |
| Tâche fixe au bureau | PC Fixe |

---

## 4. Pays / Lieu

Valeurs disponibles (non exhaustif) : `Global` / `Thaïlande` / `France` / `Saudi Arabia` / `Avion` / `Hôtel`

- **Global** = tâche réalisable depuis n'importe où (calls, docs, code)
- **Thaïlande** = requiert une présence physique à Bangkok ou en Thaïlande
- Ajouter un pays uniquement si la tâche est géo-contrainte

---

## 5. Statut des tâches (Master Board)

Valeurs canoniques dans l'ordre du workflow :

| Statut | Usage |
|---|---|
| `Pas commencé` | Défaut à la création |
| `En cours` | Tâche active |
| `En pause` | Bloquée, en attente d'un tiers |
| `À déléguer à l'IA` | Franck délègue manuellement à un agent |
| `En attente validation` | L'IA a produit un livrable, Franck doit valider |
| `Terminé` | Fait, fermé |

---

## 6. Statut des projets (base Projets)

| Statut | Usage |
|---|---|
| `Prospect` | Projet potentiel, pas encore signé |
| `En cours` | Projet actif |
| `En pause` | Projet suspendu |
| `Terminé` | Projet livré et clôturé |
| `Archivé` | Conservé pour référence, non actif |

Les **phases internes** (Stabilisation, Phase 1, Phase 2…) se documentent dans le champ **Notes** du projet, pas dans le statut. Exemple : `Phase : Stabilisation — Phase 1 livrée, Phase 2 en préparation (+500 caméras)`.

---

## 7. Nommage des tâches

Format : `[Verbe d'action] [Objet] [Contexte si nécessaire]`

- Commencer par un verbe à l'infinitif : *Mettre à jour*, *Valider*, *Finaliser*, *Tester*, *Envoyer*
- Éviter les noms sans verbe : ~~"Driver NMEA"~~ → **"Finaliser tests Driver NMEA"**
- Le contexte entre parenthèses est ok pour les détails techniques : `"Revoir avec Kai pour la reconnaissance faciale (infos en Sparameter)"`
- Pas de projet dans le nom si la relation Projet est remplie : ~~"Tests Drones DJI PTT"~~ → **"Tests Drones DJI — validation précision GPS avec AGH"**

---

## 8. Champs obligatoires à la création d'une tâche pro

| Champ | Obligatoire | Notes |
|---|---|---|
| Nom de la tâche | Oui | Verbe + Objet |
| Durée | Oui | Estimer si non précisé |
| Support | Oui | PC Portable par défaut |
| Pays / Lieu | Oui | Thaïlande ou Global pour les tâches pro |
| Statut | Oui | Pas commencé par défaut |
| Priorité | Oui | Voir table de correspondance §1 |
| Catégorie | Oui | `Travail` pour les tâches pro |
| Projet | Oui (si rattaché) | Relation vers la base Projets |
| Échéance | Si connue | Format AAAA-MM-JJ |

---

## 9. Deadlines — décalage et estimation

- Si une deadline est donnée en termes relatifs ("juin 2026"), utiliser le dernier jour du mois : `2026-06-30`
- Si une fourchette est donnée ("juin/juillet 2026"), prendre la borne haute : `2026-07-31`
- Si pas de deadline : laisser vide (ne pas inventer)
- Si on demande un décalage ("repousse de 2 mois") : +2 mois calendaires sur la date originale

---

## 10. Responsabilité de standardisation

**Tout agent** qui reçoit des tâches de l'extérieur (briefing, autre agent, liste brute) est responsable de :
1. Traduire les priorités vers les valeurs Notion canoniques (§1)
2. Estimer la durée si non fournie (§2)
3. Appliquer le nommage standard (§7)
4. Remplir tous les champs obligatoires (§8)
5. Logguer les tâches créées dans SESSION_LOG.md
