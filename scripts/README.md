# 📁 Scripts Python pour l'Automatisation

> **Dernière mise à jour** : 30 juin 2026  
> **Statut** : En élaboration (Exemples de base pour démarrer)  
> **Repository** : [Sunnynio/Automatisation-Ultime](https://github.com/Sunnynio/Automatisation-Ultime)

---

## 📌 **Sommaire**
1. [Introduction](#-introduction)
2. [Prérequis](#-prérequis)
3. [Structure du Dossier `/scripts`](#-structure-du-dossier-scripts)
4. [Configuration de Base](#-configuration-de-base)
5. [Exemples de Scripts](#-exemples-de-scripts)
6. [Bonnes Pratiques](#-bonnes-pratiques)
7. [Comment Contribuer](#-comment-contribuer)

---

## 🎯 **Introduction**

Ce dossier contient tous les **scripts Python** nécessaires pour automatiser les workflows du **Système de Productivité Hybride**. Les scripts couvrent :
- L’interaction avec **Notion API** (lecture/écriture de tâches).
- La synchronisation avec **Google Calendar API**.
- L’envoi de notifications via **Gmail API**.
- L’exécution de tâches par **Mistral API**.
- Les utilitaires (filtrage, tri, génération de résumés).

---

## 📦 **Prérequis**

### **1. Python 3.8+**
Vérifiez votre version de Python :
```bash
python --version
```
Si nécessaire, mettez à jour Python : [python.org](https://www.python.org/downloads/).

---

### **2. Bibliothèques Requises**
Installez les dépendances avec `pip` :
```bash
pip install notion-client google-api-python-client google-auth-httplib2 google-auth-oauthlib requests python-dotenv pandas matplotlib
```

---

### **3. Variables d’Environnement**
Créez un fichier `.env` à la racine du projet avec vos tokens API (voir [.env.example](../.env.example)) :
```env
# Notion
NOTION_TOKEN=secret_abc123xyz456
NOTION_DATABASE_ID=8a7e49bc83854e99868ec2e7d3aa7424

# Google
GOOGLE_CLIENT_ID=1234567890-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz
GOOGLE_REFRESH_TOKEN=1//04xABCDEFGHIJKLMNOPQRSTUVWXYZ
GMAIL_SENDER_EMAIL=franck.savin@example.com

# Mistral (optionnel)
MISTRAL_API_KEY=mistral_abc123xyz456

# Configuration locale
DATA_DIR=./data
TIMEZONE=Asia/Bangkok
```

---

## 🗂️ **Structure du Dossier `/scripts`**

```
scripts/
├── notion_api/           # Scripts liés à Notion API
│   ├── fetch_tasks.py    # Récupérer des tâches avec des filtres
│   ├── update_task.py    # Mettre à jour une tâche (statut, propriétés)
│   ├── create_task.py    # Créer une nouvelle tâche
│   └── sync_notion.py    # Synchronisation avec d'autres outils
│
├── google_api/           # Scripts liés à Google API (Calendar, Gmail)
│   ├── sync_calendar.py  # Synchroniser Calendar ↔ Notion
│   ├── send_email.py     # Envoyer un email via Gmail API
│   └── get_events.py     # Récupérer les événements Calendar
│
├── automation/           # Scripts d'automatisation (Mistral)
│   ├── context_filter.py  # Filtre contextuel (temps, support, lieu)
│   ├── daily_summary.py  # Générer un résumé quotidien
│   ├── delegate_task.py   # Exécuter une tâche "À déléguer à l’IA"
│   └── routines.py       # Gérer les routines (matin, soir, voyage)
│
├── utils/                # Fonctions utilitaires
│   ├── config.py         # Configuration centrale (chargement des variables)
│   ├── helpers.py        # Fonctions réutilisables (filtrage, tri, etc.)
│   └── logger.py         # Journalisation des actions
│
└── examples/            # Exemples d'utilisation
    ├── demo_filter.py    # Démonstration du filtre contextuel
    └── demo_sync.py      # Démonstration de la synchronisation Calendar ↔ Notion
```

---

## ⚙️ **Configuration de Base**

### **1. `scripts/utils/config.py`**
Fichier de configuration centrale pour charger les variables d’environnement et initialiser les clients API.

```python
import os
from dotenv import load_dotenv
from notion_client import Client
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Charger les variables d'environnement
load_dotenv()

# Notion
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Google
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")
GMAIL_SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL")

# Mistral
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Configuration locale
DATA_DIR = os.getenv("DATA_DIR", "./data")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Bangkok")

# Initialiser le client Notion
def get_notion_client():
    if not NOTION_TOKEN:
        raise ValueError("NOTION_TOKEN non défini dans .env")
    return Client(auth=NOTION_TOKEN)

# Initialiser le client Google Calendar
def get_google_calendar_service():
    creds = Credentials(
        token=None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build("calendar", "v3", credentials=creds)

# Initialiser le client Gmail
def get_gmail_service():
    creds = Credentials(
        token=None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build("gmail", "v1", credentials=creds)
```

---

### **2. `scripts/utils/helpers.py`**
Fonctions utilitaires pour le filtrage, le tri, et la manipulation des données.

```python
from datetime import datetime, timedelta
import pytz

# Récupérer la date/heure actuelle dans le fuseau horaire configuré
def get_current_time():
    tz = pytz.timezone(os.getenv("TIMEZONE", "Asia/Bangkok"))
    return datetime.now(tz)

# Convertir une durée en minutes (ex: "30 min" → 30, "1h" → 60)
def duration_to_minutes(duration_str: str) -> int:
    duration_map = {
        "10 min": 10,
        "30 min": 30,
        "1h": 60,
        "1h30": 90,
        "2h": 120,
        "Demi-journée": 240,
        "1 jour": 480,
        "2 jours": 960,
        "2 jours +": 1440
    }
    return duration_map.get(duration_str, 0)

# Filtrer les tâches Notion selon un contexte
def filter_tasks_by_context(tasks: list, context: dict) -> list:
    """
    Filtre une liste de tâches Notion selon un contexte donné.
    
    Args:
        tasks: Liste de tâches Notion (format API).
        context: Dictionnaire avec les clés :
            - pays (str): Pays/Lieu
            - supports (list): Liste de supports (ex: ["Téléphone", "PC Portable"])
            - max_duration (str): Durée maximale (ex: "30 min")
            - min_priority (str): Priorité minimale (ex: "Important")
            - status (str): Statut à exclure (ex: "Terminé")
    
    Returns:
        Liste de tâches filtrées.
    """
    filtered_tasks = []
    max_duration_min = duration_to_minutes(context.get("max_duration", "1 jour +"))
    
    for task in tasks:
        props = task["properties"]
        
        # Filtrer par Pays/Lieu
        if context.get("pays"):
            country = props.get("🌍 Pays/Lieu", {}).get("select", {}).get("name", "Global")
            if country != context["pays"] and country != "Global":
                continue
        
        # Filtrer par Support
        if context.get("supports"):
            task_supports = props.get("💻 Support", {}).get("multi_select", [])
            task_supports = [s["name"] for s in task_supports]
            if not any(support in task_supports for support in context["supports"]):
                continue
        
        # Filtrer par Durée
        task_duration = props.get("⏱️ Durée", {}).get("select", {}).get("name", "1 jour +")
        if duration_to_minutes(task_duration) > max_duration_min:
            continue
        
        # Filtrer par Statut
        if context.get("status"):
            task_status = props.get("⚙️ Statut", {}).get("status", {}).get("name", "Pas commencé")
            if task_status == context["status"]:
                continue
        
        # Filtrer par Priorité
        if context.get("min_priority"):
            priority_order = {"Urgent": 4, "Important": 3, "Secondaire": 2, "Optionnel": 1, "Sans priorité": 0}
            task_priority = props.get("🎯 Priorité", {}).get("select", {}).get("name", "Sans priorité")
            min_priority = context["min_priority"]
            if priority_order.get(task_priority, 0) < priority_order.get(min_priority, 0):
                continue
        
        filtered_tasks.append(task)
    
    return filtered_tasks

# Trier les tâches par priorité puis par durée
def sort_tasks_by_priority_and_duration(tasks: list) -> list:
    priority_order = {"Urgent": 4, "Important": 3, "Secondaire": 2, "Optionnel": 1, "Sans priorité": 0}
    
    def get_sort_key(task):
        props = task["properties"]
        priority = props.get("🎯 Priorité", {}).get("select", {}).get("name", "Sans priorité")
        duration = props.get("⏱️ Durée", {}).get("select", {}).get("name", "1 jour +")
        return (-priority_order.get(priority, 0), duration_to_minutes(duration))
    
    return sorted(tasks, key=get_sort_key)
```

---

### **3. `scripts/utils/logger.py`**
Module pour journaliser les actions (utile pour le débogage et l’audit).

```python
import logging
from datetime import datetime
import os

# Configurer le logger
def setup_logger(name: str = "automatisation_ultime", log_file: str = "automatisation.log") -> logging.Logger:
    """Configure un logger pour le projet."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Handler pour la console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler pour le fichier (si DATA_DIR existe)
    if os.path.exists(os.getenv("DATA_DIR", "./data")):
        file_handler = logging.FileHandler(os.path.join(os.getenv("DATA_DIR", "./data"), log_file))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Logger global
logger = setup_logger()
```

---

## 📜 **Exemples de Scripts**

### **1. `scripts/notion_api/fetch_tasks.py`**
Récupère des tâches depuis Notion avec des filtres.

```python
from utils.config import get_notion_client, NOTION_DATABASE_ID
from utils.helpers import filter_tasks_by_context, sort_tasks_by_priority_and_duration
from utils.logger import logger

def fetch_tasks(filters: dict = None, sort: bool = True) -> list:
    """
    Récupère des tâches depuis Notion avec des filtres optionnels.
    
    Args:
        filters: Dictionnaire de filtres (ex: {"pays": "Thaïlande", "supports": ["Téléphone"]}).
        sort: Si True, trie les tâches par priorité et durée.
    
    Returns:
        Liste de tâches Notion.
    """
    notion = get_notion_client()
    
    # Récupérer toutes les tâches
    all_tasks = []
    start_cursor = None
    
    while True:
        response = notion.databases.query(
            database_id=NOTION_DATABASE_ID,
            start_cursor=start_cursor,
            page_size=100
        )
        all_tasks.extend(response["results"])
        start_cursor = response.get("next_cursor")
        if not start_cursor:
            break
    
    logger.info(f"Récupéré {len(all_tasks)} tâches depuis Notion")
    
    # Appliquer les filtres
    if filters:
        all_tasks = filter_tasks_by_context(all_tasks, filters)
        logger.info(f"Filtré à {len(all_tasks)} tâches")
    
    # Trier les tâches
    if sort:
        all_tasks = sort_tasks_by_priority_and_duration(all_tasks)
    
    return all_tasks

if __name__ == "__main__":
    # Exemple : Récupérer les tâches en Thaïlande sur téléphone, durée ≤ 30 min
    filters = {
        "pays": "Thaïlande",
        "supports": ["Téléphone"],
        "max_duration": "30 min",
        "status": "Terminé"
    }
    tasks = fetch_tasks(filters)
    
    for task in tasks[:3]:  # Afficher les 3 premières tâches
        props = task["properties"]
        print(f"- {props['Nom']['title'][0]['plain_text']} ({props['⏱️ Durée']['select']['name']}, {props['🎯 Priorité']['select']['name']})")
```

---

### **2. `scripts/notion_api/update_task.py`**
Met à jour une tâche dans Notion (ex: changer le statut).

```python
from utils.config import get_notion_client
from utils.logger import logger

def update_task(page_id: str, properties: dict) -> bool:
    """
    Met à jour une tâche dans Notion.
    
    Args:
        page_id: ID de la page Notion à mettre à jour.
        properties: Dictionnaire des propriétés à mettre à jour.
    
    Returns:
        True si la mise à jour a réussi, False sinon.
    """
    notion = get_notion_client()
    
    try:
        notion.pages.update(
            page_id=page_id,
            properties=properties
        )
        logger.info(f"Tâche {page_id} mise à jour avec succès")
        return True
    except Exception as e:
        logger.error(f"Échec de la mise à jour de la tâche {page_id}: {e}")
        return False

if __name__ == "__main__":
    # Exemple : Marquer une tâche comme "En cours"
    PAGE_ID = "ID_DE_LA_PAGE"  # Remplacez par un vrai ID
    properties = {
        "⚙️ Statut": {
            "status": {"name": "En cours"}
        }
    }
    update_task(PAGE_ID, properties)
```

---

### **3. `scripts/google_api/sync_calendar.py`**
Synchronise Google Calendar avec Notion (Calendar → Notion).

```python
from utils.config import get_google_calendar_service, NOTION_DATABASE_ID
from utils.logger import logger
from notion_api.create_task import create_task

def sync_calendar_to_notion(calendar_id: str = "primary", max_results: int = 10) -> None:
    """
    Synchronise les événements Google Calendar vers Notion.
    
    Args:
        calendar_id: ID du calendrier Google (par défaut "primary").
        max_results: Nombre maximal d'événements à synchroniser.
    """
    service = get_google_calendar_service()
    
    # Récupérer les événements
    now = datetime.utcnow().isoformat() + "Z"
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    events = events_result.get("items", [])
    
    logger.info(f"Récupéré {len(events)} événements depuis Google Calendar")
    
    for event in events:
        # Vérifier si l'événement existe déjà dans Notion (via un ID unique)
        event_id = event.get("id")
        existing_tasks = fetch_tasks(filters={"📅 Date Limite": event.get("start", {}).get("dateTime", "")})
        
        if not existing_tasks:
            # Créer une nouvelle tâche dans Notion
            task_properties = {
                "Nom": {
                    "title": [{"text": {"content": event.get("summary", "Sans titre")}}]
                },
                "⏱️ Durée": {
                    "select": {"name": "1h"}  # À adapter selon la durée de l'événement
                },
                "📅 Date Limite": {
                    "date": {
                        "start": event.get("start", {}).get("dateTime", event.get("start", {}).get("date"))
                    }
                },
                "⚙️ Statut": {
                    "status": {"name": "À planifier"}
                },
                "📌 Contexte": {
                    "rich_text": [{"text": {"content": event.get("description", "")}}]
                },
                "🔗 ID Google Calendar": {
                    "rich_text": [{"text": {"content": event_id}}]
                }
            }
            create_task(task_properties)
            logger.info(f"Tâche créée pour l'événement: {event.get('summary')}")

if __name__ == "__main__":
    sync_calendar_to_notion()
```

---

### **4. `scripts/google_api/send_email.py`**
Envoie un email via Gmail API (ex: résumé quotidien).

```python
from utils.config import get_gmail_service, GMAIL_SENDER_EMAIL
from utils.logger import logger
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to: str, subject: str, body: str, body_type: str = "html") -> bool:
    """
    Envoie un email via Gmail API.
    
    Args:
        to: Adresse email du destinataire.
        subject: Sujet de l'email.
        body: Corps de l'email (en HTML ou texte brut).
        body_type: Type du corps ("html" ou "plain").
    
    Returns:
        True si l'email a été envoyé, False sinon.
    """
    service = get_gmail_service()
    
    try:
        # Créer le message
        message = MIMEMultipart()
        message["to"] = to
        message["from"] = GMAIL_SENDER_EMAIL
        message["subject"] = subject
        message.attach(MIMEText(body, body_type))
        
        # Encoder le message
        raw_message = urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        
        # Envoyer l'email
        sent_message = service.users().messages().send(
            userId="me",
            body={"raw": raw_message}
        ).execute()
        
        logger.info(f"Email envoyé à {to} (ID: {sent_message['id']})")
        return True
    except Exception as e:
        logger.error(f"Échec de l'envoi de l'email: {e}")
        return False

if __name__ == "__main__":
    # Exemple : Envoyer un résumé quotidien
    to = "franck.savin@example.com"
    subject = "📅 Résumé quotidien - 30/06/2026"
    body = """
    <h1>📊 Résumé de Productivité</h1>
    <p><strong>Date:</strong> 30/06/2026</p>
    <p><strong>Tâches terminées:</strong> 8</p>
    <p><strong>Temps total:</strong> 4h15</p>
    <p><strong>Progrès:</strong> +20% vs hier | 🏆 3ème jour consécutif > 4h</p>
    """
    send_email(to, subject, body)
```

---

### **5. `scripts/automation/context_filter.py`**
Filtre contextuel : propose les meilleures tâches en fonction du contexte (temps, support, lieu).

```python
from notion_api.fetch_tasks import fetch_tasks
from utils.helpers import sort_tasks_by_priority_and_duration
from utils.logger import logger

def get_contextual_suggestions(pays: str, supports: list, available_time_min: int, limit: int = 3) -> list:
    """
    Propose les meilleures tâches en fonction du contexte.
    
    Args:
        pays: Pays/Lieu actuel (ex: "Thaïlande").
        supports: Liste des supports disponibles (ex: ["Téléphone", "PC Portable"]).
        available_time_min: Temps disponible en minutes (ex: 45).
        limit: Nombre maximal de suggestions (par défaut 3).
    
    Returns:
        Liste des tâches suggérées (format Notion API).
    """
    # Convertir le temps disponible en durée Notion (ex: 45 min → "45 min")
    duration_map = {30: "30 min", 45: "45 min", 60: "1h", 90: "1h30", 120: "2h"}
    max_duration = duration_map.get(available_time_min, "1h")
    
    # Récupérer et filtrer les tâches
    filters = {
        "pays": pays,
        "supports": supports,
        "max_duration": max_duration,
        "status": "Terminé",
        "min_priority": "Secondaire"  # Exclure les tâches optionnelles
    }
    tasks = fetch_tasks(filters)
    
    logger.info(f"Trouvé {len(tasks)} tâches correspondantes")
    
    # Retourner les meilleures suggestions
    return tasks[:limit]

def format_suggestions(tasks: list) -> str:
    """Formate les suggestions sous forme de tableau Markdown."""
    if not tasks:
        return "Aucune tâche ne correspond à votre contexte. Profitez de ce temps pour vous reposer ! 😊"
    
    header = "| Tâche | Durée | Priorité | Contexte |"
    separator = "|-------|-------|----------|---------|"
    rows = []
    
    for task in tasks:
        props = task["properties"]
        name = props["Nom"]["title"][0]["plain_text"]
        duration = props["⏱️ Durée"]["select"]["name"]
        priority = props["🎯 Priorité"]["select"]["name"]
        context = ", ".join([c["plain_text"] for c in props.get("📌 Contexte", {}).get("rich_text", [])])
        rows.append(f"| {name} | {duration} | {priority} | {context} |")
    
    return "\n".join([header, separator] + rows)

if __name__ == "__main__":
    # Exemple : "J’ai 45 min sur mon téléphone en Thaïlande"
    pays = "Thaïlande"
    supports = ["Téléphone"]
    available_time_min = 45
    
    suggestions = get_contextual_suggestions(pays, supports, available_time_min)
    print("🎯 Voici les tâches que tu peux faire :")
    print(format_suggestions(suggestions))
```

---

### **6. `scripts/automation/daily_summary.py`**
Génère un résumé quotidien des tâches terminées et l’envoie par email.

```python
from notion_api.fetch_tasks import fetch_tasks
from google_api.send_email import send_email
from utils.helpers import get_current_time
from utils.logger import logger
from datetime import datetime

def generate_daily_summary() -> dict:
    """
    Génère un résumé quotidien des tâches terminées.
    
    Returns:
        Dictionnaire avec les stats du jour.
    """
    today = get_current_time().strftime("%Y-%m-%d")
    
    # Récupérer les tâches terminées aujourd'hui
    filters = {
        "status": "Terminé",
        "date_completion": today  # Supposons que cette propriété existe
    }
    tasks = fetch_tasks(filters)
    
    # Calculer les statistiques
    total_tasks = len(tasks)
    total_time_min = sum(
        duration_to_minutes(task["properties"]["⏱️ Durée"]["select"]["name"]) 
        for task in tasks
    )
    
    # Répartition par priorité
    priority_counts = {"Urgent": 0, "Important": 0, "Secondaire": 0, "Optionnel": 0}
    for task in tasks:
        priority = task["properties"]["🎯 Priorité"]["select"]["name"]
        if priority in priority_counts:
            priority_counts[priority] += 1
    
    # Calculer la progression vs hier (simplifié)
    yesterday = (get_current_time() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_tasks = fetch_tasks({"status": "Terminé", "date_completion": yesterday})
    yesterday_time_min = sum(
        duration_to_minutes(task["properties"]["⏱️ Durée"]["select"]["name"]) 
        for task in yesterday_tasks
    )
    progress = ((total_time_min - yesterday_time_min) / yesterday_time_min * 100) if yesterday_time_min > 0 else 0
    
    return {
        "date": today,
        "total_tasks": total_tasks,
        "total_time_min": total_time_min,
        "priority_counts": priority_counts,
        "progress_percent": progress
    }

def format_summary(summary: dict) -> str:
    """Formate le résumé en Markdown/HTML pour email."""
    hours = summary["total_time_min"] // 60
    minutes = summary["total_time_min"] % 60
    time_str = f"{hours}h{minutes:02d}" if hours > 0 else f"{minutes} min"
    
    priority_str = ", ".join([f"{k}: {v}" for k, v in summary["priority_counts"].items() if v > 0])
    
    progress_str = f"+{summary['progress_percent']:.0f}% vs hier" if summary["progress_percent"] > 0 else \
                  f"{summary['progress_percent']:.0f}% vs hier"
    
    return f"""
    <h1>📅 Résumé de Productivité - {summary['date']}</h1>
    <p><strong>Tâches terminées:</strong> {summary['total_tasks']}</p>
    <p><strong>Temps total:</strong> {time_str}</p>
    <p><strong>Répartition par priorité:</strong> {priority_str}</p>
    <p><strong>Progrès:</strong> {progress_str}</p>
    """

if __name__ == "__main__":
    summary = generate_daily_summary()
    email_body = format_summary(summary)
    
    # Envoyer par email
    send_email(
        to="franck.savin@example.com",
        subject=f"📊 Résumé quotidien - {summary['date']}",
        body=email_body
    )
    
    logger.info(f"Résumé quotidien généré et envoyé pour le {summary['date']}")
```

---

### **7. `scripts/automation/delegate_task.py`**
Exécute une tâche marquée comme "À déléguer à l’IA" et met à jour Notion.

```python
import requests
from notion_api.fetch_tasks import fetch_tasks
from notion_api.update_task import update_task
from utils.config import MISTRAL_API_KEY
from utils.logger import logger

def delegate_task_to_mistral(task: dict) -> str:
    """
    Délègue une tâche à Mistral pour exécution.
    
    Args:
        task: Tâche Notion (format API).
    
    Returns:
        Résultat de l'exécution (ex: lien vers un brouillon).
    """
    props = task["properties"]
    task_name = props["Nom"]["title"][0]["plain_text"]
    task_context = ", ".join([c["plain_text"] for c in props.get("📌 Contexte", {}).get("rich_text", [])])
    task_id = task["id"]
    
    # Préparer la requête pour Mistral
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-medium",
        "messages": [
            {
                "role": "user",
                "content": f"Exécute la tâche suivante : {task_name}. Contexte : {task_context}. "
                           f"Prépare un brouillon ou un livrable que je pourrai valider. "
                           f"Si tu as besoin de plus d'informations, demande-moi."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()["choices"][0]["message"]["content"]
        logger.info(f"Tâche {task_name} exécutée par Mistral")
        return result
    except Exception as e:
        logger.error(f"Échec de l'exécution de la tâche {task_name}: {e}")
        return None

def process_delegable_tasks() -> None:
    """Traite toutes les tâches marquées comme "À déléguer à l’IA"."""
    # Récupérer les tâches à déléguer
    filters = {"⚙️ Statut": "À déléguer à l’IA"}
    tasks = fetch_tasks(filters)
    
    logger.info(f"Trouvé {len(tasks)} tâches à déléguer à l'IA")
    
    for task in tasks:
        # Déléguer à Mistral
        result = delegate_task_to_mistral(task)
        
        if result:
            # Mettre à jour Notion
            update_task(
                page_id=task["id"],
                properties={
                    "⚙️ Statut": {"status": {"name": "En attente de validation"}},
                    "🤖 Statut IA": {"select": {"name": "Terminée"}},
                    "📄 Livrable": {"url": result},
                    "📅 Date de Délégation": {"date": {"start": get_current_time().strftime("%Y-%m-%d")}}
                }
            )
            
            # Notifier l'utilisateur (ex: par email)
            send_email(
                to="franck.savin@example.com",
                subject=f"✅ Tâche terminée : {task['properties']['Nom']['title'][0]['plain_text']}",
                body=f"La tâche a été exécutée par Mistral. <a href='{result}'>Voir le livrable</a>."
            )
            logger.info(f"Tâche {task['id']} mise à jour et notification envoyée")

if __name__ == "__main__":
    process_delegable_tasks()
```

---

### **8. `scripts/automation/routines.py`**
Gère les routines (matin, soir, voyage) et génère des résumés de complétion.

```python
from notion_api.fetch_tasks import fetch_tasks
from notion_api.update_task import update_task
from utils.helpers import get_current_time
from utils.logger import logger

def get_routine_tasks(routine_type: str) -> list:
    """
    Récupère les tâches associées à une routine.
    
    Args:
        routine_type: Type de routine (ex: "Matin", "Soir", "Voyage").
    
    Returns:
        Liste des tâches de la routine.
    """
    # Supposons qu'il existe une base "Routines" avec une relation vers le Master Board
    # Ce script est un exemple simplifié
    filters = {"📌 Contexte": routine_type}
    return fetch_tasks(filters)

def mark_routine_as_completed(routine_id: str) -> bool:
    """
    Marque une routine comme complétée.
    
    Args:
        routine_id: ID de la routine dans Notion.
    
    Returns:
        True si la mise à jour a réussi.
    """
    # Mettre à jour la propriété "Complétion" de la routine
    return update_task(
        page_id=routine_id,
        properties={
            "✅ Complétion": {"checkbox": True},
            "📅 Dernière Complétion": {"date": {"start": get_current_time().strftime("%Y-%m-%d")}}
        }
    )

def generate_routine_summary(routine_type: str) -> dict:
    """
    Génère un résumé de complétion pour une routine.
    
    Args:
        routine_type: Type de routine (ex: "Matin").
    
    Returns:
        Dictionnaire avec le % de complétion et les tâches restantes.
    """
    tasks = get_routine_tasks(routine_type)
    total_tasks = len(tasks)
    completed_tasks = sum(
        1 for task in tasks 
        if task["properties"]["⚙️ Statut"]["status"]["name"] == "Terminé"
    )
    
    return {
        "routine_type": routine_type,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_percent": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    }

if __name__ == "__main__":
    # Exemple : Résumé de la routine "Matin"
    summary = generate_routine_summary("Matin")
    print(f"Routine {summary['routine_type']}: {summary['completed_tasks']}/{summary['total_tasks']} tâches terminées ({summary['completion_percent']:.0f}%)")
```

---

## ✅ **Bonnes Pratiques**

### **1. Gestion des Erreurs**
- **Utilisez `try/except`** pour tous les appels API.
- **Journalisez les erreurs** avec `logger.error()`.
- **Implémentez des réessais** pour les erreurs temporaires (ex: rate limiting).

**Exemple** :
```python
from time import sleep
from notion_client import APIError

max_retries = 3
retry_delay = 5  # secondes

for attempt in range(max_retries):
    try:
        tasks = fetch_tasks()
        break
    except APIError as e:
        logger.error(f"Erreur (attempt {attempt + 1}): {e}")
        if attempt < max_retries - 1:
            sleep(retry_delay)
        else:
            logger.error("Échec après 3 tentatives")
            raise
```

---

### **2. Optimisation des Appels API**
- **Cachez les résultats** des appels fréquents (ex: liste des tâches).
- **Utilisez la pagination** pour éviter de surcharger les API.
- **Limitez les requêtes** (ex: Notion permet 3 requêtes/seconde).

**Exemple de cache simple** :
```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=128)
def fetch_tasks_cached(filters: frozenset = None) -> list:
    # Convertir filters en frozenset pour le cache
    return fetch_tasks(dict(filters) if filters else {})
```

---

### **3. Sécurité**
- **Ne jamais commiter `.env`** (utilisez `.gitignore`).
- **Permissions minimales** : Donnez uniquement les permissions nécessaires aux tokens API.
- **Rotations des tokens** : Changez les tokens tous les 3-6 mois.

---

### **4. Tests**
- **Testez avec des données fictives** avant de passer en production.
- **Utilisez `unittest.mock`** pour simuler les appels API.
- **Validez les données** : Vérifiez que les tâches synchronisées (ex: Calendar ↔ Notion) sont cohérentes.

**Exemple de test unitaire** :
```python
import unittest
from unittest.mock import patch
from scripts.notion_api.fetch_tasks import fetch_tasks

class TestFetchTasks(unittest.TestCase):
    @patch('scripts.notion_api.fetch_tasks.get_notion_client')
    def test_fetch_tasks(self, mock_client):
        # Configurer le mock
        mock_client.return_value.databases.query.return_value = {
            "results": [
                {
                    "id": "1",
                    "properties": {
                        "Nom": {"title": [{"plain_text": "Test Task"}]},
                        "⏱️ Durée": {"select": {"name": "30 min"}},
                        "⚙️ Statut": {"status": {"name": "Pas commencé"}}
                    }
                }
            ]
        }
        
        # Appeler la fonction
        tasks = fetch_tasks()
        
        # Vérifier le résultat
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["properties"]["Nom"]["title"][0]["plain_text"], "Test Task")

if __name__ == "__main__":
    unittest.main()
```

---

### **5. Documentation**
- **Docstring** : Ajoutez des docstrings à toutes les fonctions (format Google).
- **Commentaires** : Expliquez les parties complexes du code.
- **Examples** : Ajoutez des exemples d’utilisation dans les `if __name__ == "__main__":`.

---

## 🤝 **Comment Contribuer**

### **1. Ajouter un Nouveau Script**
1. **Créez un fichier** dans le dossier approprié (`/scripts/notion_api`, `/scripts/google_api`, etc.).
2. **Ajoutez une docstring** expliquant le but du script.
3. **Utilisez les modules utilitaires** (`config.py`, `helpers.py`, `logger.py`).
4. **Testez le script** avec des données fictives.
5. **Documentez l’exemple** dans le `if __name__ == "__main__":`.

---

### **2. Améliorer un Script Existant**
1. **Forker le repository** (ou travailler sur une branche).
2. **Faire vos modifications** (optimisation, correction de bugs, nouvelles fonctionnalités).
3. **Tester** les changements.
4. **Ouvrir une Pull Request** avec une description claire des modifications.

---

### **3. Signaler un Bug**
1. **Ouvrir une Issue** sur GitHub.
2. **Décrivez le problème** :
   - Étapes pour reproduire.
   - Comportement attendu vs réel.
   - Logs d’erreur (si disponibles).
3. **Ajoutez des labels** (`bug`, `notion-api`, `google-api`, etc.).

---

## 📚 **Ressources Utiles**
- [Notion API Documentation](https://developers.notion.com/docs)
- [Google Calendar API Documentation](https://developers.google.com/calendar/api)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Mistral API Documentation](https://docs.mistral.ai/)
- [Python `notion-client` Library](https://github.com/ramnes/notion-sdk-py)
- [Python `google-api-python-client` Library](https://github.com/googleapis/google-api-python-client)

---

> **Prochaines Étapes** :
> - [ ] **Tester les scripts** avec des données réelles (Notion, Calendar).
> - [ ] **Ajouter des tests unitaires** pour les fonctions critiques.
> - [ ] **Documenter les cas d’usage avancés** (ex: synchronisation bidirectionnelle).
> - [ ] **Optimiser les performances** (cache, pagination, etc.).