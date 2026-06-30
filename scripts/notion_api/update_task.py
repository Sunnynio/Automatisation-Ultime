# Mise à Jour des Tâches dans Notion

> **Fichier** : `scripts/notion_api/update_task.py`  
> **Rôle** : Mettre à jour les propriétés d'une tâche dans Notion (statut, priorité, durée, etc.).  
> **Dépendances** : `notion-client`, `utils.config`, `utils.logger`

---

## 📌 **Fonctionnalités**
- Mise à jour **une ou plusieurs propriétés** d'une tâche.
- Gestion des **différents types de propriétés** Notion (Sélection, Statut, Texte, Date, etc.).
- **Journalisation** des actions pour le débogage.
- **Vérification des erreurs** (ex: tâche introuvable, propriétés invalides).

---

## 🔧 **Code**

```python
from typing import Dict, Any, Optional, Union
from notion_client import Client, APIError
from utils.config import get_notion_client
from utils.logger import logger, log_exception


def update_task(
    page_id: str,
    properties: Dict[str, Any],
    notion_client: Optional[Client] = None
) -> bool:
    """
    Met à jour une ou plusieurs propriétés d'une tâche dans Notion.
    
    Args:
        page_id: ID de la page Notion à mettre à jour.
        properties: Dictionnaire des propriétés à mettre à jour (format Notion API).
        notion_client: Client Notion (par défaut : nouveau client via get_notion_client()).
    
    Returns:
        bool: True si la mise à jour a réussi, False sinon.
    
    Exemple:
        >>> update_task(
        ...     page_id="ID_DE_LA_PAGE",
        ...     properties={
        ...         "⚙️ Statut": {"status": {"name": "En cours"}},
        ...         "🎯 Priorité": {"select": {"name": "Urgent"}}
        ...     }
        ... )
    """
    if not notion_client:
        notion_client = get_notion_client()
    
    try:
        notion_client.pages.update(
            page_id=page_id,
            properties=properties
        )
        logger.info(f"Tâche {page_id} mise à jour avec succès")
        return True
    
    except APIError as e:
        log_exception(e, f"Échec de la mise à jour de la tâche {page_id}")
        return False
    
    except Exception as e:
        log_exception(e, f"Erreur inattendue lors de la mise à jour de la tâche {page_id}")
        return False


def update_task_status(
    page_id: str,
    status: str,
    notion_client: Optional[Client] = None
) -> bool:
    """
    Met à jour le statut d'une tâche.
    
    Args:
        page_id: ID de la page Notion.
        status: Nouveau statut (ex: "En cours", "Terminé", "À déléguer à l’IA").
        notion_client: Client Notion.
    
    Returns:
        bool: True si la mise à jour a réussi.
    
    Exemple:
        >>> update_task_status("ID_DE_LA_PAGE", "Terminé")
    """
    properties = {"⚙️ Statut": {"status": {"name": status}}}
    return update_task(page_id, properties, notion_client)


def update_task_priority(
    page_id: str,
    priority: str,
    notion_client: Optional[Client] = None
) -> bool:
    """
    Met à jour la priorité d'une tâche.
    
    Args:
        page_id: ID de la page Notion.
        priority: Nouvelle priorité (ex: "Urgent", "Important", "Secondaire").
        notion_client: Client Notion.
    
    Returns:
        bool: True si la mise à jour a réussi.
    """
    properties = {"🎯 Priorité": {"select": {"name": priority}}}
    return update_task(page_id, properties, notion_client)


def update_task_duration(
    page_id: str,
    duration: str,
    notion_client: Optional[Client] = None
) -> bool:
    """
    Met à jour la durée d'une tâche.
    
    Args:
        page_id: ID de la page Notion.
        duration: Nouvelle durée (ex: "30 min", "1h", "Demi-journée").
        notion_client: Client Notion.
    
    Returns:
        bool: True si la mise à jour a réussi.
    """
    properties = {"⏱️ Durée": {"select": {"name": duration}}}
    return update_task(page_id, properties, notion_client)


def update_task_support(
    page_id: str,
    supports: list,
    notion_client: Optional[Client] = None
) -> bool:
    """
    Met à jour les supports d'une tâche.
    
    Args:
        page_id: ID de la page Notion.
        supports: Liste des nouveaux supports (ex: ["Téléphone", "PC Portable"]).
        notion_client: Client Notion.
    
    Returns:
        bool: True si la mise à jour a réussi.
    """
    properties = {"💻 Support": {"multi_select": [{"name": s} for s in supports]}}
    return update_task(page_id, properties, notion_client)


def update_task_country(
    page_id: str,
    country: str,
    notion_client: Optional[Client] = None
) -> bool:
    """
    Met à jour le pays/lieu d'une tâche.
    
    Args:
        page_id: ID de la page Notion.
        country: Nouveau pays/lieu (ex: "Thaïlande", "France", "Global").
        notion_client: Client Notion.
    
    Returns:
        bool: True si la mise à jour a réussi.
    """
    properties = {"🌍 Pays/Lieu": {"select": {"name": country}}}
    return update_task(page_id, properties, notion_client)


def update_task_context(
    page_id: str,
    context: Union[str, list],
    notion_client: Optional[Client] = None
) -> bool:
    """
    Met à jour le contexte (mots-clés) d'une tâche.
    
    Args:
        page_id: ID de la page Notion.
        context: Nouveau contexte (chaîne ou liste de chaînes).
        notion_client: Client Notion.
    
    Returns:
        bool: True si la mise à jour a réussi.
    """
    if isinstance(context, str):
        context = [context]
    
    # Notion attend un tableau de "rich_text" pour le type Texte
    properties = {
        "📌 Contexte": {
            "rich_text": [{"type": "text", "text": {"content": c}} for c in context]
        }
    }
    return update_task(page_id, properties, notion_client)


def update_task_deadline(
    page_id: str,
    deadline: str,
    notion_client: Optional[Client] = None
) -> bool:
    """
    Met à jour la date limite d'une tâche.
    
    Args:
        page_id: ID de la page Notion.
        deadline: Nouvelle date limite (format YYYY-MM-DD).
        notion_client: Client Notion.
    
    Returns:
        bool: True si la mise à jour a réussi.
    """
    properties = {"📅 Date Limite": {"date": {"start": deadline}}}
    return update_task(page_id, properties, notion_client)


def update_task_delegation_status(
    page_id: str,
    status: str,
    livrable: Optional[str] = None,
    notion_client: Optional[Client] = None
) -> bool:
    """
    Met à jour le statut de délégation à l'IA et le livrable.
    
    Args:
        page_id: ID de la page Notion.
        status: Nouveau statut IA (ex: "En attente", "En cours", "Terminée", "Échec").
        livrable: URL du livrable (ex: lien vers un Google Doc).
        notion_client: Client Notion.
    
    Returns:
        bool: True si la mise à jour a réussi.
    """
    properties = {"🔄 Statut IA": {"select": {"name": status}}}
    
    if livrable:
        properties["📄 Livrable"] = {"url": livrable}
    
    return update_task(page_id, properties, notion_client)


def update_task_completion(
    page_id: str,
    completed: bool = True,
    completion_date: Optional[str] = None,
    real_time_min: Optional[int] = None,
    points: Optional[int] = None,
    notion_client: Optional[Client] = None
) -> bool:
    """
    Marque une tâche comme terminée et met à jour les champs de gamification.
    
    Args:
        page_id: ID de la page Notion.
        completed: Si True, marque comme terminée ; sinon, marque comme non terminée.
        completion_date: Date de complétion (format YYYY-MM-DD).
        real_time_min: Temps réel passé en minutes.
        points: Points attribués pour la tâche.
        notion_client: Client Notion.
    
    Returns:
        bool: True si la mise à jour a réussi.
    """
    properties = {"⚙️ Statut": {"status": {"name": "Terminé" if completed else "Pas commencé"}}}
    
    if completion_date:
        properties["✅ Date de Complétion"] = {"date": {"start": completion_date}}
    
    if real_time_min is not None:
        properties["⏱️ Temps Réel"] = {"number": real_time_min}
    
    if points is not None:
        properties["🌟 Points"] = {"number": points}
    
    return update_task(page_id, properties, notion_client)


def batch_update_tasks(
    updates: Dict[str, Dict[str, Any]],
    notion_client: Optional[Client] = None
) -> Dict[str, bool]:
    """
    Met à jour plusieurs tâches en une seule opération (séquentielle).
    
    Args:
        updates: Dictionnaire avec les IDs des tâches comme clés et les propriétés à mettre à jour comme valeurs.
        notion_client: Client Notion.
    
    Returns:
        Dict[str, bool]: Dictionnaire avec les IDs des tâches et un booléen indiquant si la mise à jour a réussi.
    
    Exemple:
        >>> updates = {
        ...     "ID_TASK_1": {"⚙️ Statut": {"status": {"name": "Terminé"}}},
        ...     "ID_TASK_2": {"🎯 Priorité": {"select": {"name": "Urgent"}}}
        ... }
        >>> results = batch_update_tasks(updates)
    """
    if not notion_client:
        notion_client = get_notion_client()
    
    results = {}
    for page_id, properties in updates.items():
        results[page_id] = update_task(page_id, properties, notion_client)
    
    return results


# ======================
# Exemples d'Utilisation
# ======================

if __name__ == "__main__":
    # Avertissement : Ces exemples nécessitent un vrai ID de page Notion
    print("⚠️  Ces exemples nécessitent un vrai ID de page Notion pour fonctionner.")
    print("   Remplacez 'ID_DE_LA_PAGE' par un ID valide pour tester.\n")
    
    # Exemple 1: Mettre à jour le statut
    print("📌 Exemple 1: Mettre à jour le statut d'une tâche")
    # update_task_status("ID_DE_LA_PAGE", "En cours")
    
    # Exemple 2: Mettre à jour la priorité
    print("📌 Exemple 2: Mettre à jour la priorité d'une tâche")
    # update_task_priority("ID_DE_LA_PAGE", "Urgent")
    
    # Exemple 3: Mettre à jour plusieurs propriétés
    print("📌 Exemple 3: Mettre à jour plusieurs propriétés")
    properties = {
        "⚙️ Statut": {"status": {"name": "À déléguer à l’IA"}},
        "🎯 Priorité": {"select": {"name": "Important"}},
        "📌 Contexte": {"rich_text": [{"type": "text", "text": {"content": "Test"}}]}
    }
    # update_task("ID_DE_LA_PAGE", properties)
    
    # Exemple 4: Marquer une tâche comme terminée
    print("📌 Exemple 4: Marquer une tâche comme terminée")
    # update_task_completion(
    #     "ID_DE_LA_PAGE",
    #     completed=True,
    #     completion_date="2026-06-30",
    #     real_time_min=45,
    #     points=15
    # )
    
    # Exemple 5: Mettre à jour le statut de délégation
    print("📌 Exemple 5: Mettre à jour le statut de délégation à l'IA")
    # update_task_delegation_status(
    #     "ID_DE_LA_PAGE",
    #     status="Terminée",
    #     livrable="https://docs.google.com/document/d/EXEMPLE"
    # )
    
    print("\n✅ Exemples affichés. Pour tester, décommentez les lignes et remplacez les IDs.")
```

