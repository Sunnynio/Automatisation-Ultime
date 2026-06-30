# OPEN_QUESTIONS — Points non tranchés

Ces 5 questions doivent orienter le brainstorming. Elles ne sont pas résolues et toute IA qui propose une réponse doit la valider avec Franck avant de la considérer comme une décision (→ la déplacer dans `brainstorming/decisions.md`).

---

## Q1 — Fiabilité de la sync bidirectionnelle Calendar↔Notion

La sync bidirectionnelle Calendar↔Notion **n'existe pas nativement** : ni Notion ni Google Calendar ne l'exposent en natif. Elle doit être construite (Make.com, script Python hébergé, ou webhook).

Questions ouvertes :
- Quel sens prioriser en premier ? Calendar→Notion semble le plus simple.
- Comment gérer les conflits (même tâche modifiée des deux côtés) ?
- Make.com est-il suffisamment fiable pour la production, ou faut-il prévoir un script Python dès le départ ?
- Comment éviter les doublons (l'ID unique `GCAL_{ID}` dans Notion est une piste) ?

---

## Q2 — Mécanisme technique des routines récurrentes

Notion **n'a pas de récurrence native** : une tâche marquée "Terminée" ne se recrée pas automatiquement. Plusieurs options :

- Script Python planifié (cron) qui recrée les tâches selon la propriété `Récurrence`
- Make.com avec un scénario de polling quotidien
- Duplication manuelle assistée par l'IA à la demande
- Case à cocher "Tâche Récurrente Automatique" + script Mistral

Aucune option n'a été tranchée. Critère de décision clé : complexité d'implémentation vs fréquence d'utilisation réelle.

---

## Q3 — Tension capture rapide / discipline de saisie

Le filtre contextuel ne fonctionne bien que si chaque tâche est correctement renseignée (Durée, Support, Pays/Lieu, Priorité). Or la capture rapide — notamment vocale — favorise des entrées incomplètes.

Questions ouvertes :
- Faut-il un mode de capture "rapide" (Nom + Durée seulement) avec enrichissement différé par l'IA ?
- Peut-on déléguer l'enrichissement des propriétés à Gemini ou Mistral après la capture ?
- Comment encourager la discipline de saisie sans friction excessive ?

---

## Q4 — Mécanique réelle de la délégation IA

Quand une tâche passe en statut "À déléguer à l'IA", comment Mistral le détecte-t-il et comment agit-il ?

Options :
- **Polling** : Mistral interroge Notion toutes les N minutes (simple, mais latence et coût API)
- **Webhook** : Notion déclenche une URL à chaque modification de statut (nécessite un serveur exposé)
- **Notification manuelle** : l'utilisateur ping Mistral quand il délègue (fiable, mais pas automatique)

Aucune option n'a été implémentée. Le choix impacte l'hébergement (Make.com, Google Cloud Functions, serveur dédié).

---

## Q5 — Accès et mise à jour du repo par les différentes IA

Plusieurs IA (Claude, Gemini, Mistral) doivent pouvoir contribuer au repo sans relire tout l'historique.

Questions ouvertes :
- Claude Code (cette session) a accès au repo via GitHub. Gemini et Mistral ont-ils un accès équivalent ?
- Si non, quel est le workflow : Franck copie-colle les sorties des autres IA dans les fichiers, puis Claude Code commite ?
- Faut-il un fichier `CONTRIBUTING.md` spécifique aux IA avec des instructions de format ?
- Comment éviter les conflits si deux IA écrivent sur le même fichier lors de sessions parallèles ?
