# STANDARDS — Conventions de saisie multi-agents

> Ce document est la référence unique pour tout agent (Claude, Gemini, Mistral, humain) qui crée ou modifie des données dans ce système.
> Dernière mise à jour : 2026-07-01

---

## Pourquoi ce document existe

Les tâches arrivent de sources différentes (agents IA distincts, saisie manuelle, briefings). Sans convention explicite, chaque source invente ses propres labels, produit des incohérences dans Notion, et casse les filtres.

**Règle** : tout ajout dans le Master Board ou la base Projets doit respecter ces standards, sans exception.

---

## 1. Urgence — table de correspondance canonique

Critère : **deadline / temps contraint**. Répond à la question « faut-il le faire maintenant ? »

Valeurs **Notion** (toujours utiliser ces libellés exacts, emoji inclus) :

| Valeur Notion | Signification | Aliases acceptés en entrée |
|---|---|---|
| `🔴 Urgent` | Deadline proche, bloquant, ou pénalité si non fait aujourd'hui | HAUTE, P1, immédiat, ASAP, critique |
| `🟡 Normal` | À faire cette semaine, pas de blocage immédiat | MOYENNE, P2, normal |
| `⚪ Non urgent` | Aucune deadline, peut attendre | BASSE, P3, P4, Low, plus tard |

---

## 2. Importance — table de correspondance canonique

Critère : **impact / valeur ajoutée**. Répond à la question « est-ce que ça a de l'importance si ce n'est pas fait ? »

| Valeur Notion | Signification | Aliases acceptés en entrée |
|---|---|---|
| `🔴 Critique` | Impact fort, stratégique, irremplaçable | Critique, Essentiel, Clé |
| `🟠 Important` | Utile, valeur réelle, à faire | Important, ⚠️, orange |
| `🟡 Secondaire` | Peu d'impact, confort | Secondaire, BASSE, Low |
| `⚪ Optionnel` | Nice-to-have, aucune conséquence si non fait | Optionnel, P4 |

**Matrice Eisenhower — guide de décision rapide** :

| | Urgent 🔴 | Normal 🟡 | Non urgent ⚪ |
|---|---|---|---|
| **Critique 🔴** | Faire maintenant | Planifier | Planifier long terme |
| **Important 🟠** | Faire bientôt | Planifier cette semaine | Reporter |
| **Secondaire 🟡** | Déléguer | Reporter | Éliminer |
| **Optionnel ⚪** | Déléguer | Éliminer | Éliminer |

**Règle de conversion** : quand un agent reçoit un label externe (HAUTE, P1, ⚠️…), il le traduit en valeurs Notion canoniques (**Urgence** + **Importance** séparément) **avant** la saisie. Ne jamais écrire "HAUTE" ou "P1" dans Notion.

> Note : l'ancien champ `Priorité` (Urgent/Important/Secondaire/Optionnel) est **supprimé** et remplacé par ces deux champs séparés.

---

## 3. Énergie requise

Critère : **niveau de concentration / effort cognitif**. Utilisé pour adapter le Session Planning à l'état du moment.

| Valeur | Signification | Exemples |
|---|---|---|
| `Faible` | Tâche mécanique, administrative, peu de concentration | Cocher des cases, passer un appel court, trier des emails |
| `Moyenne` | Concentration normale, pas de deep work | Rédiger un email, préparer un document simple |
| `Élevée` | Deep work, créatif ou technique complexe | Développement, analyse, présentation, rédaction longue |

Si non renseigné à la création : laisser vide (ne pas inventer). L'IA peut l'inférer lors du triage différé.

---

## 4. Durée — estimation par défaut

Valeurs **Notion** disponibles : `10 min` / `30 min` / `1h` / `1h30` / `2h` / `Demi-journée` / `1 jour +`

