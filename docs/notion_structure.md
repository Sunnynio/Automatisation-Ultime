# 🗃️ Structure Détaillée de la Base de Données Notion

> **Dernière mise à jour** : 30 juin 2026  
> **Statut** : En élaboration (À valider avec les IA collaboratrices)  
> **Repository** : [Sunnynio/Automatisation-Ultime](https://github.com/Sunnynio/Automatisation-Ultime)

---

## 📌 **Sommaire**
1. [Introduction](#-introduction)
2. [Master Board (Base Principale)](#-master-board-base-principale)
3. [Base "Routines"](#-base-routines)
4. [Base "Journal de Bord"](#-base-journal-de-bord)
5. [Relations entre les Bases](#-relations-entre-les-bases)
6. [Exemples Concrets](#-exemples-concrets)
7. [Bonnes Pratiques](#-bonnes-pratiques)
8. [Export/Import](#-exportimport)

---

## 🎯 **Introduction**

Ce document détaille la **structure optimale** des bases de données Notion pour le **Système de Productivité Hybride**. L’objectif est de permettre :
- Un **filtrage intelligent** par les IA (Gemini, Mistral).
- Une **synchronisation fluide** avec Google Calendar.
- Une **visualisation claire** (widgets, tableaux de bord).

---

## 🏆 **Master Board (Base Principale)**

### **Description**
Base de données **centrale** qui contient **toutes les tâches** du système. Chaque tâche est un **enregistrement** avec des propriétés structurées pour un filtrage contextuel.

---

### **Propriétés**

#### **1. Propriétés Obligatoires**
| Nom               | Type               | Description                                                                                     | Valeurs Possibles (Exemples)                                                                 | Format/Exemple                     |
|-------------------|--------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------|
| **Nom**           | Titre              | Nom de la tâche.                                                                                 | Libre                                                                                       | "Relancer client X"              |
| **⏱️ Durée**      | Sélection          | Temps estimé pour compléter la tâche.                                                         | 10 min, 30 min, 1h, 1h30, 2h, Demi-journée, 1 jour, 2 jours +                               | "30 min"                          |
| **💻 Support**     | Sélection Multiple | Supports compatibles pour réaliser la tâche.                                                   | PC Portable, PC Fixe, Téléphone, Tablette, Global                                          | ["PC Portable", "Téléphone"]     |
| **🌍 Pays/Lieu**   | Sélection          | Localisation requise ou actuelle pour la tâche.                                               | Global, Thaïlande, France, Saudi Arabia, Avion, Hôtel, Bureau                              | "Thaïlande"                      |
| **⚙️ Statut**      | Statut (Kanban)   | État actuel de la tâche.                                                                       | Pas commencé, En cours, En pause, À déléguer à l’IA, En attente de validation, Terminé       | "À déléguer à l’IA"              |
| **🎯 Priorité**    | Sélection          | Niveau de priorité de la tâche.                                                                 | Urgent, Important, Secondaire, Optionnel, Sans priorité                                   | "Urgent"                         |
| **🔄 Récurrence**  | Sélection          | Fréquence de la tâche.                                                                          | Unique, Quotidienne, Hebdomadaire, Mensuelle, Trimestrielle, Voyage, Pré-départ, Post-arrivée | "Quotidienne"                    |

---

#### **2. Propriétés Recommandées**
| Nom               | Type               | Description                                                                                     | Valeurs Possibles (Exemples)                                                                 | Format/Exemple                     |
|-------------------|--------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------|
| **📌 Contexte**    | Texte              | Mots-clés pour un filtrage contextuel (ex: domaine, projet, type de tâche).                      | "Admin", "Client X", "Apprentissage Thai", "Projet Cobra", "Santé", "Finances"                | ["Admin", "Client X"]             |
| **🕒 Heure de la journée** | Sélection   | Moment idéal pour réaliser la tâche.                                                          | Matin (6h-12h), Après-midi (12h-18h), Soir (18h-24h), Nuit (0h-6h)                              | "Matin"                          |
| **🔗 Dépendances** | Relation           | Lien vers d’autres tâches Notion (blocages).                                                    | Tâches Notion (ex: "Tâche A doit être terminée avant Tâche B")                              | [Tâche A, Tâche B]                |
| **📅 Date Limite** | Date               | Échéance de la tâche (si applicable).                                                           | JJ/MM/AAAA                                                                                   | 05/07/2026                        |
| **📅 Date de Début** | Date            | Date à partir de laquelle la tâche peut être réalisée.                                         | JJ/MM/AAAA                                                                                   | 01/07/2026                        |
| **🔢 Énergie Requise** | Sélection     | Niveau d’énergie physique/mentale nécessaire.                                                  | Faible, Moyenne, Élevée, Très élevée                                                          | "Moyenne"                        |
| **👤 Assigné à**    | Personne          | Personne responsable de la tâche (pour les projets collaboratifs).                           | Franck Savin, Équipe X, Non assigné                                                          | "Franck Savin"                   |
| **📝 Notes**       | Texte              | Détails supplémentaires, liens, ou instructions.                                             | Libre                                                                                       | "Voir doc joint : [lien]"         |
| **🏷️ Tags**       | Sélection Multiple | Tags pour un filtrage avancé.                                                                   | #Urgent, #Automatisable, #Voyage, #Récurrent                                                   | ["#Urgent", "#Voyage"]           |

---

#### **3. Propriétés pour l’Automatisation (Mistral)**
| Nom               | Type               | Description                                                                                     | Valeurs Possibles (Exemples)                                                                 | Format/Exemple                     |
|-------------------|--------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------|
| **🤖 Délégable à l’IA** | Case à cocher | Indique si la tâche peut être entièrement ou partiellement délégable à une IA.               | Oui/Non                                                                                     | ✅ (coché)                         |
| **📄 Livrable**    | URL               | Lien vers le livrable généré par l’IA (ex: Google Doc, email brouillon).                       | URL                                                                                         | "https://docs.google.com/..."    |
| **🔄 Statut IA**   | Sélection          | État de la délégation à l’IA.                                                                  | Non délégée, En attente, En cours, Terminée, Échec                                          | "En attente"                      |
| **📅 Date de Délégation** | Date      | Date à laquelle la tâche a été délégée à l’IA.                                                 | JJ/MM/AAAA                                                                                   | 30/06/2026                        |

---

#### **4. Propriétés pour la Gamification**
| Nom               | Type               | Description                                                                                     | Valeurs Possibles (Exemples)                                                                 | Format/Exemple                     |
|-------------------|--------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------|
| **✅ Date de Complétion** | Date      | Date à laquelle la tâche a été marquée comme terminée.                                       | JJ/MM/AAAA                                                                                   | 30/06/2026                        |
| **⏱️ Temps Réel** | Nombre           | Temps réel passé sur la tâche (en minutes).                                                   | Nombre entier                                                                               | 45                                |
| **🌟 Points**      | Nombre           | Points attribués pour la tâche (pour la gamification).                                        | Nombre entier                                                                               | 10                                |

---

### **Vues Recommandées pour le Master Board**

#### **1. Vue Kanban (Par Statut)**
- **Filtres** : Aucun (toutes les tâches).
- **Groupement** : Par `Statut`.
- **Tri** : Par `Priorité` (Urgent → Optionnel), puis par `Date Limite`.
- **Utilité** : Visualiser l’avancement global des tâches.

#### **2. Vue Tableau (Filtre Contextuel)**
- **Filtres** : Dynamiques (ex: `Pays = Thaïlande` **ET** `Support contient Téléphone`).
- **Colonnes visibles** : `Nom`, `Durée`, `Priorité`, `Contexte`, `Date Limite`.
- **Tri** : Par `Priorité`, puis par `Durée`.
- **Utilité** : Répondre à des requêtes comme "Quelles tâches puis-je faire en 30 min sur mon téléphone ?".

#### **3. Vue Calendrier (Par Date)**
- **Filtres** : `Date Limite` ou `Date de Début` définie.
- **Affichage** : Tâches organisées par date.
- **Utilité** : Visualiser les échéances et planifier le temps.

#### **4. Vue Liste (Par Priorité)**
- **Filtres** : `Statut ≠ Terminé`.
- **Groupement** : Par `Priorité`.
- **Tri** : Par `Date Limite`.
- **Utilité** : Prioriser les tâches urgentes/importantes.

#### **5. Vue "À Déléguer à l’IA"**
- **Filtres** : `Statut = À déléguer à l’IA` **OU** `Délégable à l’IA = Oui`.
- **Colonnes visibles** : `Nom`, `Contexte`, `Statut IA`, `Date de Délégation`.
- **Utilité** : Suivre les tâches en attente d’exécution par l’IA.

---

## 🔄 **Base "Routines"**

### **Description**
Base dédiée aux **checklists réutilisables** pour les routines quotidiennes ou spécifiques (ex: matin, soir, voyage).

---

### **Propriétés**
| Nom               | Type               | Description                                                                                     | Valeurs Possibles (Exemples)                                                                 | Format/Exemple                     |
|-------------------|--------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------|
| **Nom**           | Titre              | Nom de la routine.                                                                              | "Routine Matin", "Routine Voyage", "Checklist Pré-départ"                                    | "Routine Matin"                  |
| **Type**          | Sélection          | Type de routine.                                                                               | Matin, Soir, Voyage, Pré-départ, Post-arrivée, Hebdomadaire, Mensuelle                          | "Matin"                          |
| **Éléments**      | Relation           | Lien vers les tâches du *Master Board* incluses dans cette routine.                           | Tâches Notion                                                                               | [Tâche 1, Tâche 2, Tâche 3]       |
| **📌 Ordre**      | Nombre           | Ordre d’affichage des éléments dans la routine.                                               | Nombre entier                                                                               | 1, 2, 3                           |
| **✅ Complétion**  | Case à cocher     | Indique si la routine a été complétée aujourd’hui.                                             | Oui/Non                                                                                     | ✅ (coché)                         |
| **📅 Dernière Complétion** | Date    | Date de la dernière fois où la routine a été complétée.                                       | JJ/MM/AAAA                                                                                   | 30/06/2026                        |

---

### **Vues Recommandées pour les Routines**

#### **1. Vue Tableau (Par Type)**
- **Filtres** : Aucun.
- **Groupement** : Par `Type`.
- **Tri** : Par `Ordre`.
- **Utilité** : Visualiser toutes les routines organisées par type.

#### **2. Vue "À Faire Aujourd’hui"**
- **Filtres** : `Type = Matin` **OU** `Type = Soir` (selon l’heure actuelle).
- **Colonnes visibles** : `Nom`, `Éléments`, `Complétion`.
- **Utilité** : Afficher les routines du jour.

---

## 📊 **Base "Journal de Bord"**

### **Description**
Base qui **archive les résumés quotidiens** générés par Mistral, avec des statistiques de productivité.

---

### **Propriétés**
| Nom               | Type               | Description                                                                                     | Valeurs Possibles (Exemples)                                                                 | Format/Exemple                     |
|-------------------|--------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------|
| **📅 Date**       | Date               | Date du journal.                                                                               | JJ/MM/AAAA                                                                                   | 30/06/2026                        |
| **📝 Résumé**     | Texte              | Résumé quotidien généré par Mistral (ex: "8 tâches terminées, 4h15 travaillées").              | Libre                                                                                       | "8 tâches, 4h15, +20% vs hier"    |
| **📈 Tâches Terminées** | Nombre     | Nombre de tâches marquées comme terminées ce jour.                                             | Nombre entier                                                                               | 8                                 |
| **⏱️ Temps Total** | Nombre           | Temps total travaillé (en minutes).                                                           | Nombre entier                                                                               | 255 (4h15)                       |
| **🎯 Priorités**   | Texte              | Répartition des tâches par priorité (ex: "Urgent: 2, Important: 3").                          | Libre                                                                                       | "Urgent: 2, Important: 3"         |
| **🌍 Localisation** | Sélection          | Pays où l’utilisateur était ce jour.                                                          | Global, Thaïlande, France, etc.                                                             | "Thaïlande"                      |
| **📊 Graphique**   | Médias             | Capture d’écran ou lien vers un graphique de productivité.                                    | URL ou fichier image                                                                         | "[Lien vers graphique]"           |

---

### **Vues Recommandées pour le Journal de Bord**

#### **1. Vue Calendrier (Par Date)**
- **Filtres** : Aucun.
- **Affichage** : Journaux organisés par date.
- **Utilité** : Visualiser l’historique quotidien.

#### **2. Vue Liste (Tri par Temps Total)**
- **Filtres** : Aucun.
- **Tri** : Par `Temps Total` (décroissant).
- **Utilité** : Identifier les jours les plus productifs.

#### **3. Vue "Statistiques Mensuelles"**
- **Filtres** : `Date` dans le mois en cours.
- **Groupement** : Par semaine.
- **Colonnes visibles** : `Tâches Terminées`, `Temps Total`, `Résumé`.
- **Utilité** : Analyser les tendances sur un mois.

---

## 🔗 **Relations entre les Bases**

### **1. Master Board ↔ Routines**
- **Type de relation** : **Relation** (Notion).
- **Description** :
  - Chaque **routine** contient une liste de **tâches** (liens vers le Master Board).
  - Exemple : La routine "Matin" peut inclure les tâches "Café", "Étirements", "Vérifier emails".
- **Utilité** :
  - Permet de **réutiliser des tâches** dans plusieurs routines.
  - Facilite la **complétion en bloc** (ex: cocher toutes les tâches d’une routine).

---

### **2. Master Board ↔ Journal de Bord**
- **Type de relation** : **Automatique** (via scripts Mistral).
- **Description** :
  - Chaque jour, Mistral **scanne le Master Board** pour les tâches avec `Statut = Terminé` et `Date de Complétion = Aujourd’hui`.
  - Les données sont **agregées** dans une nouvelle entrée du Journal de Bord.
- **Utilité** :
  - **Historiser** les performances quotidiennes.
  - **Analyser** les tendances (ex: "Je suis plus productif le matin").

---

### **3. Master Board ↔ Google Calendar**
- **Type de relation** : **Synchronisation externe** (via Make.com ou scripts Python).
- **Description** :
  - **Calendar → Notion** : Un nouvel événement dans Calendar crée une tâche dans le Master Board.
  - **Notion → Calendar** : Optionnel (ex: créer un événement pour les tâches terminées).
- **Propriétés synchronisées** :
  - `Nom` ↔ Titre de l’événement.
  - `Durée` ↔ Durée de l’événement.
  - `Date Limite` ↔ Date/Heure de l’événement.
- **Utilité** :
  - **Éviter les doublons** entre les deux outils.
  - **Centraliser** la gestion du temps.

---

## 📋 **Exemples Concrets**

### **1. Exemple de Tâche dans le Master Board**
| Propriété          | Valeur                          |
|--------------------|---------------------------------|
| Nom                | Relancer client X               |
| Durée              | 30 min                          |
| Support            | Téléphone, PC Portable          |
| Pays/Lieu          | Global                          |
| Statut             | À déléguer à l’IA                |
| Priorité           | Urgent                          |
| Récurrence          | Unique                          |
| Contexte           | Admin, Client X                 |
| Heure de la journée| Après-midi                     |
| Date Limite        | 05/07/2026                      |
| Délégable à l’IA   | ✅ (coché)                       |
| Statut IA          | En attente                      |

---

### **2. Exemple de Routine "Matin"**
| Propriété          | Valeur                          |
|--------------------|---------------------------------|
| Nom                | Routine Matin                   |
| Type               | Matin                           |
| Éléments           | [Café, Étirements, Vérifier emails] |
| Ordre              | 1, 2, 3                         |
| Complétion         | ✅ (coché)                       |
| Dernière Complétion | 30/06/2026                   |

---

### **3. Exemple d’Entrée dans le Journal de Bord**
| Propriété          | Valeur                          |
|--------------------|---------------------------------|
| Date               | 30/06/2026                      |
| Résumé             | 8 tâches terminées (4h15). +20% vs hier. 3ème jour > 4h. |
| Tâches Terminées   | 8                               |
| Temps Total        | 255 (minutes)                   |
| Priorités          | Urgent: 2, Important: 4, Secondaire: 2 |
| Localisation       | Thaïlande                      |

---

## ✅ **Bonnes Pratiques**

### **1. Nommage des Propriétés**
- **Utiliser des emojis** pour une meilleure lisibilité (ex: `⏱️ Durée` au lieu de `Durée`).
- **Être cohérent** : Toujours utiliser les mêmes termes (ex: `Pays` et non `Localisation` dans une base et `Pays/Lieu` dans une autre).
- **Éviter les espaces** dans les noms de propriétés (utiliser `_` ou `-` si nécessaire).

---

### **2. Gestion des Sélections**
- **Limiter les options** : Ne pas avoir trop de valeurs pour une propriété `Sélection` (max 10-15).
- **Utiliser des couleurs** pour les priorités (ex: 🔴 Urgent, 🟡 Important, 🟢 Secondaire).
- **Ordonner les options** : Classer les valeurs par ordre logique (ex: `10 min`, `30 min`, `1h` pour la `Durée`).

---

### **3. Synchronisation avec Google Calendar**
- **Éviter les doublons** : Utiliser un **ID unique** (ex: `GCAL_{ID_EVENEMENT}`) dans Notion pour lier les entrées.
- **Synchroniser régulièrement** : Toutes les 15-30 min pour éviter les désynchronisations.
- **Gérer les conflits** : Privilégier Notion comme source de vérité (ex: si une tâche est modifiée dans Notion, mettre à jour Calendar).

---

### **4. Automatisation avec Mistral**
- **Utiliser des filtres précis** : Toujours inclure `Statut ≠ Terminé` pour éviter de traiter des tâches déjà terminées.
- **Journaliser les actions** : Conserver un historique des modifications (ex: qui a mis à jour une tâche ? Quand ?).
- **Gérer les erreurs** : Prévoir des mécanismes de replay en cas d’échec (ex: réessayer 3 fois avant d’abandonner).

---

### **5. Gamification**
- **Récompenser les petites tâches** : Attribuer des points même pour les tâches courtes (ex: 5 points pour 10 min, 10 points pour 30 min).
- **Visualiser les progrès** : Utiliser des graphiques (via Notion ou scripts Python) pour motiver.
- **Comparer avec soi-même** : Afficher des statistiques comme "+20% vs hier" plutôt que des comparaisons absolues.

---

## 📥 **Export/Import**

### **1. Exporter une Base Notion**
1. **Menu Notion** : Cliquez sur `•••` (en haut à droite de la base) → **Exporter**. 
2. **Format** : Choisissez **Markdown & CSV** ou **JSON** (pour une réimportation facile).
3. **Enregistrer** : Téléchargez le fichier.

---

### **2. Importer une Base Notion**
1. **Menu Notion** : Cliquez sur `+ Nouveau` → **Importer**. 
2. **Sélectionner le fichier** : Choisissez le fichier exporté (CSV, JSON, etc.).
3. **Configurer** : Mappez les colonnes si nécessaire.

---

### **3. Exemple de Fichier JSON pour le Master Board**
```json
{
  "properties": {
    "Nom": {
      "title": []
    },
    "⏱️ Durée": {
      "select": {
        "name": "30 min"
      }
    },
    "💻 Support": {
      "multi_select": [
        {"name": "Téléphone"},
        {"name": "PC Portable"}
      ]
    },
    "🌍 Pays/Lieu": {
      "select": {
        "name": "Thaïlande"
      }
    },
    "⚙️ Statut": {
      "status": {
        "name": "À déléguer à l’IA"
      }
    },
    "🎯 Priorité": {
      "select": {
        "name": "Urgent"
      }
    }
  }
}
```

---

### **4. Script Python pour Importer/Exporter**
```python
from notion_client import Client
import json

# Initialiser le client Notion
notion = Client(auth="TON_TOKEN_NOTION")

# Exporter une base de données
def export_database(database_id: str, output_file: str):
    response = notion.databases.query(database_id=database_id)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=4, ensure_ascii=False)
    print(f"Base exportée vers {output_file}")

# Importer des données dans une base
def import_data(database_id: str, data: list):
    for item in data:
        notion.pages.create(
            parent={"database_id": database_id},
            properties=item["properties"]
        )
    print("Données importées avec succès")

# Exemple d'utilisation
# export_database("ID_DE_LA_BASE", "master_board_export.json")
```

---

## 🔜 **Prochaines Étapes**

- [ ] **Valider la structure** avec les IA collaboratrices (Gemini, Mistral).
- [ ] **Créer un template Notion** avec les propriétés proposées.
- [ ] **Tester les vues** (Kanban, Tableau, Calendrier) avec des données fictives.
- [ ] **Automatiser la synchronisation** avec Google Calendar (Make.com ou Python).
- [ ] **Prototyper les scripts Mistral** pour le filtrage contextuel et la gamification.

---

> **Ressources Utiles** :
> - [Notion API Documentation](https://developers.notion.com/docs)
> - [Notion Templates](https://www.notion.so/templates)
> - [Guide des Propriétés Notion](https://www.notion.so/help/databases)
> - [Exemples de Bases Notion](https://www.notion.so/help/databases/examples)