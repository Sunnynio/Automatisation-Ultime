# Récupération des Tâches depuis Notion

> **Fichier** : `scripts/notion_api/fetch_tasks.py`  
> **Rôle** : Récupérer des tâches depuis une base Notion avec des filtres et un tri personnalisés.  
> **Dépendances** : `notion-client`, `utils.config`, `utils.helpers`, `utils.logger`

---

## 📌 **Fonctionnalités**
- Récupération de **toutes les tâches** d’une base Notion.
- **Filtrage** par contexte (pays, support, durée, priorité, statut, etc.).
- **Tri** par priorité et durée (ou autre critère).
- **Pagination** pour gérer les grandes bases.
- **Journalisation** des actions pour le débogage.

---

## 🔧 **Code**

```python
from typing import List, Dict, Any, Optional
from notion_client import Client
from utils.config import get_notion_client, NOTION_DATABASE_ID
from utils.helpers import filter_tasks_by_context, sort_tasks_by_priority_and_duration
from utils.logger import logger, log_exception


def fetch_all_tasks(
    database_id: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None,
    sort: bool = True,
    page_size: int = 100
) -> List[Dict[str, Any]]:
    """
    Récupère toutes les tâches d'une base Notion, avec pagination.
    
    Args:
        database_id: ID de la base Notion (par défaut : NOTION_DATABASE_ID depuis .env).
        filters: Dictionnaire de filtres (ex: {"pays": "Thaïlande", "supports": ["Téléphone"]}).
        sort: Si True, trie les tâches par priorité et durée.
        page_size: Nombre de tâches par page (max 100 pour Notion API).
    
    Returns:
        List[Dict[str, Any]]: Liste de toutes les tâches (format Notion API).
    
    Raises:
        ValueError: Si database_id n'est pas fourni et que NOTION_DATABASE_ID n'est pas défini.
    """
    if not database_id and not NOTION_DATABASE_ID:
        raise ValueError(
            "Aucun ID de base Notion fourni et NOTION_DATABASE_ID non défini dans .env. "
            "Veuillez fournir un database_id ou configurer NOTION_DATABASE_ID."
        )
    
    database_id = database_id or NOTION_DATABASE_ID
    notion = get_notion_client()
    
    all_tasks = []
    start_cursor = None
    
    logger.info(f"Récupération des tâches depuis la base Notion {database_id}")
    
    while True:
        try:
            response = notion.databases.query(
                database_id=database_id,
                start_cursor=start_cursor,
                page_size=page_size
            )
            all_tasks.extend(response["results"])
            start_cursor = response.get("next_cursor")
            
            if not start_cursor:
                break
            
            logger.debug(f"Récupéré {len(response['results'])} tâches (cursor: {start_cursor})")
        
        except Exception as e:
            log_exception(e, f"Erreur lors de la récupération des tâches (cursor: {start_cursor})")
            raise
    
    logger.info(f"Total tâches récupérées: {len(all_tasks)}")
    
    # Appliquer les filtres si fournis
    if filters:
        all_tasks = filter_tasks_by_context(all_tasks, filters)
        logger.info(f"Tâches après filtrage: {len(all_tasks)}")
    
    # Trier les tâches si demandé
    if sort:
        all_tasks = sort_tasks_by_priority_and_duration(all_tasks)
    
    return all_tasks


def fetch_tasks_by_context(
    context: Dict[str, Any],
    database_id: Optional[str] = None,
    sort: bool = True
) -> List[Dict[str, Any]]:
    """
    Récupère des tâches filtrées par contexte.
    
    Args:
        context: Dictionnaire de contexte pour le filtrage (ex: {"pays": "Thaïlande", "supports": ["Téléphone"]}).
        database_id: ID de la base Notion (par défaut : NOTION_DATABASE_ID).
        sort: Si True, trie les tâches par priorité et durée.
    
    Returns:
        List[Dict[str, Any]]: Liste de tâches filtrées et triées.
    
    Exemple:
        >>> context = {
        ...     "pays": "Thaïlande",
        ...     "supports": ["Téléphone"],
        ...     "max_duration": "30 min",
        ...     "status": "Terminé"
        ... }
        >>> tasks = fetch_tasks_by_context(context)
    """
    tasks = fetch_all_tasks(database_id=database_id, filters=context, sort=sort)
    return tasks


def fetch_tasks_by_status(
    status: str,
    database_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Récupère des tâches par statut.
    
    Args:
        status: Statut des tâches à récupérer (ex: "À déléguer à l’IA", "Terminé").
        database_id: ID de la base Notion.
    
    Returns:
        List[Dict[str, Any]]: Liste de tâches avec le statut spécifié.
    """
    context = {"status": status}
    return fetch_tasks_by_context(context, database_id)


def fetch_tasks_by_priority(
    priority: str,
    database_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Récupère des tâches par priorité.
    
    Args:
        priority: Priorité des tâches (ex: "Urgent", "Important").
        database_id: ID de la base Notion.
    
    Returns:
        List[Dict[str, Any]]: Liste de tâches avec la priorité spécifiée.
    """
    context = {"min_priority": priority}
    return fetch_tasks_by_context(context, database_id)


def fetch_tasks_by_country(
    country: str,
    database_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Récupère des tâches par pays/lieu.
    
    Args:
        country: Pays ou lieu des tâches (ex: "Thaïlande", "France").
        database_id: ID de la base Notion.
    
    Returns:
        List[Dict[str, Any]]: Liste de tâches pour le pays spécifié.
    """
    context = {"pays": country}
    return fetch_tasks_by_context(context, database_id)


def fetch_tasks_by_support(
    supports: List[str],
    database_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Récupère des tâches par support.
    
    Args:
        supports: Liste des supports (ex: ["Téléphone", "PC Portable"]).
        database_id: ID de la base Notion.
    
    Returns:
        List[Dict[str, Any]]: Liste de tâches pour les supports spécifiés.
    """
    context = {"supports": supports}
    return fetch_tasks_by_context(context, database_id)


def fetch_tasks_by_duration(
    max_duration: str,
    database_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Récupère des tâches par durée maximale.
    
    Args:
        max_duration: Durée maximale (ex: "30 min", "1h").
        database_id: ID de la base Notion.
    
    Returns:
        List[Dict[str, Any]]: Liste de tâches avec une durée ≤ max_duration.
    """
    context = {"max_duration": max_duration}
    return fetch_tasks_by_context(context, database_id)


# ======================
# Exemples d'Utilisation
# ======================

if __name__ == "__main__":
    # Exemple 1: Récupérer toutes les tâches
    print("📌 Récupération de toutes les tâches...")
    all_tasks = fetch_all_tasks()
    print(f"Total: {len(all_tasks)} tâches\n")
    
    # Exemple 2: Filtrer par contexte (Thaïlande, Téléphone, 30 min max)
    print("📌 Tâches en Thaïlande sur téléphone (≤ 30 min):")
    context = {
        "pays": "Thaïlande",
        "supports": ["Téléphone"],
        "max_duration": "30 min",
        "status": "Terminé"
    }
    filtered_tasks = fetch_tasks_by_context(context)
    for task in filtered_tasks[:3]:  # Afficher les 3 premières
        props = task["properties"]
        print(f"- {props['Nom']['title'][0]['plain_text']} ({props['⏱️ Durée']['select']['name']})")
    print()
    
    # Exemple 3: Récupérer les tâches "À déléguer à l’IA"
    print("📌 Tâches à déléguer à l’IA:")
    delegable_tasks = fetch_tasks_by_status("À déléguer à l’IA")
    for task in delegable_tasks:
        print(f"- {task['properties']['Nom']['title'][0]['plain_text']}")
    print()
    
    # Exemple 4: Récupérer les tâches urgentes
    print("📌 Tâches urgentes:")
    urgent_tasks = fetch_tasks_by_priority("Urgent")
    for task in urgent_tasks:
        print(f"- {task['properties']['Nom']['title'][0]['plain_text']}")
    print()
    
    # Exemple 5: Récupérer les tâches pour la France
    print("📌 Tâches pour la France:")
    france_tasks = fetch_tasks_by_country("France")
    for task in france_tasks:
        print(f"- {task['properties']['Nom']['title'][0]['plain_text']}")
```

