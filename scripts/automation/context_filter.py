# Filtre Contextuel pour les Tâches

> **Fichier** : `scripts/automation/context_filter.py`  
> **Rôle** : Proposer les meilleures tâches en fonction du contexte de l'utilisateur (temps disponible, support, localisation, etc.).  
> **Dépendances** : `notion_api.fetch_tasks`, `utils.helpers`, `utils.logger`

---

## 📌 **Fonctionnalités**
- **Filtrage intelligent** des tâches Notion selon le contexte.
- **Priorisation** par priorité, durée, et date limite.
- **Gestion des chevauchements** avec Google Calendar (optionnel).
- **Formatage des résultats** (tableau Markdown, liste vocalisée, etc.).
- **Journalisation** des actions pour le débogage.

---

## 🔧 **Code**

```python
from typing import List, Dict, Any, Optional
from notion_api.fetch_tasks import fetch_tasks_by_context
from utils.helpers import (
    filter_tasks_by_context,
    sort_tasks_by_priority_and_duration,
    format_tasks_as_markdown_table,
    duration_to_minutes,
    get_current_time
)
from utils.logger import logger, log_exception


def get_contextual_suggestions(
    pays: Optional[str] = None,
    supports: Optional[List[str]] = None,
    available_time_min: Optional[int] = None,
    max_suggestions: int = 3,
    exclude_status: str = "Terminé",
    min_priority: Optional[str] = None,
    context_keywords: Optional[List[str]] = None,
    database_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Propose les meilleures tâches en fonction du contexte de l'utilisateur.
    
    Args:
        pays: Pays/Lieu actuel (ex: "Thaïlande"). Si None, utilise "Global".
        supports: Liste des supports disponibles (ex: ["Téléphone", "PC Portable"]).
        available_time_min: Temps disponible en minutes (ex: 45).
        max_suggestions: Nombre maximal de suggestions à retourner (par défaut: 3).
        exclude_status: Statut à exclure (par défaut: "Terminé").
        min_priority: Priorité minimale (ex: "Important"). Si None, inclut toutes les priorités.
        context_keywords: Mots-clés de contexte pour filtrer les tâches (ex: ["Admin", "Client X"]).
        database_id: ID de la base Notion (par défaut: NOTION_DATABASE_ID depuis .env).
    
    Returns:
        List[Dict[str, Any]]: Liste des tâches suggérées (format Notion API), triées par priorité et durée.
    
    Exemple:
        >>> suggestions = get_contextual_suggestions(
        ...     pays="Thaïlande",
        ...     supports=["Téléphone"],
        ...     available_time_min=45
        ... )
    """
    # Construire le contexte de filtrage
    context = {"status": exclude_status}
    
    if pays:
        context["pays"] = pays
    
    if supports:
        context["supports"] = supports
    
    if available_time_min:
        # Convertir en durée Notion (ex: 45 → "45 min")
        if available_time_min <= 10:
            context["max_duration"] = "10 min"
        elif available_time_min <= 30:
            context["max_duration"] = "30 min"
        elif available_time_min <= 60:
            context["max_duration"] = "1h"
        elif available_time_min <= 90:
            context["max_duration"] = "1h30"
        elif available_time_min <= 120:
            context["max_duration"] = "2h"
        else:
            context["max_duration"] = "Demi-journée"
    
    if min_priority:
        context["min_priority"] = min_priority
    
    if context_keywords:
        context["context_keywords"] = context_keywords
    
    # Récupérer et filtrer les tâches
    tasks = fetch_tasks_by_context(context, database_id=database_id)
    
    logger.info(f"Trouvé {len(tasks)} tâches correspondantes au contexte: {context}")
    
    # Retourner les meilleures suggestions
    return tasks[:max_suggestions]


def format_suggestions(
    tasks: List[Dict[str, Any]],
    output_format: str = "markdown",
    include_details: bool = True
) -> str:
    """
    Formate les suggestions selon le format souhaité.
    
    Args:
        tasks: Liste de tâches suggérées.
        output_format: Format de sortie ("markdown", "text", "vocal").
        include_details: Si True, inclut les détails (durée, priorité, contexte).
    
    Returns:
        str: Suggestions formatées.
    """
    if not tasks:
        if output_format == "vocal":
            return "Aucune tâche ne correspond à votre contexte. Profitez de ce temps pour vous reposer !"
        else:
            return "Aucune tâche ne correspond à votre contexte."
    
    if output_format == "markdown":
        return format_tasks_as_markdown_table(tasks)
    
    elif output_format == "text":
        lines = []
        for i, task in enumerate(tasks, 1):
            props = task["properties"]
            name = props["Nom"]["title"][0]["plain_text"]
            if include_details:
                duration = props["⏱️ Durée"]["select"]["name"]
                priority = props["🎯 Priorité"]["select"]["name"]
                lines.append(f"{i}. {name} ({duration}, {priority})")
            else:
                lines.append(f"{i}. {name}")
        return "\n".join(lines)
    
    elif output_format == "vocal":
        if len(tasks) == 1:
            props = tasks[0]["properties"]
            name = props["Nom"]["title"][0]["plain_text"]
            duration = props["⏱️ Durée"]["select"]["name"]
            priority = props["🎯 Priorité"]["select"]["name"]
            return f"Je te suggère de faire : {name}. Cette tâche prendra {duration} et est de priorité {priority}."
        else:
            intro = f"J’ai trouvé {len(tasks)} tâches que tu peux faire : "
            suggestions = []
            for i, task in enumerate(tasks, 1):
                props = task["properties"]
                name = props["Nom"]["title"][0]["plain_text"]
                if include_details:
                    duration = props["⏱️ Durée"]["select"]["name"]
                    priority = props["🎯 Priorité"]["select"]["name"]
                    suggestions.append(f"{i}. {name} ({duration}, {priority})")
                else:
                    suggestions.append(f"{i}. {name}")
            return intro + ". ".join(suggestions)
    
    else:
        raise ValueError(f"Format de sortie non supporté: {output_format}")


def get_contextual_suggestions_with_calendar(
    pays: Optional[str] = None,
    supports: Optional[List[str]] = None,
    available_time_min: Optional[int] = None,
    max_suggestions: int = 3,
    calendar_events: Optional[List[Dict[str, Any]]] = None,
    database_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Propose des tâches en tenant compte des événements Google Calendar pour éviter les chevauchements.
    
    Args:
        pays: Pays/Lieu actuel.
        supports: Liste des supports disponibles.
        available_time_min: Temps disponible en minutes.
        max_suggestions: Nombre maximal de suggestions.
        calendar_events: Liste des événements Calendar (format Google API).
        database_id: ID de la base Notion.
    
    Returns:
        List[Dict[str, Any]]: Liste des tâches suggérées, en excluant celles qui chevauchent avec des événements.
    
    Note:
        Cette fonction suppose que `calendar_events` est une liste d'événements avec des clés 'start' et 'end'.
        Exemple d'événement : {"start": {"dateTime": "2026-06-30T14:00:00+07:00"}, "end": {"dateTime": "2026-06-30T15:00:00+07:00"}}
    """
    # Récupérer les suggestions initiales
    suggestions = get_contextual_suggestions(
        pays=pays,
        supports=supports,
        available_time_min=available_time_min,
        max_suggestions=max_suggestions * 2,  # Récupérer plus de suggestions pour tenir compte des chevauchements
        database_id=database_id
    )
    
    if not calendar_events:
        return suggestions[:max_suggestions]
    
    # Filtrer les tâches qui chevauchent avec des événements Calendar
    filtered_suggestions = []
    now = get_current_time()
    
    for task in suggestions:
        task_duration_min = duration_to_minutes(task["properties"]["⏱️ Durée"]["select"]["name"])
        
        # Supposons que la tâche commence maintenant (on pourrait aussi utiliser une date de début si disponible)
        task_start = now
        task_end = task_start + timedelta(minutes=task_duration_min)
        
        # Vérifier les chevauchements avec les événements Calendar
        has_conflict = False
        for event in calendar_events:
            event_start_str = event.get("start", {}).get("dateTime", event.get("start", {}).get("date"))
            event_end_str = event.get("end", {}).get("dateTime", event.get("end", {}).get("date"))
            
            if not event_start_str or not event_end_str:
                continue
            
            try:
                # Parser les dates de l'événement (format ISO 8601)
                if "T" in event_start_str:
                    event_start = datetime.fromisoformat(event_start_str)
                    event_end = datetime.fromisoformat(event_end_str)
                else:
                    event_start = datetime.strptime(event_start_str, "%Y-%m-%d")
                    event_end = datetime.strptime(event_end_str, "%Y-%m-%d") + timedelta(days=1)
                
                # Vérifier le chevauchement
                if task_start < event_end and task_end > event_start:
                    has_conflict = True
                    break
            except ValueError:
                continue
        
        if not has_conflict:
            filtered_suggestions.append(task)
    
    logger.info(f"Filtré {len(suggestions) - len(filtered_suggestions)} tâches en raison de chevauchements Calendar")
    return filtered_suggestions[:max_suggestions]


def smart_suggestions(
    query: str,
    database_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Interprète une requête naturelle et retourne des suggestions intelligentes.
    
    Args:
        query: Requête de l'utilisateur (ex: "J’ai 45 min sur mon téléphone en Thaïlande").
        database_id: ID de la base Notion.
    
    Returns:
        Dict[str, Any]: Dictionnaire avec :
            - suggestions: Liste des tâches suggérées.
            - formatted: Suggestions formatées (markdown, text, ou vocal).
            - context: Contexte extrait de la requête.
    
    Exemple:
        >>> result = smart_suggestions("J’ai 1h sur mon PC portable en France")
        >>> print(result["formatted"])
    """
    # Extraire le contexte de la requête (simplifié)
    context = {
        "pays": None,
        "supports": [],
        "available_time_min": None,
        "output_format": "markdown"
    }
    
    # Analyser la requête (exemple basique, à améliorer avec NLP)
    query_lower = query.lower()
    
    # Extraire le temps disponible
    time_keywords = {
        "10 min": 10,
        "30 min": 30,
        "1h": 60,
        "1 heure": 60,
        "2h": 120,
        "2 heures": 120,
        "demi-journée": 240,
        "1 jour": 480
    }
    
    for keyword, minutes in time_keywords.items():
        if keyword in query_lower:
            context["available_time_min"] = minutes
            break
    
    # Extraire les supports
    support_keywords = {
        "téléphone": "Téléphone",
        "mobile": "Téléphone",
        "pc portable": "PC Portable",
        "laptop": "PC Portable",
        "pc fixe": "PC Fixe",
        "desktop": "PC Fixe",
        "tablette": "Tablette"
    }
    
    for keyword, support in support_keywords.items():
        if keyword in query_lower:
            context["supports"].append(support)
    
    # Extraire le pays
    country_keywords = {
        "thaïlande": "Thaïlande",
        "france": "France",
        "saudi": "Saudi Arabia",
        "arabie saoudite": "Saudi Arabia",
        "bangkok": "Thaïlande",
        "paris": "France"
    }
    
    for keyword, country in country_keywords.items():
        if keyword in query_lower:
            context["pays"] = country
            break
    
    # Déterminer le format de sortie (par défaut: markdown)
    if "vocal" in query_lower or "dire" in query_lower or "lire" in query_lower:
        context["output_format"] = "vocal"
    elif "texte" in query_lower:
        context["output_format"] = "text"
    
    # Récupérer les suggestions
    suggestions = get_contextual_suggestions(
        pays=context["pays"],
        supports=context["supports"],
        available_time_min=context["available_time_min"],
        database_id=database_id
    )
    
    # Formater les suggestions
    formatted = format_suggestions(suggestions, output_format=context["output_format"])
    
    return {
        "suggestions": suggestions,
        "formatted": formatted,
        "context": context
    }


# ======================
# Exemples d'Utilisation
# ======================

if __name__ == "__main__":
    print("🎯 Exemples d'utilisation du filtre contextuel\n")
    
    # Exemple 1: Requête basique
    print("📌 Exemple 1: Requête basique")
    print("Requête: 'J’ai 45 min sur mon téléphone en Thaïlande'")
    result = smart_suggestions("J’ai 45 min sur mon téléphone en Thaïlande")
    print("Contexte extrait:", result["context"])
    print("\nSuggestions formatées (Markdown):")
    print(result["formatted"])
    print()
    
    # Exemple 2: Requête avec priorité
    print("📌 Exemple 2: Requête avec priorité")
    print("Requête: 'Quelles tâches urgentes puis-je faire sur mon PC portable ?'")
    result = smart_suggestions("Quelles tâches urgentes puis-je faire sur mon PC portable ?")
    print("Contexte extrait:", result["context"])
    print("\nSuggestions formatées (Texte):")
    # Forcer le format texte pour l'exemple
    result["formatted"] = format_suggestions(result["suggestions"], output_format="text")
    print(result["formatted"])
    print()
    
    # Exemple 3: Requête vocale
    print("📌 Exemple 3: Requête vocale")
    print("Requête: 'Dis-moi ce que je peux faire en 30 min'")
    result = smart_suggestions("Dis-moi ce que je peux faire en 30 min")
    print("Contexte extrait:", result["context"])
    print("\nSuggestions formatées (Vocal):")
    # Forcer le format vocal pour l'exemple
    result["formatted"] = format_suggestions(result["suggestions"], output_format="vocal")
    print(result["formatted"])
    print()
    
    # Exemple 4: Filtrage manuel
    print("📌 Exemple 4: Filtrage manuel")
    suggestions = get_contextual_suggestions(
        pays="Thaïlande",
        supports=["Téléphone", "PC Portable"],
        available_time_min=60,
        min_priority="Important"
    )
    print(f"Trouvé {len(suggestions)} tâches correspondantes")
    print("\nTableau Markdown:")
    print(format_suggestions(suggestions, output_format="markdown"))
```

