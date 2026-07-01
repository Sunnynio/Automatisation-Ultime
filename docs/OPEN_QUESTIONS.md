# OPEN_QUESTIONS — Points non tranchés

Ces questions doivent orienter le brainstorming. Toute IA qui propose une réponse doit la valider avec Franck avant de la considérer comme une décision (→ la déplacer dans `brainstorming/decisions.md`).

---

## ~~Q1 — Fiabilité de la sync bidirectionnelle Calendar↔Notion~~ — RÉSOLUE

**Décision (30/06/2026)** : Pas de sync. Google Calendar = événements fixes. Notion = tâches. Deux espaces distincts. Voir `docs/SESSION_LOG.md` entrée du 30/06 (brainstorming scope).

---

## ~~Q2 — Mécanisme technique des routines récurrentes~~ — RÉSOLUE

**Décision (01/07/2026)** : Make.com avec cron/scheduling + appel Notion API.
- **Routine du Matin** : reset chaque nuit à une heure définie (ex: 3h00) → toutes les cases décochées
- **Liste Avant Aéroport** : reset 24h après le dernier check (ou à la demande manuelle)
- En attente : création du scénario Make.com + définir l'heure exacte de reset matin

---

## Q3 — Tension capture rapide / discipline de saisie — PARTIELLEMENT RÉSOLUE

**Décision partielle (30/06/2026)** : le workflow "Capture d'abord, tri ensuite" est validé. Saisie minimale (Nom + Durée), enrichissement différé par l'IA.

**Décision complémentaire (01/07/2026)** : le workflow "Capture libre → log" complète ce dispositif — Franck peut dire à l'IA ce qu'il a fait après coup, sans planification préalable.

Question restante :
- Quel est le bon rythme de triage des tâches sans propriétés ? Hebdomadaire ? À la demande ? Déclenché automatiquement quand la base atteint X entrées non renseignées ?

---

## Q4 — Mécanique réelle de la délégation IA — CLARIFIÉE

**Décision (30/06/2026)** : délégation **manuelle** pour l'instant. Franck bascule le statut lui-même et interpelle l'IA.

**Extension (01/07/2026)** : Make.com peut également détecter automatiquement si une tâche est délégable à une IA (ex: rédaction, code, analyse) vs physique (sortir les poubelles, aller au bureau). En cours de mise en place.

Question restante (future) :
- Si le volume de délégations augmente, quand bascule-t-on vers un mécanisme semi-automatique ?

---

## Q5 — Accès et mise à jour du repo par les différentes IA

Plusieurs IA (Claude, Gemini, Mistral) doivent pouvoir contribuer au repo sans relire tout l'historique.

Questions ouvertes :
- Claude Code a accès au repo via GitHub. Gemini et Mistral ont-ils un accès équivalent ?
- Si non, quel est le workflow : Franck copie-colle les sorties des autres IA dans les fichiers, puis Claude Code commite ?
- Comment éviter les conflits si deux IA travaillent sur le même fichier lors de sessions parallèles ?