---

## 📝 **Explications**

### **1. `fetch_all_tasks()`**
- **Fonction principale** pour récupérer toutes les tâches d’une base Notion.
- **Gère la pagination** automatiquement (Notion limite à 100 tâches par requête).
- **Applique les filtres** si fournis (via `filter_tasks_by_context`).
- **Trie les tâches** par priorité et durée si `sort=True`.

---

### **2. `fetch_tasks_by_context()`**
- **Fonction de haut niveau** pour récupérer des tâches filtrées par contexte.
- **Utilise `filter_tasks_by_context`** pour appliquer les filtres.
- **Retourne les tâches triées** si `sort=True`.

---

### **3. Fonctions Spécialisées**
- **`fetch_tasks_by_status()`** : Filtre par statut (ex: "À déléguer à l’IA").
- **`fetch_tasks_by_priority()`** : Filtre par priorité (ex: "Urgent").
- **`fetch_tasks_by_country()`** : Filtre par pays/lieu (ex: "Thaïlande").
- **`fetch_tasks_by_support()`** : Filtre par support (ex: ["Téléphone"]).
- **`fetch_tasks_by_duration()`** : Filtre par durée maximale (ex: "30 min").

---

## 🚀 **Utilisation**

### **1. Récupérer Toutes les Tâches**
```python
from notion_api.fetch_tasks import fetch_all_tasks

# Récupérer toutes les tâches de la base par défaut
all_tasks = fetch_all_tasks()

# Récupérer toutes les tâches d'une base spécifique
all_tasks = fetch_all_tasks(database_id="ID_DE_LA_BASE")
```

