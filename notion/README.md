# 📁 Dossier Notion : Templates et Exemples

> **Dossier** : `/notion`  
> **Rôle** : Centraliser les **templates Notion** (Master Board, Routines, Journal de Bord) et les exemples de données pour faciliter l’initialisation du projet.

---

## 📌 **Structure du Dossier**

```
notion/
├── templates/               # Templates JSON pour créer les bases Notion
│   ├── master_board.json    # Template pour le Master Board (tâches principales)
│   ├── routines.json         # Template pour les Routines (matin, soir, voyage)
│   └── journal_de_bord.json  # Template pour le Journal de Bord (stats quotidiennes)
├── examples/                # Exemples de données pour tester
│   ├── sample_tasks.json    # Exemple de tâches pour le Master Board
│   └── sample_routines.json  # Exemple de routines
└── README.md                # Ce fichier
```

---

## 🎯 **Templates Disponibles**

### **1. `master_board.json`**
- **Description** : Template pour la **base principale** du système, contenant toutes les tâches.
- **Propriétés incluses** :
  - `Nom`, `⏱️ Durée`, `💻 Support`, `🌍 Pays/Lieu`, `⚙️ Statut`, `🎯 Priorité`, `🔄 Récurrence` (obligatoires).
  - `📌 Contexte`, `🕒 Heure de la journée`, `🔗 Dépendances`, `📅 Date Limite`, `📝 Notes` (recommandées).
  - `🤖 Délégable à l’IA`, `📄 Livrable`, `🔄 Statut IA`, `📅 Date de Délégation` (automatisation).
  - `✅ Date de Complétion`, `⏱️ Temps Réel`, `🌟 Points` (gamification).
- **Vues incluses** :
  - Tableau (par défaut).
  - Kanban (par statut).
  - Calendrier (par date limite).
  - À Déléguer à l’IA (filtré).
  - Filtre Contextuel (pour les requêtes IA).

---

### **2. `routines.json`** *(À créer)*
- **Description** : Template pour la base **Routines**, contenant les checklists réutilisables (matin, soir, voyage, etc.).
- **Propriétés suggérées** :
  - `Nom` (Titre).
  - `Type` (Sélection : Matin, Soir, Voyage, Pré-départ, Post-arrivée).
  - `Éléments` (Relation vers le Master Board).
  - `Ordre` (Nombre).
  - `✅ Complétion` (Case à cocher).
  - `📅 Dernière Complétion` (Date).

---

### **3. `journal_de_bord.json`** *(À créer)*
- **Description** : Template pour la base **Journal de Bord**, archivant les résumés quotidiens.
- **Propriétés suggérées** :
  - `📅 Date` (Date).
  - `📝 Résumé` (Texte).
  - `📈 Tâches Terminées` (Nombre).
  - `⏱️ Temps Total` (Nombre, en minutes).
  - `🎯 Priorités` (Texte, ex: "Urgent: 2, Important: 3").
  - `🌍 Localisation` (Sélection : pays).

---

## 📥 **Comment Importer les Templates**

### **Méthode 1 : Via l’API Notion (Recommandé)**

#### **Prérequis**
- Un **token Notion API** (voir [.env.example](../.env.example)).
- L’ID d’une **page parente** (où créer la base).

#### **Étapes**
1. **Récupérer l’ID de la page parente** :
   - Créez une page Notion (ex: "Système de Productivité").
   - L’URL ressemblera à : `https://www.notion.so/workspace/8a7e49bc83854e99868ec2e7d3aa7424`
   - Copiez la partie **`8a7e49bc83854e99868ec2e7d3aa7424`** (avant le `?`).

