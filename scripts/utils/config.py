# Configuration Centrale pour les Scripts Python

> **Fichier** : `scripts/utils/config.py`  
> **Rôle** : Charger les variables d'environnement et initialiser les clients API (Notion, Google Calendar, Gmail, Mistral).  
> **Dépendances** : `python-dotenv`, `notion-client`, `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`

---

## 📌 **Fonctionnalités**
- Chargement des variables d'environnement depuis `.env`.
- Initialisation des clients API pour Notion, Google Calendar, Gmail, et Mistral.
- Gestion centralisée des erreurs de configuration.

---

## 🔧 **Code**

```python
import os
from dotenv import load_dotenv
from notion_client import Client
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Optional

# Charger les variables d'environnement depuis .env
load_dotenv()

# ======================
# Variables Notion
# ======================
NOTION_TOKEN: Optional[str] = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID: Optional[str] = os.getenv("NOTION_DATABASE_ID")
NOTION_ROUTINES_DATABASE_ID: Optional[str] = os.getenv("NOTION_ROUTINES_DATABASE_ID")
NOTION_JOURNAL_DATABASE_ID: Optional[str] = os.getenv("NOTION_JOURNAL_DATABASE_ID")

# ======================
# Variables Google
# ======================
GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REFRESH_TOKEN: Optional[str] = os.getenv("GOOGLE_REFRESH_TOKEN")
GMAIL_SENDER_EMAIL: Optional[str] = os.getenv("GMAIL_SENDER_EMAIL")

# ======================
# Variables Mistral
# ======================
MISTRAL_API_KEY: Optional[str] = os.getenv("MISTRAL_API_KEY")

# ======================
# Variables Make.com
# ======================
MAKE_API_KEY: Optional[str] = os.getenv("MAKE_API_KEY")

# ======================
# Configuration Locale
# ======================
DATA_DIR: str = os.getenv("DATA_DIR", "./data")
TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Bangkok")

# ======================
# Initialisation des Clients API
# ======================

def get_notion_client() -> Client:
    """
    Initialise et retourne le client Notion.
    
    Returns:
        Client Notion authentifié.
    
    Raises:
        ValueError: Si NOTION_TOKEN n'est pas défini.
    """
    if not NOTION_TOKEN:
        raise ValueError(
            "NOTION_TOKEN non défini dans les variables d'environnement. "
            "Veuillez créer un fichier .env avec votre token Notion."
        )
    return Client(auth=NOTION_TOKEN)


def get_google_calendar_service() -> build:
    """
    Initialise et retourne le service Google Calendar.
    
    Returns:
        Service Google Calendar authentifié.
    
    Raises:
        ValueError: Si les identifiants Google ne sont pas définis.
    """
    if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN]):
        raise ValueError(
            "Les identifiants Google (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN) "
            "ne sont pas définis dans les variables d'environnement."
        )
    
    creds = Credentials(
        token=None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build("calendar", "v3", credentials=creds)


def get_gmail_service() -> build:
    """
    Initialise et retourne le service Gmail.
    
    Returns:
        Service Gmail authentifié.
    
    Raises:
        ValueError: Si les identifiants Google ne sont pas définis.
    """
    if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN]):
        raise ValueError(
            "Les identifiants Google (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN) "
            "ne sont pas définis dans les variables d'environnement."
        )
    
    creds = Credentials(
        token=None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build("gmail", "v1", credentials=creds)


def get_mistral_headers() -> dict:
    """
    Retourne les en-têtes pour les requêtes Mistral API.
    
    Returns:
        Dictionnaire avec les en-têtes (Authorization, Content-Type).
    
    Raises:
        ValueError: Si MISTRAL_API_KEY n'est pas défini.
    """
    if not MISTRAL_API_KEY:
        raise ValueError(
            "MISTRAL_API_KEY non défini dans les variables d'environnement."
        )
    return {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }


# ======================
# Vérification de la Configuration
# ======================

def check_config() -> bool:
    """
    Vérifie que toutes les variables d'environnement nécessaires sont définies.
    
    Returns:
        True si toutes les variables sont définies, False sinon.
    """
    required_vars = {
        "Notion": [NOTION_TOKEN, NOTION_DATABASE_ID],
        "Google": [GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN, GMAIL_SENDER_EMAIL],
        "Mistral": [MISTRAL_API_KEY]  # Optionnel pour certains scripts
    }
    
    all_ok = True
    for service, vars in required_vars.items():
        if service == "Mistral":
            continue  # Mistral est optionnel
        for var in vars:
            if not var:
                print(f"⚠️  Variable manquante pour {service}: {var}")
                all_ok = False
    
    if all_ok:
        print("✅ Toutes les variables d'environnement nécessaires sont définies.")
    return all_ok


if __name__ == "__main__":
    # Vérifier la configuration au démarrage
    check_config()
    
    # Exemple d'utilisation
    try:
        notion = get_notion_client()
        print("✅ Client Notion initialisé avec succès.")
    except ValueError as e:
        print(f"❌ Erreur: {e}")
    
    try:
        calendar_service = get_google_calendar_service()
        print("✅ Service Google Calendar initialisé avec succès.")
    except ValueError as e:
        print(f"❌ Erreur: {e}")
    
    try:
        gmail_service = get_gmail_service()
        print("✅ Service Gmail initialisé avec succès.")
    except ValueError as e:
        print(f"❌ Erreur: {e}")
    
    try:
        headers = get_mistral_headers()
        print("✅ En-têtes Mistral générés avec succès.")
    except ValueError as e:
        print(f"❌ Erreur: {e}")
```

---

## 📝 **Explications**

### **1. Chargement des Variables d’Environnement**
- Le fichier utilise `python-dotenv` pour charger les variables depuis `.env`.
- **Ne jamais commiter `.env`** (il contient des tokens sensibles). Utilisez `.env.example` comme template.

---

### **2. Clients API**
- **Notion** : Utilise la bibliothèque `notion-client` pour interagir avec l’API Notion.
- **Google Calendar/Gmail** : Utilise `google-api-python-client` et `google-auth` pour l’authentification OAuth 2.0.
- **Mistral** : Retourne simplement les en-têtes HTTP pour les requêtes à l’API Mistral.

---

### **3. Gestion des Erreurs**
- Chaque fonction vérifie que les variables d’environnement nécessaires sont définies.
- Si une variable manque, une `ValueError` est levée avec un message clair.

---

### **4. Vérification de la Configuration**
- La fonction `check_config()` permet de vérifier que toutes les variables nécessaires sont définies.
- Utile pour le débogage ou les scripts de démarrage.

---

## 🚀 **Utilisation**

### **1. Dans un Script**
Importez les fonctions nécessaires depuis ce module :
```python
from utils.config import get_notion_client, get_google_calendar_service, get_mistral_headers

# Initialiser les clients
notion = get_notion_client()
calendar_service = get_google_calendar_service()
headers = get_mistral_headers()
```

---

### **2. Vérifier la Configuration**
Exécutez le script directement pour vérifier que tout est bien configuré :
```bash
python scripts/utils/config.py
```

---

## 🔒 **Sécurité**
- **Ne jamais commiter `.env`** : Ajoutez `.env` à votre `.gitignore`.
- **Permissions minimales** : Donnez uniquement les permissions nécessaires aux tokens API.
- **Rotation des tokens** : Changez les tokens régulièrement (tous les 3-6 mois).

---

## 📚 **Ressources**
- [python-dotenv Documentation](https://saurabh-kumar.com/python-dotenv/)
- [Notion API Documentation](https://developers.notion.com/docs)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
- [Mistral API Documentation](https://docs.mistral.ai/)