---

## 📝 **Explications**

### **1. `get_contextual_suggestions()`**
- **Fonction principale** pour récupérer des suggestions de tâches en fonction du contexte.
- **Paramètres** :
  - `pays` : Pays/Lieu actuel (ex: "Thaïlande").
  - `supports` : Liste des supports disponibles (ex: ["Téléphone"]).
  - `available_time_min` : Temps disponible en minutes (ex: 45).
  - `max_suggestions` : Nombre maximal de suggestions (par défaut: 3).
  - `exclude_status` : Statut à exclure (par défaut: "Terminé").
  - `min_priority` : Priorité minimale (ex: "Important").
  - `context_keywords` : Mots-clés de contexte pour filtrer les tâches.
- **Retourne** : Liste des tâches suggérées, triées par priorité et durée.

---

### **2. `format_suggestions()`**
- Formate les suggestions selon le **format souhaité** :
  - **`markdown`** : Tableau Markdown (pour les widgets Notion).
  - **`text`** : Liste texte simple.
  - **`vocal`** : Phrase adaptée pour une sortie vocale (ex: via Google TTS).

---

### **3. `get_contextual_suggestions_with_calendar()`**
- **Filtrage avancé** qui tient compte des **événements Google Calendar** pour éviter les chevauchements.
- **Exemple** : Si un événement est prévu de 14h à 15h, une tâche de 1h ne sera pas suggérée à 14h.