---

### **2. Filtrer par Contexte**
```python
from notion_api.fetch_tasks import fetch_tasks_by_context

# Définir le contexte
context = {
    "pays": "Thaïlande",
    "supports": ["Téléphone", "PC Portable"],
    "max_duration": "1h",
    "min_priority": "Important",
    "status": "Terminé"
}

# Récupérer les tâches filtrées
tasks = fetch_tasks_by_context(context)
```

---

### **3. Utiliser les Fonctions Spécialisées**
```python
from notion_api.fetch_tasks import (
    fetch_tasks_by_status,
    fetch_tasks_by_priority,
    fetch_tasks_by_country
)

# Tâches à déléguer à l'IA
delegable_tasks = fetch_tasks_by_status("À déléguer à l’IA")

# Tâches urgentes
urgent_tasks = fetch_tasks_by_priority("Urgent")

# Tâches pour la Thaïlande
thailand_tasks = fetch_tasks_by_country("Thaïlande")
```

---

## ✅ **Bonnes Pratiques**

1. **Toujours gérer les erreurs** : Utilisez `try/except` pour capturer les erreurs API.
2. **Limiter les requêtes** : Notion limite à **3 requêtes/seconde**. Ajoutez un délai si nécessaire.
3. **Cachez les résultats** : Pour les requêtes fréquentes, utilisez un cache (ex: `@lru_cache`).
4. **Journalisez les actions** : Utilisez `logger.info()` pour suivre l’exécution.

---

## 📚 **Ressources**
- [Notion API Documentation](https://developers.notion.com/docs/working-with-databases)
- [Notion API Pagination](https://developers.notion.com/docs/pagination)
- [Python `notion-client` Library](https://github.com/ramnes/notion-sdk-py)