2. **Utiliser le script Python** :
   ```python
   from notion_client import Client
   import json
   
   # Initialiser le client Notion
   notion = Client(auth="VOTRE_TOKEN_NOTION")
   
   # Charger le template
   with open("notion/templates/master_board.json", "r", encoding="utf-8") as f:
       template = json.load(f)
   
   # Remplacer l'ID de la page parente
   parent_page_id = "ID_DE_LA_PAGE_PARENTE"
   template["parent"] = {"type": "page_id", "page_id": parent_page_id}
   
   # Créer la base
   notion.databases.create(**template)
   print("✅ Base Master Board créée avec succès !")
   ```

---

### **Méthode 2 : Manuellement (Copier-Coller)**

1. **Créer une nouvelle base Notion** :
   - Cliquez sur **+ Nouveau** → **Base de données** → **Tableau** ou **Liste**.

2. **Ajouter les propriétés** :
   - Pour chaque propriété dans le template, ajoutez-la manuellement dans Notion.
   - Utilisez les **mêmes noms et types** que dans le JSON.
   - Pour les **Sélections**, ajoutez les mêmes **options** (ex: "Urgent", "Important" pour `Priorité`).

3. **Ajouter les vues** :
   - Cliquez sur **•••** → **Vues** → **Ajouter une vue**.
   - Configurez chaque vue selon le template (filtres, tri, colonnes visibles).

---

## 📤 **Comment Exporter une Base Existante**

Si vous avez déjà une base Notion et souhaitez la **sauvegarder** ou la **partager** :

### **Via l’Interface Notion**
1. Ouvrez votre base Notion.
2. Cliquez sur **•••** (en haut à droite) → **Exporter**.
3. Choisissez le format **JSON** ou **Markdown & CSV**.
4. Téléchargez le fichier et placez-le dans `/notion/templates/`.

### **Via l’API Notion**
```python
from notion_client import Client
import json

notion = Client(auth="VOTRE_TOKEN_NOTION")
database_id = "ID_DE_LA_BASE"

# Récupérer la structure de la base
response = notion.databases.retrieve(database_id=database_id)

# Enregistrer dans un fichier
with open("notion/templates/my_database.json", "w", encoding="utf-8") as f:
    json.dump(response, f, indent=4, ensure_ascii=False)

print("✅ Base exportée avec succès !")
```

---

## 📋 **Exemples de Données**

### **1. `sample_tasks.json`** *(À créer)*
Exemple de tâches pour peupler le **Master Board** :
```json
[
  {
    "Nom": "Relancer client X",
    "⏱️ Durée": "30 min",
    "💻 Support": ["Téléphone", "PC Portable"],
    "🌍 Pays/Lieu": "Global",
    "⚙️ Statut": "À déléguer à l’IA",
    "🎯 Priorité": "Urgent",
    "📌 Contexte": ["Admin", "Client X"],
    "📅 Date Limite": "2026-07-05"
  },
  {
    "Nom": "Révision Thai",
    "⏱️ Durée": "45 min",
    "💻 Support": ["PC Portable", "Téléphone"],
    "🌍 Pays/Lieu": "Thaïlande",
    "⚙️ Statut": "Pas commencé",
    "🎯 Priorité": "Important",
    "📌 Contexte": ["Apprentissage"],
    "🕒 Heure de la journée": "Soir"
  },
  {
    "Nom": "Analyser le rapport projet Cobra",
    "⏱️ Durée": "2h",
    "💻 Support": ["PC Portable", "PC Fixe"],
    "🌍 Pays/Lieu": "France",
    "⚙️ Statut": "En cours",
    "🎯 Priorité": "Important",
    "📌 Contexte": ["Projet Cobra", "Analyse"],
    "📅 Date Limite": "2026-07-10"
  }
]
```

---

### **2. `sample_routines.json`** *(À créer)*
Exemple de routines pour peupler la base **Routines** :
```json
[
  {
    "Nom": "Routine Matin",
    "Type": "Matin",
    "Éléments": [
      "Café",
      "Étirements (10 min)",
      "Vérifier emails urgents",
      "Planifier la journée (5 min)"
    ],
    "Ordre": [1, 2, 3, 4]
  },
  {
    "Nom": "Routine Voyage",
    "Type": "Voyage",
    "Éléments": [
      "Vérifier les réservations",
      "Préparer les documents",
      "Charger les appareils",
      "Contacter le client local"
    ],
    "Ordre": [1, 2, 3, 4]
  }
]
```