---

### **4. `smart_suggestions()`**
- **Interprète une requête naturelle** (ex: "J’ai 45 min sur mon téléphone en Thaïlande") et extrait le contexte.
- **Utilise une analyse basique** (à améliorer avec NLP ou une IA comme Mistral).
- **Retourne** :
  - `suggestions` : Liste des tâches suggérées.
  - `formatted` : Suggestions formatées selon le format détecté.
  - `context` : Contexte extrait de la requête.

---

## 🚀 **Utilisation**

### **1. Requête Basique**
```python
from automation.context_filter import get_contextual_suggestions, format_suggestions

# Récupérer des suggestions
suggestions = get_contextual_suggestions(
    pays="Thaïlande",
    supports=["Téléphone"],
    available_time_min=45
)

# Afficher en Markdown
print(format_suggestions(suggestions, output_format="markdown"))
```

---

### **2. Requête Naturelle (Smart Suggestions)**
```python
from automation.context_filter import smart_suggestions

# Interpréter une requête naturelle
result = smart_suggestions("J’ai 1h sur mon PC portable en France")

# Afficher les suggestions formatées
print(result["formatted"])
```

---

### **3. Avec Google Calendar**
```python
from automation.context_filter import get_contextual_suggestions_with_calendar

# Supposons que calendar_events est une liste d'événements Google Calendar
calendar_events = [
    {
        "start": {"dateTime": "2026-06-30T14:00:00+07:00"},
        "end": {"dateTime": "2026-06-30T15:00:00+07:00"}
    }
]

# Récupérer des suggestions sans chevauchement
suggestions = get_contextual_suggestions_with_calendar(
    pays="Thaïlande",
    supports=["PC Portable"],
    available_time_min=60,
    calendar_events=calendar_events
)
```