---

## 📝 **Explications**

### **1. `update_task()`**
- **Fonction principale** pour mettre à jour une tâche dans Notion.
- **Accepte un dictionnaire de propriétés** au format Notion API.
- **Gère les erreurs** et journalise les actions.

---

### **2. Fonctions Spécialisées**
Chaque fonction met à jour un **type spécifique de propriété** :
- **`update_task_status()`** : Met à jour le **statut** (Kanban).
- **`update_task_priority()`** : Met à jour la **priorité** (Sélection).
- **`update_task_duration()`** : Met à jour la **durée** (Sélection).
- **`update_task_support()`** : Met à jour les **supports** (Sélection multiple).
- **`update_task_country()`** : Met à jour le **pays/lieu** (Sélection).
- **`update_task_context()`** : Met à jour le **contexte** (Texte).
- **`update_task_deadline()`** : Met à jour la **date limite** (Date).
- **`update_task_delegation_status()`** : Met à jour le **statut IA** et le **livrable** (pour les tâches délégables).
- **`update_task_completion()`** : Marque une tâche comme terminée et met à jour les champs de **gamification**.

---

### **3. `batch_update_tasks()`**
- Met à jour **plusieurs tâches en une seule opération** (séquentielle).
- Retourne un dictionnaire avec les résultats pour chaque tâche.