| Type de tâche | Durée suggérée |
|---|---|
| Appel de coordination / sync | 30 min |
| Réunion / review / présentation | 1h |
| Configuration technique, debug | 1h30 – 2h |
| Rédaction / rapport / analyse | 2h – Demi-journée |
| Test terrain / démo client | Demi-journée |
| Développement / projet complexe | 1 jour + |

---

## 5. Support

Valeurs **Notion** disponibles (MULTI_SELECT) : `PC Portable` / `PC Fixe` / `Téléphone` / `Tablette` / `Global`

| Contexte | Support |
|---|---|
| Tâche technique, dev, rédaction | PC Portable |
| Appel, coordination à distance | Téléphone |
| Tâche réalisable sur n'importe quel device | Global |
| Tâche fixe au bureau | PC Fixe |

---

## 6. Pays / Lieu

Valeurs disponibles (non exhaustif) : `Global` / `Thaïlande` / `France` / `Saudi Arabia` / `Avion` / `Hôtel`

- **Global** = tâche réalisable depuis n'importe où (calls, docs, code)
- **Thaïlande** = requiert une présence physique à Bangkok ou en Thaïlande
- Ajouter un pays uniquement si la tâche est géo-contrainte

---

## 7. Statut des tâches (Master Board)

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

## 8. Statut des projets (base Projets)

| Statut | Usage |
|---|---|
| `Prospect` | Projet potentiel, pas encore signé |
| `En cours` | Projet actif |
| `En pause` | Projet suspendu |
| `Terminé` | Projet livré et clôturé |
| `Archivé` | Conservé pour référence, non actif |

Les **phases internes** (Stabilisation, Phase 1…) se documentent dans le champ **Notes** du projet, pas dans le statut.

---

## 9. Nommage des tâches

Format : `[Verbe d'action] [Objet] [Contexte si nécessaire]`

- Commencer par un verbe à l'infinitif : *Mettre à jour*, *Valider*, *Finaliser*, *Tester*, *Envoyer*
- Éviter les noms sans verbe : ~~"Driver NMEA"~~ → **"Finaliser tests Driver NMEA"**
- Le contexte entre parenthèses est ok pour les détails techniques
- Pas de projet dans le nom si la relation Projet est remplie

---

## 10. Champs obligatoires à la création d'une tâche pro

| Champ | Obligatoire | Notes |
|---|---|---|
| Nom de la tâche | Oui | Verbe + Objet |
| Durée | Oui | Estimer si non précisé |
| Support | Oui | PC Portable par défaut |
| Pays / Lieu | Oui | Thaïlande ou Global pour les tâches pro |
| Statut | Oui | Pas commencé par défaut |
| 🚨 Urgence | Oui | Voir table §1 |
| 💡 Importance | Oui | Voir table §2 |
| 🔋 Énergie | Si connue | Laisser vide si incertaine |
| Catégorie | Oui | `Travail` pour les tâches pro |
| Projet | Oui (si rattaché) | Relation vers la base Projets |
| Échéance | Si connue | Format AAAA-MM-JJ |

---

## 11. Deadlines — décalage et estimation

- Si une deadline est donnée en termes relatifs ("juin 2026") : dernier jour du mois `2026-06-30`
- Si une fourchette ("juin/juillet 2026") : borne haute `2026-07-31`
- Si pas de deadline : laisser vide (ne pas inventer)
- Si décalage demandé ("repousse de 2 mois") : +2 mois calendaires sur la date originale

---

## 12. Responsabilité de standardisation

**Tout agent** qui reçoit des tâches de l'extérieur (briefing, autre agent, liste brute) est responsable de :
1. Traduire l'urgence vers la valeur Notion canonique (§1)
2. Traduire l'importance vers la valeur Notion canonique (§2)
3. Estimer l'énergie si évidente (§3)
4. Estimer la durée si non fournie (§4)
5. Appliquer le nommage standard (§9)
6. Remplir tous les champs obligatoires (§10)
7. Logguer les tâches créées dans SESSION_LOG.md