---

### **4. Intégration avec Gemini/Mistral**
```python
from automation.context_filter import smart_suggestions

# Utiliser avec une IA pour interpréter la requête
user_query = "Qu’est-ce que je peux faire de productif avec 30 min sur mon téléphone ?"

# Obtenir des suggestions
result = smart_suggestions(user_query)

# Envoyer la réponse à l'utilisateur (ex: via vocal ou email)
print(result["formatted"])
```

---

## ✅ **Bonnes Pratiques**

1. **Toujours vérifier les paramètres** : Assurez-vous que `pays`, `supports`, et `available_time_min` sont valides.
2. **Limiter le nombre de suggestions** : `max_suggestions=3` est un bon défaut pour éviter la surcharge.
3. **Gérer les erreurs** : Utilisez `try/except` pour capturer les erreurs de filtrage ou de tri.
4. **Journaliser les actions** : Utilisez `logger.info()` pour suivre les requêtes et les résultats.
5. **Optimiser les requêtes** : Cachez les résultats si la même requête est faite plusieurs fois.

---

## 📚 **Ressources**
- [Notion API Query Documentation](https://developers.notion.com/docs/working-with-databases#querying-a-database)
- [Python `datetime` Documentation](https://docs.python.org/3/library/datetime.html)
- [Natural Language Processing with Python](https://realpython.com/nltk-nlp-python/) (pour améliorer `smart_suggestions`)
- [Google Calendar API Events](https://developers.google.com/calendar/api/v3/reference/events)