---

## 🔧 **Script pour Peupler une Base avec des Exemples**

Utilisez ce script pour ajouter des tâches d’exemple à votre **Master Board** :

```python
from notion_client import Client
import json

# Initialiser le client Notion
notion = Client(auth="VOTRE_TOKEN_NOTION")
database_id = "ID_DE_LA_BASE_MASTER_BOARD"

# Charger les exemples de tâches
with open("notion/examples/sample_tasks.json", "r", encoding="utf-8") as f:
    tasks = json.load(f)

# Ajouter chaque tâche à la base
for task in tasks:
    # Convertir les listes en format Notion (ex: ["Téléphone"] → [{"name": "Téléphone"}])
    properties = {}
    for key, value in task.items():
        if key == "Nom":
            properties[key] = {"title": [{"text": {"content": value}}]}
        elif key in ["⏱️ Durée", "🌍 Pays/Lieu", "⚙️ Statut", "🎯 Priorité", "🔄 Récurrence", "🕒 Heure de la journée"]:
            properties[key] = {"select": {"name": value}}
        elif key == "💻 Support":
            properties[key] = {"multi_select": [{"name": s} for s in value]}
        elif key == "📌 Contexte":
            properties[key] = {"rich_text": [{"text": {"content": c}} for c in value]}
        elif key == "📅 Date Limite":
            properties[key] = {"date": {"start": value}}
        elif key == "🔗 Dépendances":
            # Supposons que les dépendances sont des IDs de pages Notion
            properties[key] = {"relation": [{"id": d} for d in value]}
        else:
            properties[key] = {"rich_text": [{"text": {"content": str(value)}}]}
    
    notion.pages.create(
        parent={"database_id": database_id},
        properties=properties
    )
    print(f"✅ Tâche ajoutée: {task['Nom']}")

print("✅ Toutes les tâches d'exemple ont été ajoutées !")
```

---

## ✅ **Bonnes Pratiques**

1. **Adaptez les templates** : Modifiez les **options des Sélections** (ex: ajoutez des pays ou des priorités spécifiques à votre usage).
2. **Testez avec des données fictives** : Avant d’importer vos vraies tâches, testez avec des exemples.
3. **Sauvegardez régulièrement** : Exportez vos bases Notion pour éviter les pertes de données.
4. **Documentez vos modifications** : Si vous modifiez un template, notez les changements dans ce fichier.
5. **Utilisez des IDs uniques** : Pour les propriétés de type **Relation**, utilisez des IDs de pages Notion valides.

---

## 🚀 **Prochaines Étapes**

- [ ] **Créer `routines.json`** : Template pour la base Routines.
- [ ] **Créer `journal_de_bord.json`** : Template pour la base Journal de Bord.
- [ ] **Ajouter `sample_tasks.json`** : Exemples de tâches pour le Master Board.
- [ ] **Ajouter `sample_routines.json`** : Exemples de routines.
- [ ] **Tester l’import/export** avec des données réelles.

---

## 📚 **Ressources**
- [Notion API Documentation](https://developers.notion.com/docs)
- [Notion Databases Guide](https://www.notion.so/help/databases)
- [Notion Templates Gallery](https://www.notion.so/templates) (pour inspiration)
- [JSON Schema for Notion API](https://developers.notion.com/reference/database)

---

> **Besoin d’aide ?**
> - Consultez le [README principal](../README.md) pour une vue d’ensemble du projet.
> - Voir le [Guide des API](../docs/api_guide.md) pour des exemples de code.
> - Ouvrez une **Issue** sur GitHub pour poser une question.