# OPEN_QUESTIONS — Points non tranchés

Ces questions doivent orienter le brainstorming. Toute IA qui propose une réponse doit la valider avec Franck avant de la considérer comme une décision (→ la déplacer dans `brainstorming/decisions.md`).

---

## ~~Q1 — Fiabilité de la sync bidirectionnelle Calendar↔Notion~~ — RÉSOLUE

**Décision (30/06/2026)** : Pas de sync. Google Calendar = événements fixes. Notion = tâches. Deux espaces distincts. Voir `docs/SESSION_LOG.md` entrée du 30/06 (brainstorming scope).

---

## Q2 — Mécanisme technique des routines récurrentes

Notion **n'a pas de récurrence native** : une tâche marquée "Terminée" ne se recrée pas automatiquement. Plusieurs options :

- Script Python planifié (cron) qui recrée les tâches selon la propriété `Récurrence`
- Make.com avec un scénario de polling quotidien
- Duplication manuelle assistée par l'IA à la demande

Critère de décision clé : combien de tâches récurrentes Franck a-t-il vraiment dans son système ? Si < 10, la duplication manuelle suffit. Si > 30, il faut un script.

---

## Q3 — Tension capture rapide / discipline de saisie — PARTIELLEMENT RÉSOLUE

**Décision partielle (30/06/2026)** : le workflow "Capture d'abord, tri ensuite" est validé. Saisie minimale (Nom + Durée), enrichissement différé par l'IA.

Question restante :
- Quel est le bon rythme de triage ? Hebdomadaire ? À la demande ? Déclenché automatiquement quand la base atteint X entrées non renseignées ?

---

## Q4 — Mécanique réelle de la délégation IA — CLARIFIÉE

**Décision (30/06/2026)** : délégation **manuelle** pour l'instant. Franck bascule le statut lui-même et interpelle l'IA. Pas de polling/webhook/autonomie dans le scope actuel.

Question restante (future) :
- Si le volume de délégations augmente, quand bascule-t-on vers un mécanisme semi-automatique ? Quel seuil déclencherait la décision ?

---

## Q5 — Accès et mise à jour du repo par les différentes IA

Plusieurs IA (Claude, Gemini, Mistral) doivent pouvoir contribuer au repo sans relire tout l'historique.

Questions ouvertes :
- Claude Code a accès au repo via GitHub. Gemini et Mistral ont-ils un accès équivalent ?
- Si non, quel est le workflow : Franck copie-colle les sorties des autres IA dans les fichiers, puis Claude Code commite ?
- Comment éviter les conflits si deux IA travaillent sur le même fichier lors de sessions parallèles ?