---

## 🚀 **Utilisation**

### **1. Mettre à Jour une Propriété Simple**
```python
from notion_api.update_task import update_task_status, update_task_priority

# Mettre à jour le statut
update_task_status("ID_DE_LA_PAGE", "Terminé")

# Mettre à jour la priorité
update_task_priority("ID_DE_LA_PAGE", "Urgent")
```

---

### **2. Mettre à Jour Plusieurs Propriétés**
```python
from notion_api.update_task import update_task

properties = {
    "⚙️ Statut": {"status": {"name": "En cours"}},
    "🎯 Priorité": {"select": {"name": "Important"}},
    "📌 Contexte": {"rich_text": [{"type": "text", "text": {"content": "Client X"}}]}
}
update_task("ID_DE_LA_PAGE", properties)
```

---

### **3. Marquer une Tâche comme Terminé**
```python
from notion_api.update_task import update_task_completion
from utils.helpers import get_today_date_str

update_task_completion(
    page_id="ID_DE_LA_PAGE",
    completed=True,
    completion_date=get_today_date_str(),
    real_time_min=45,
    points=15
)
```

---

### **4. Mettre à Jour Plusieurs Tâches**
```python
from notion_api.update_task import batch_update_tasks

updates = {
    "ID_TASK_1": {"⚙️ Statut": {"status": {"name": "Terminé"}}},
    "ID_TASK_2": {"🎯 Priorité": {"select": {"name": "Urgent"}}}
}
results = batch_update_tasks(updates)

for page_id, success in results.items():
    if success:
        print(f"✅ Tâche {page_id} mise à jour")
    else:
        print(f"❌ Échec pour la tâche {page_id}")
```

---

## ✅ **Bonnes Pratiques**

1. **Toujours vérifier l’ID de la page** : Un ID invalide entraînera une erreur API.
2. **Utiliser les types de propriétés corrects** : Notion est strict sur les formats (ex: `{"status": {"name": "..."}}` pour un Statut).
3. **Journaliser les mises à jour** : Utilisez `logger.info()` pour suivre les modifications.
4. **Gérer les erreurs** : Utilisez `try/except` pour capturer les `APIError` et autres exceptions.
5. **Éviter les mises à jour inutiles** : Ne mettez à jour que les propriétés qui ont changé.

---

## 📚 **Ressources**
- [Notion API Update Page Documentation](https://developers.notion.com/reference/update-a-page)
- [Notion API Property Types](https://developers.notion.com/docs/working-with-databases#property-types)
- [Python `notion-client` Library](https://github.com/ramnes/notion-sdk-py)