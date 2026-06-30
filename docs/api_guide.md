# 🔌 Guide des API : Notion, Google Calendar, et Intégrations

> **Dernière mise à jour** : 30 juin 2026  
> **Statut** : En élaboration (À compléter avec les retours des IA)  
> **Repository** : [Sunnynio/Automatisation-Ultime](https://github.com/Sunnynio/Automatisation-Ultime)

---

## 📌 **Sommaire**
1. [Introduction](#-introduction)
2. [Notion API](#-notion-api)
3. [Google Calendar API](#-google-calendar-api)
4. [Google Gmail API](#-google-gmail-api)
5. [Mistral API](#-mistral-api)
6. [Make.com (Ex-Zapier)](#-makecom-ex-zapier)
7. [Exemples de Code](#-exemples-de-code)
8. [Bonnes Pratiques](#-bonnes-pratiques)
9. [Dépannage](#-dépannage)

---

## 🎯 **Introduction**

Ce guide détaille comment **interagir avec les API** nécessaires au projet **Système de Productivité Hybride**. Il couvre :
- **Notion API** : Pour manipuler les bases de données (Master Board, Routines, Journal de Bord).
- **Google Calendar API** : Pour synchroniser les événements avec Notion.
- **Google Gmail API** : Pour envoyer des notifications par email.
- **Mistral API** : Pour déléguer des tâches à l’IA.
- **Make.com** : Pour automatiser les workflows sans coder.

---

## 📝 **Notion API**

### **1. Prérequis**
- **Compte Notion** : Un compte payant (pour l’API).
- **Intégration Notion** : Créée via [Notion Developers](https://www.notion.so/my-integrations).
- **Token d’API** : `NOTION_TOKEN` (à stocker dans `.env`).
- **ID de la Base de Données** : `NOTION_DATABASE_ID` (voir [docs/notion_structure.md](../docs/notion_structure.md)).

---

### **2. Installation**
```bash
pip install notion-client
```

---

### **3. Authentification**
```python
from notion_client import Client
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

# Initialiser le client
notion = Client(auth=NOTION_TOKEN)
```

---

### **4. Opérations de Base**

#### **Lister les Bases de Données**
```python
# Lister toutes les bases accessibles par l'intégration
response = notion.search(filter={"property": "object", "value": "database"})
for db in response["results"]:
    print(f"Base: {db['title'][0]['plain_text']} (ID: {db['id']})")
```

---

#### **Lister les Tâches d’une Base**
```python
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Récupérer toutes les tâches
response = notion.databases.query(database_id=DATABASE_ID)
for task in response["results"]:
    print(f"Tâche: {task['properties']['Nom']['title'][0]['plain_text']}")
```

---

#### **Filtrer les Tâches**
```python
# Filtrer les tâches en Thaïlande, sur téléphone, durée ≤ 30 min
response = notion.databases.query(
    database_id=DATABASE_ID,
    filter={
        "and": [
            {"property": "🌍 Pays/Lieu", "select": {"equals": "Thaïlande"}},
            {"property": "💻 Support", "multi_select": {"contains": "Téléphone"}},
            {"property": "⏱️ Durée", "select": {"equals": "30 min"}},
            {"property": "⚙️ Statut", "status": {"is_not": "Terminé"}}
        ]
    }
)
for task in response["results"]:
    print(f"Tâche: {task['properties']['Nom']['title'][0]['plain_text']}")
```

---

#### **Créer une Tâche**
```python
new_task = {
    "Nom": {
        "title": [{"text": {"content": "Nouvelle tâche test"}}]
    },
    "⏱️ Durée": {
        "select": {"name": "30 min"}
    },
    "💻 Support": {
        "multi_select": [{"name": "Téléphone"}, {"name": "PC Portable"}]
    },
    "🌍 Pays/Lieu": {
        "select": {"name": "Thaïlande"}
    },
    "⚙️ Statut": {
        "status": {"name": "Pas commencé"}
    }
}

notion.pages.create(
    parent={"database_id": DATABASE_ID},
    properties=new_task
)
print("Tâche créée avec succès")
```

---

#### **Mettre à Jour une Tâche**
```python
PAGE_ID = "ID_DE_LA_PAGE"  # Récupéré depuis une requête précédente

updated_properties = {
    "⚙️ Statut": {
        "status": {"name": "En cours"}
    }
}

notion.pages.update(
    page_id=PAGE_ID,
    properties=updated_properties
)
print("Tâche mise à jour")
```

---

#### **Supprimer une Tâche**
```python
PAGE_ID = "ID_DE_LA_PAGE"

notion.pages.update(
    page_id=PAGE_ID,
    archived=True  # Archive la page (ne la supprime pas définitivement)
)
print("Tâche archivée")
```

---

### **5. Gérer les Relations**

#### **Lier une Tâche à une Routine**
```python
# Supposons que ROUTINE_ID est l'ID d'une page dans la base "Routines"
ROUTINE_ID = "ID_DE_LA_ROUTINE"

# Ajouter une relation à une tâche existante
notion.pages.update(
    page_id=PAGE_ID,
    properties={
        "🔗 Dépendances": {
            "relation": [{"id": ROUTINE_ID}]
        }
    }
)
```

---

### **6. Récupérer les Pages Liées**
```python
# Récupérer les tâches liées à une routine
response = notion.databases.query(
    database_id=DATABASE_ID,
    filter={
        "property": "🔗 Dépendances",
        "relation": [{"id": ROUTINE_ID}]
    }
)
for task in response["results"]:
    print(f"Tâche liée: {task['properties']['Nom']['title'][0]['plain_text']}")
```

---

### **7. Pagination**
```python
# Récupérer toutes les pages (avec pagination)
all_results = []
start_cursor = None

while True:
    response = notion.databases.query(
        database_id=DATABASE_ID,
        start_cursor=start_cursor,
        page_size=100  # Max 100 par requête
    )
    all_results.extend(response["results"])
    start_cursor = response.get("next_cursor")
    if not start_cursor:
        break

print(f"Total tâches: {len(all_results)}")
```

---

### **8. Documentation Officielle**
- [Notion API Reference](https://developers.notion.com/reference)
- [Notion SDK Python](https://github.com/ramnes/notion-sdk-py)
- [Exemples Notion API](https://developers.notion.com/docs/working-with-the-api)

---

## 📅 **Google Calendar API**

### **1. Prérequis**
- **Projet Google Cloud** : Créé via [Google Cloud Console](https://console.cloud.google.com/).
- **API Activée** : **Google Calendar API** (et éventuellement **Gmail API**).
- **Identifiants OAuth 2.0** : `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` (voir [.env.example](../.env.example)).
- **Token de Rafraîchissement** : `GOOGLE_REFRESH_TOKEN` (généré via un script d’authentification).

---

### **2. Installation**
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

### **3. Authentification**
```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Charger les variables d'environnement
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Authentification (si pas de token valide)
def get_credentials():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    
    return creds

credentials = get_credentials()
```

---

### **4. Opérations de Base**

#### **Lister les Calendriers**
```python
from googleapiclient.discovery import build

service = build("calendar", "v3", credentials=credentials)

# Lister tous les calendriers accessibles
calendar_list = service.calendarList().list().execute()
for calendar in calendar_list.get("items", []):
    print(f"Calendrier: {calendar['summary']} (ID: {calendar['id']})")
```

---

#### **Lister les Événements d’un Calendrier**
```python
CALENDAR_ID = "primary"  # ou l'ID d'un calendrier spécifique

# Récupérer les événements pour aujourd'hui
now = datetime.datetime.utcnow().isoformat() + "Z"
end_of_day = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z"

events_result = service.events().list(
    calendarId=CALENDAR_ID,
    timeMin=now,
    timeMax=end_of_day,
    singleEvents=True,
    orderBy="startTime"
).execute()

for event in events_result.get("items", []):
    print(f"Événement: {event['summary']} ({event['start'].get('dateTime', event['start'].get('date'))})")
```

---

#### **Créer un Événement**
```python
new_event = {
    "summary": "Réunion avec Client X",
    "start": {
        "dateTime": "2026-07-01T14:00:00+07:00",  # UTC+7 (Thaïlande)
        "timeZone": "Asia/Bangkok"
    },
    "end": {
        "dateTime": "2026-07-01T15:00:00+07:00",
        "timeZone": "Asia/Bangkok"
    },
    "description": "Discuter du projet Cobra"
}

created_event = service.events().insert(
    calendarId=CALENDAR_ID,
    body=new_event
).execute()
print(f"Événement créé: {created_event.get('htmlLink')}")
```

---

#### **Mettre à Jour un Événement**
```python
EVENT_ID = "ID_DE_L_EVENEMENT"

updated_event = {
    "summary": "Réunion avec Client X (Reportée)",
    "start": {
        "dateTime": "2026-07-02T14:00:00+07:00",
        "timeZone": "Asia/Bangkok"
    }
}

service.events().update(
    calendarId=CALENDAR_ID,
    eventId=EVENT_ID,
    body=updated_event
).execute()
print("Événement mis à jour")
```

---

#### **Supprimer un Événement**
```python
EVENT_ID = "ID_DE_L_EVENEMENT"

service.events().delete(
    calendarId=CALENDAR_ID,
    eventId=EVENT_ID
).execute()
print("Événement supprimé")
```

---

### **5. Synchronisation avec Notion**

#### **Exemple : Créer une Tâche Notion depuis un Événement Calendar**
```python
# Récupérer les événements Calendar
events = service.events().list(calendarId=CALENDAR_ID, maxResults=10).execute().get("items", [])

for event in events:
    # Créer une tâche Notion correspondante
    new_task = {
        "Nom": {"title": [{"text": {"content": event["summary"]}}]},
        "⏱️ Durée": {"select": {"name": "1h"}},  # À adapter selon la durée de l'événement
        "📅 Date Limite": {"date": {"start": event["start"].get("date", event["start"].get("dateTime"))}},
        "⚙️ Statut": {"status": {"name": "À planifier"}},
        "📌 Contexte": {"rich_text": [{"text": {"content": event.get("description", "")}}]}
    }
    
    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties=new_task
    )
```

---

### **6. Documentation Officielle**
- [Google Calendar API Reference](https://developers.google.com/calendar/api/v3/reference)
- [Google Calendar API Guide](https://developers.google.com/calendar/api/guides)
- [Python Quickstart](https://developers.google.com/calendar/api/quickstart/python)

---

## 📧 **Google Gmail API**

### **1. Prérequis**
- **API Activée** : **Gmail API** dans Google Cloud Console.
- **Scopes** : Ajoutez `https://www.googleapis.com/auth/gmail.send` à vos scopes OAuth.
- **Token de Rafraîchissement** : Même processus que pour Calendar API.

---

### **2. Installation**
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

### **3. Authentification**
Utilisez le même script que pour Calendar API, mais avec les scopes Gmail :
```python
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
```

---

### **4. Envoyer un Email**
```python
from googleapiclient.discovery import build
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

service = build("gmail", "v1", credentials=credentials)

# Créer le message
message = MIMEMultipart()
message["to"] = "destinataire@example.com"
message["from"] = os.getenv("GMAIL_SENDER_EMAIL")
message["subject"] = "Résumé quotidien de productivité"

# Corps de l'email (en Markdown ou HTML)
body = """
📅 **30/06/2026**
✅ **8 tâches terminées** (Temps : 4h15)
📈 **+20% vs hier** | 🏆 **3ème jour consécutif > 4h**
"""
message.attach(MIMEText(body, "html"))

# Encoder le message
raw_message = urlsafe_b64encode(message.as_bytes()).decode("utf-8")

# Envoyer l'email
sent_message = service.users().messages().send(
    userId="me",
    body={"raw": raw_message}
).execute()
print(f"Email envoyé (ID: {sent_message['id']})")
```

---

### **5. Lire les Emails**
```python
# Lister les 10 derniers emails
results = service.users().messages().list(userId="me", maxResults=10).execute()
messages = results.get("messages", [])

for message in messages:
    msg = service.users().messages().get(userId="me", id=message["id"]).execute()
    print(f"De: {msg['payload']['headers'][15]['value']}")  # Adaptez l'index selon la structure
    print(f"Sujet: {msg['payload']['headers'][17]['value']}")
```

---

### **6. Documentation Officielle**
- [Gmail API Reference](https://developers.google.com/gmail/api/reference)
- [Gmail API Guide](https://developers.google.com/gmail/api/guides)
- [Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)

---

## 🤖 **Mistral API**

### **1. Prérequis**
- **Clé API** : `MISTRAL_API_KEY` (à obtenir sur [Mistral AI](https://mistral.ai/)).
- **Bibliothèque** : `requests` pour les appels HTTP.

---

### **2. Installation**
```bash
pip install requests
```

---

### **3. Authentification**
```python
import os
from dotenv import load_dotenv

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

headers = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}
```

---

### **4. Envoyer une Requête à Mistral**
```python
import requests

url = "https://api.mistral.ai/v1/chat/completions"

payload = {
    "model": "mistral-medium",
    "messages": [
        {
            "role": "user",
            "content": "Quelles sont les 3 tâches les plus urgentes dans ma base Notion pour aujourd'hui ?"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 1000
}

response = requests.post(url, headers=headers, json=payload)
print(response.json()["choices"][0]["message"]["content"])
```

---

### **5. Intégration avec Notion**
**Exemple : Déléguer une Tâche à Mistral**
```python
# 1. Récupérer les tâches "À déléguer à l'IA" depuis Notion
tasks = notion.databases.query(
    database_id=DATABASE_ID,
    filter={
        "property": "⚙️ Statut",
        "status": {"equals": "À déléguer à l'IA"}
    }
).get("results", [])

# 2. Pour chaque tâche, demander à Mistral de l'exécuter
for task in tasks:
    task_name = task["properties"]["Nom"]["title"][0]["plain_text"]
    task_context = task["properties"]["📌 Contexte"]["rich_text"][0]["plain_text"]
    
    payload = {
        "model": "mistral-medium",
        "messages": [
            {
                "role": "user",
                "content": f"Exécute la tâche suivante : {task_name}. Contexte : {task_context}. Prépare un brouillon ou un livrable."
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()["choices"][0]["message"]["content"]
    
    # 3. Mettre à jour Notion avec le résultat
    notion.pages.update(
        page_id=task["id"],
        properties={
            "🤖 Statut IA": {"select": {"name": "Terminée"}},
            "📄 Livrable": {"url": result}  # ou un lien vers un Google Doc
        }
    )
```

---

### **6. Documentation Officielle**
- [Mistral API Documentation](https://docs.mistral.ai/)
- [Mistral API Reference](https://docs.mistral.ai/api/)

---

## 🔗 **Make.com (Ex-Zapier)**

### **1. Introduction**
**Make.com** est un outil d’automatisation **no-code** qui permet de connecter Notion, Google Calendar, Gmail, et d’autres services **sans écrire de code**.

---

### **2. Cas d’Usage pour le Projet**

#### **A. Synchronisation Calendar ↔ Notion**
**Scénario** : "Quand un nouvel événement est créé dans Google Calendar, créer une tâche dans Notion."

**Étapes** :
1. **Déclencheur** : Google Calendar → "Nouvel événement créé".
2. **Action** : Notion → "Créer une page dans la base Master Board".
3. **Mapping** :
   - `Summary` (Calendar) → `Nom` (Notion).
   - `Start Time` (Calendar) → `Date Limite` (Notion).
   - `Duration` (Calendar) → `⏱️ Durée` (Notion).

---

#### **B. Notification pour les Tâches "À Déléguer à l’IA"**
**Scénario** : "Quand une tâche est marquée comme 'À déléguer à l’IA' dans Notion, envoyer une notification à Mistral."

**Étapes** :
1. **Déclencheur** : Notion → "Page mise à jour" (filtre : `Statut = À déléguer à l’IA`).
2. **Action** : Webhook → "Envoyer une requête HTTP à Mistral API".
3. **Payload** :
   ```json
   {
     "task_id": "{{ID de la page Notion}}",
     "task_name": "{{Nom de la tâche}}",
     "context": "{{Contexte}}"
   }
   ```

---

#### **C. Génération de Résumé Quotidien**
**Scénario** : "Tous les soirs à 20h, générer un résumé des tâches terminées et l’envoyer par email."

**Étapes** :
1. **Déclencheur** : Schedule → "Tous les jours à 20h (UTC+7)".
2. **Action 1** : Notion → "Lister les pages avec Statut = Terminé et Date de Complétion = Aujourd’hui".
3. **Action 2** : Gmail → "Envoyer un email avec le résumé".

---

### **3. Avantages/Inconvénients**

| **Critère**          | **Make.com**                          | **Script Python**                     |
|----------------------|---------------------------------------|---------------------------------------|
| **Facilité**         | ⭐⭐⭐⭐⭐ (No-code)                     | ⭐⭐ (Code requis)                     |
| **Flexibilité**      | ⭐⭐⭐ (Limité aux connecteurs disponibles) | ⭐⭐⭐⭐⭐ (Tout est possible)       |
| **Coût**            | Payant (à partir de ~$9/mois)          | Gratuit (si hébergement local)        |
| **Maintenance**      | ⭐⭐⭐ (Interface visuelle)              | ⭐⭐⭐⭐ (Code à maintenir)               |
| **Performances**     | ⭐⭐⭐ (Délai de quelques secondes)      | ⭐⭐⭐⭐⭐ (Instantané)                  |

---

### **4. Lien Utile**
- [Make.com Documentation](https://www.make.com/en/help)
- [Make.com Templates](https://www.make.com/en/integrations)

---

## 💻 **Exemples de Code**

### **1. Script Complet : Filtre Contextuel**
```python
from notion_client import Client
import os
from dotenv import load_dotenv

# Charger les variables
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Initialiser Notion
notion = Client(auth=NOTION_TOKEN)

# Filtrer les tâches selon le contexte
def filter_tasks(pays: str, supports: list, duree_max: str):
    response = notion.databases.query(
        database_id=DATABASE_ID,
        filter={
            "and": [
                {"property": "🌍 Pays/Lieu", "select": {"equals": pays}},
                {"property": "💻 Support", "multi_select": {"contains": supports[0]}},
                {"property": "⏱️ Durée", "select": {"equals": duree_max}},
                {"property": "⚙️ Statut", "status": {"is_not": "Terminé"}}
            ]
        },
        sorts=[
            {"property": "🎯 Priorité", "direction": "descending"},
            {"property": "⏱️ Durée", "direction": "ascending"}
        ]
    )
    return response["results"]

# Exemple d'utilisation
tasks = filter_tasks("Thaïlande", ["Téléphone"], "30 min")
for task in tasks[:3]:  # Top 3 tâches
    print(f"- {task['properties']['Nom']['title'][0]['plain_text']} ({task['properties']['⏱️ Durée']['select']['name']})")
```

---

### **2. Script Complet : Synchronisation Calendar ↔ Notion**
```python
from googleapiclient.discovery import build
from notion_client import Client
from google.oauth2.credentials import Credentials
import os
from dotenv import load_dotenv

# Charger les variables
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS_PATH")  # Chemin vers credentials.json

# Initialiser les clients
notion = Client(auth=NOTION_TOKEN)
service = build("calendar", "v3", credentials=Credentials.from_authorized_user_file(GOOGLE_CREDENTIALS))

# Synchroniser Calendar → Notion
def sync_calendar_to_notion(calendar_id="primary"):
    events = service.events().list(
        calendarId=calendar_id,
        maxResults=10,
        singleEvents=True
    ).execute().get("items", [])
    
    for event in events:
        # Vérifier si l'événement existe déjà dans Notion (via un ID unique)
        existing_tasks = notion.databases.query(
            database_id=DATABASE_ID,
            filter={
                "property": "📅 Date Limite",
                "date": {"equals": event["start"].get("date", event["start"].get("dateTime"))}
            }
        ).get("results", [])
        
        if not existing_tasks:
            new_task = {
                "Nom": {"title": [{"text": {"content": event["summary"]}}]},
                "⏱️ Durée": {"select": {"name": "1h"}},  # À adapter
                "📅 Date Limite": {"date": {"start": event["start"].get("date", event["start"].get("dateTime"))}},
                "⚙️ Statut": {"status": {"name": "À planifier"}},
                "📌 Contexte": {"rich_text": [{"text": {"content": event.get("description", "")}}]}
            }
            notion.pages.create(parent={"database_id": DATABASE_ID}, properties=new_task)
            print(f"Tâche créée: {event['summary']}")

sync_calendar_to_notion()
```

---

### **3. Script Complet : Génération de Résumé Quotidien**
```python
from notion_client import Client
import os
from dotenv import load_dotenv
from datetime import datetime

# Charger les variables
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
JOURNAL_DATABASE_ID = os.getenv("JOURNAL_DATABASE_ID")  # ID de la base Journal de Bord

# Initialiser Notion
notion = Client(auth=NOTION_TOKEN)

# Générer le résumé quotidien
def generate_daily_summary():
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Récupérer les tâches terminées aujourd'hui
    completed_tasks = notion.databases.query(
        database_id=DATABASE_ID,
        filter={
            "and": [
                {"property": "⚙️ Statut", "status": {"equals": "Terminé"}},
                {"property": "✅ Date de Complétion", "date": {"equals": today}}
            ]
        }
    ).get("results", [])
    
    # Calculer les statistiques
    total_tasks = len(completed_tasks)
    total_time = sum(
        int(task["properties"]["⏱️ Durée"]["select"]["name"].replace(" min", "").replace("h", "0")) 
        for task in completed_tasks
    ) if completed_tasks else 0
    
    # Créer une entrée dans le Journal de Bord
    summary = f"{total_tasks} tâches terminées (Temps : {total_time} min)"
    
    new_entry = {
        "📅 Date": {"date": {"start": today}},
        "📝 Résumé": {"rich_text": [{"text": {"content": summary}}]},
        "📈 Tâches Terminées": {"number": total_tasks},
        "⏱️ Temps Total": {"number": total_time}
    }
    
    notion.pages.create(
        parent={"database_id": JOURNAL_DATABASE_ID},
        properties=new_entry
    )
    print(f"Résumé quotidien généré: {summary}")

generate_daily_summary()
```

---

## ✅ **Bonnes Pratiques**

### **1. Gestion des Tokens API**
- **Ne jamais commiter** : Utilisez `.gitignore` pour exclure `.env` et les fichiers de credentials.
- **Variables d’environnement** : Toujours charger les tokens depuis `.env` ou des secrets (ex: GitHub Secrets).
- **Rotation** : Changez vos tokens tous les **3-6 mois**.

---

### **2. Optimisation des Appels API**
- **Cache** : Stockez les résultats des appels API fréquents (ex: liste des tâches) pour éviter de les refaire.
- **Pagination** : Utilisez la pagination pour éviter de surcharger les API (Notion limite à 100 résultats par requête).
- **Rate Limiting** : Respectez les limites des API (ex: Notion permet 3 requêtes/seconde).

---

### **3. Gestion des Erreurs**
- **Try/Except** : Toujours encapsuler les appels API dans des blocs `try/except`.
- **Logs** : Journalisez les erreurs pour le débogage.
- **Retry** : Implémentez une logique de réessai pour les erreurs temporaires.

**Exemple** :
```python
import time
from notion_client import APIError

max_retries = 3
retry_delay = 5  # secondes

for attempt in range(max_retries):
    try:
        response = notion.databases.query(database_id=DATABASE_ID)
        break
    except APIError as e:
        print(f"Erreur (attempt {attempt + 1}): {e}")
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            print("Échec après 3 tentatives")
```

---

### **4. Sécurité**
- **Scopes minimaux** : Donnez uniquement les permissions nécessaires (ex: Notion en lecture seule si possible).
- **Chiffrement** : Pour les projets sensibles, chiffrez les tokens avec des outils comme `git-secret`.
- **Audit** : Vérifiez régulièrement les **logs d’accès** aux API (ex: Google Cloud Console pour Gmail/Calendar).

---

### **5. Tests**
- **Données fictives** : Testez toujours avec des données fictives avant de passer en production.
- **Mocking** : Utilisez des bibliothèques comme `unittest.mock` pour simuler les appels API.
- **Validation** : Vérifiez que les données synchronisées (ex: Calendar ↔ Notion) sont cohérentes.

---

## 🚨 **Dépannage**

### **1. Erreurs Courantes avec Notion API**
| **Erreur**                          | **Cause**                                  | **Solution**                                                                 |
|-------------------------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| `APIError: Invalid token`           | Token Notion invalide ou expiré.          | Régénérez le token dans [Notion Developers](https://www.notion.so/my-integrations). |
| `APIError: Database not found`      | ID de base de données incorrect.           | Vérifiez l’ID dans l’URL de la base Notion.                                |
| `APIError: Property not found`      | Propriété mal orthographiée.              | Vérifiez le nom exact de la propriété dans Notion.                        |
| `Rate limit exceeded`                | Trop de requêtes en peu de temps.         | Ajoutez un délai entre les requêtes (`time.sleep(1)`).                    |

---

### **2. Erreurs Courantes avec Google API**
| **Erreur**                          | **Cause**                                  | **Solution**                                                                 |
|-------------------------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| `Invalid Credentials`               | Token Google expiré ou invalide.           | Régénérez le `refresh_token` avec le script d’authentification.             |
| `Insufficient Permission`           | Scopes OAuth manquants.                   | Ajoutez les scopes nécessaires (ex: `https://www.googleapis.com/auth/calendar`). |
| `Quota Exceeded`                    | Quota API dépassé.                         | Vérifiez vos quotas dans [Google Cloud Console](https://console.cloud.google.com/). |

---

### **3. Erreurs Courantes avec Mistral API**
| **Erreur**                          | **Cause**                                  | **Solution**                                                                 |
|-------------------------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| `Invalid API Key`                   | Clé API Mistral invalide.                 | Vérifiez votre clé dans [Mistral AI](https://mistral.ai/).                |
| `Rate Limit Exceeded`               | Trop de requêtes à Mistral.                | Attendez quelques secondes avant de réessayer.                            |
| `Model Not Found`                   | Modèle non disponible (ex: `mistral-medium`). | Vérifiez les modèles disponibles dans la [documentation Mistral](https://docs.mistral.ai/). |

---

### **4. Outils de Débogage**
- **Notion API** : Utilisez [Postman](https://www.postman.com/) pour tester les requêtes.
- **Google API** : Activez les **logs** dans [Google Cloud Console](https://console.cloud.google.com/).
- **Mistral API** : Utilisez `curl` pour tester les requêtes :
  ```bash
  curl -X POST "https://api.mistral.ai/v1/chat/completions" \
    -H "Authorization: Bearer VOTRE_CLE_API" \
    -H "Content-Type: application/json" \
    -d '{"model": "mistral-medium", "messages": [{"role": "user", "content": "Test"}]}'
  ```

---

## 📚 **Ressources Complémentaires**
- [Notion API Playground](https://developers.notion.com/docs/working-with-the-api)
- [Google API Explorer](https://developers.google.com/calendar/api/v3/reference/rest)
- [Mistral API Playground](https://console.mistral.ai/)
- [Make.com Community](https://www.make.com/en/community)

---

> **Prochaine Étape** :
> - [ ] Tester les exemples de code avec des **données réelles** (Notion, Calendar).
> - [ ] Configurer **Make.com** pour les workflows no-code.
> - [ ] Automatiser la **génération de résumés quotidiens** avec Mistral.
> - [ ] Documenter les **cas d’erreur spécifiques** rencontrés.