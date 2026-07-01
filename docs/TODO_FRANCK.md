# TODO FRANCK — Ce qui reste à faire

> Généré le 2026-07-01. Mis à jour après chaque session.
> Ce document liste uniquement ce que **Franck doit faire en personne** — tout ce qui pouvait être fait automatiquement l'a été.

---

## Déjà fait automatiquement cette session

- [x] Vue **"Par projet"** créée dans le Master Board (filtre Catégorie=Travail, groupé par Projet)
- [x] Script `scripts/automation/reset_routine.py` créé (décoche les cases d'une routine)
- [x] Schéma Notion corrigé : ajout de **En pause** + **En attente validation** dans Statut
- [x] Schéma Notion corrigé : ajout de **Saudi Arabia**, **Avion**, **Hôtel** dans Pays/Lieu
- [x] Schéma Notion corrigé : ajout de **Tablette** + **Global** dans Support
- [x] `.env.example` mis à jour avec les IDs des pages Routines pré-remplis
- [x] Bug `"1 jour+"` corrigé dans les scripts
- [x] `prompts/DISPATCH_AGENT.md` créé (system prompt pour ton agent dispatch)

---

## Ce qui reste pour toi

---

### 1. Configurer ton `.env` local _(10 min)_

**Priorité : FAIRE EN PREMIER — sans ça aucun script ne fonctionne.**

```bash
# Dans le dossier du projet :
cp .env.example .env
```

Puis ouvrir `.env` et remplir **uniquement** :

```
NOTION_TOKEN=secret_xxxxxxx   ← à trouver sur notion.so/my-integrations
```

Le reste est déjà pré-rempli (IDs des bases, IDs des pages Routines).

**Tester ensuite :**
```bash
pip install -r requirements.txt
python scripts/notion_api/fetch_tasks.py
```
Si tu vois la liste de tes tâches → c'est bon.

---

### 2. Tester le script de reset des routines _(2 min après le point 1)_

```bash
# Décoche toutes les cases de la Routine du Matin :
python scripts/automation/reset_routine.py --matin

# Décoche toutes les cases d'Avant Aéroport :
python scripts/automation/reset_routine.py --aeroport
```

Vérifier dans Notion que les cases sont bien décochées après l'exécution.

---

### 3. Make.com — Reset automatique Routine du Matin _(30 min)_

**Objectif :** chaque nuit à 3h00 (ou l'heure de ton choix), toutes les cases de la Routine du Matin sont décochées automatiquement.

**Option A — Simple (recommandée) : webhook Make.com → script local**

1. Dans Make.com : créer un nouveau scénario
2. Module 1 : **Scheduler** → Every day à 03:00 (Bangkok = UTC+7, donc 20:00 UTC la veille)
3. Module 2 : **HTTP → Make a request** → POST vers un webhook de ton choix
4. Sur ton PC/serveur : exposer le script avec un outil comme `ngrok` ou le déployer sur un petit VPS

**Option B — 100% Make.com (sans script Python)**

1. Scénario Make.com avec Scheduler (03:00 chaque nuit)
2. Module : **Notion → Get a Page's Content** → Page ID : `38fcace54fe1819e8b68f3208b6c7d1c`
3. Module : **Notion → List All Blocks** (blocks de la page Matin)
4. Module : **Iterator** (itérer sur chaque bloc)
5. Module : **Router** → si bloc type = `to_do` ET `checked = true`
6. Module : **Notion → Update a Block** → `checked: false`

**Option C — Manuel pour commencer**

Lancer chaque matin à la main : `python scripts/automation/reset_routine.py --matin`
Upgrader vers Make.com quand c'est une douleur.

---

### 4. Make.com — Reset automatique Avant Aéroport _(15 min)_

Même logique que le point 3, mais :
- Trigger : **pas un cron** — déclencher 24h après le dernier check (ou bouton manuel)
- Page ID : `38fcace54fe1819fa390d727895c733e`

**Option simple pour l'instant :** lancer manuellement après un voyage :
```bash
python scripts/automation/reset_routine.py --aeroport
```

Make.com peut attendre que tu aies le reset Matin en place d'abord.

---

### 5. Widgets Routines sur mobile et PC _(5 min)_

Ajouter ces deux pages en favori / widget / raccourci :

| Routine | URL |
|---|---|
| ☀️ Routine du Matin | https://app.notion.com/p/38fcace54fe1819e8b68f3208b6c7d1c |
| ✈️ Avant Aéroport | https://app.notion.com/p/38fcace54fe1819fa390d727895c733e |

**Sur téléphone (iOS/Android) :**
1. Ouvrir Notion → naviguer vers la page
2. Appui long sur l'icône → "Ajouter à l'écran d'accueil"
OU utiliser le widget Notion officiel (iOS 16+ / Android)

**Sur PC :**
1. Épingler l'onglet dans le navigateur
2. OU créer un raccourci bureau vers l'URL

---

### 6. Agent dispatch — Configurer le system prompt _(5 min)_

1. Ouvrir le fichier `prompts/DISPATCH_AGENT.md` dans le repo
2. Copier tout le contenu
3. Le coller comme **system prompt** (ou contexte d'initialisation) de ton agent
4. Tester avec : "j'ai 2h devant moi, énergie Moyenne, je suis à Bangkok sur PC"

L'agent devrait répondre avec un mini-agenda tiré de tes tâches Notion.

---

### 7. Décision : `Priorité projet` dans la base Projets _(2 min)_

La base **Projets** a encore un champ `Priorité projet` avec les anciennes valeurs (Urgent / Important / Secondaire) — champ de niveau projet, pas de tâche.

**Deux options :**
- **Garder tel quel** → simple, suffisant pour quelques projets
- **Supprimer et remplacer** par `🚨 Urgence projet` + `💡 Importance projet` → cohérent avec la logique Eisenhower, mais plus de champs à remplir

Dis-moi ton choix et je m'en occupe.

---

### 8. Décision : Workflow Gemini/Mistral → repo _(10 min de réflexion)_

ClaudeCode et l'agent dispatch ont tous les deux accès au repo. Mais Gemini et Mistral n'ont pas d'accès GitHub direct.

**Options :**

| Option | Mécanisme | Effort |
|---|---|---|
| **A — Via l'agent dispatch** | L'agent dispatch reçoit les sorties de Gemini/Mistral, les intègre, et te demande de valider → tu demandes à Claude Code de commiter | Minimal |
| **B — Copier-coller via toi** | Gemini/Mistral produisent du contenu → tu le passes à Claude Code pour commit | Minimal, déjà fonctionnel |
| **C — Token GitHub dans Gemini/Mistral** | Configurer un accès GitHub API dans chaque outil | 30-60 min de setup, maintenu séparément |

**Recommandation** : Option A ou B pour commencer — suffisant vu que la délégation est manuelle de toute façon.

---

## Récapitulatif par urgence

| # | Tâche | Temps | Bloquant ? |
|---|---|---|---|
| 1 | Configurer `.env` + tester scripts | 10 min | **Oui** — rien ne marche sans ça |
| 2 | Tester reset_routine | 2 min | Après #1 |
| 3 | Widgets Routines | 5 min | Non |
| 4 | Agent dispatch system prompt | 5 min | Non |
| 5 | Make.com reset Matin | 30 min | Non |
| 6 | Make.com reset Aéroport | 15 min | Non |
| 7 | Décision Priorité projet | 2 min | Non |
| 8 | Décision Gemini/Mistral workflow | 10 min | Non |
