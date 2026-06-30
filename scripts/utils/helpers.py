# Fonctions Utilitaires pour les Scripts Python

> **Fichier** : `scripts/utils/helpers.py`  
> **Rôle** : Fonctions réutilisables pour le filtrage, le tri, la manipulation des données, et les conversions.  
> **Dépendances** : `pytz`, `datetime`

---

## 📌 **Fonctionnalités**
- Gestion des **dates et fuseaux horaires** (UTC+7 pour la Thaïlande).
- Conversion des **durées** (ex: "30 min" → 30 minutes).
- **Filtrage** des tâches Notion selon un contexte (pays, support, durée, etc.).
- **Tri** des tâches par priorité et durée.
- **Calculs** pour la gamification (points, temps total, etc.).

---

## 🔧 **Code**

```python
import os
import pytz
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# ======================
# Configuration
# ======================
TIMEZONE = os.getenv("TIMEZONE", "Asia/Bangkok")

# ======================
# Fonctions de Date/Heure
# ======================

def get_current_time() -> datetime:
    """
    Récupère la date/heure actuelle dans le fuseau horaire configuré.
    
    Returns:
        datetime: Date/heure actuelle dans le fuseau horaire configuré.
    """
    tz = pytz.timezone(TIMEZONE)
    return datetime.now(tz)


def get_today_date_str() -> str:
    """
    Récupère la date du jour au format YYYY-MM-DD.
    
    Returns:
        str: Date du jour (ex: "2026-06-30").
    """
    return get_current_time().strftime("%Y-%m-%d")


def get_time_in_timezone(dt: datetime, timezone: str = TIMEZONE) -> datetime:
    """
    Convertit un datetime dans un fuseau horaire spécifique.
    
    Args:
        dt: datetime à convertir.
        timezone: Fuseau horaire cible (ex: "Asia/Bangkok").
    
    Returns:
        datetime: datetime converti.
    """
    tz = pytz.timezone(timezone)
    if dt.tzinfo is None:
        # Si dt n'a pas de timezone, on suppose qu'il est en UTC
        dt = pytz.utc.localize(dt)
    return dt.astimezone(tz)


# ======================
# Fonctions de Conversion de Durée
# ======================

def duration_to_minutes(duration_str: str) -> int:
    """
    Convertit une durée (ex: "30 min", "1h") en minutes.
    
    Args:
        duration_str: Chaîne représentant la durée (ex: "30 min", "1h", "Demi-journée").
    
    Returns:
        int: Durée en minutes.
    """
    duration_map = {
        "10 min": 10,
        "30 min": 30,
        "1h": 60,
        "1h30": 90,
        "2h": 120,
        "Demi-journée": 240,  # 4 heures
        "1 jour": 480,       # 8 heures
        "2 jours": 960,      # 16 heures
        "2 jours +": 1440     # 24 heures
    }
    return duration_map.get(duration_str, 0)


def minutes_to_duration(minutes: int) -> str:
    """
    Convertit des minutes en chaîne de durée (ex: 30 → "30 min", 60 → "1h").
    
    Args:
        minutes: Durée en minutes.
    
    Returns:
        str: Chaîne représentant la durée.
    """
    if minutes <= 10:
        return "10 min"
    elif minutes <= 30:
        return "30 min"
    elif minutes <= 60:
        return "1h"
    elif minutes <= 90:
        return "1h30"
    elif minutes <= 120:
        return "2h"
    elif minutes <= 240:
        return "Demi-journée"
    elif minutes <= 480:
        return "1 jour"
    elif minutes <= 960:
        return "2 jours"
    else:
        return "2 jours +"


# ======================
# Fonctions de Filtrage des Tâches
# ======================

def filter_tasks_by_context(
    tasks: List[Dict[str, Any]],
    context: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Filtre une liste de tâches Notion selon un contexte donné.
    
    Args:
        tasks: Liste de tâches Notion (format API).
        context: Dictionnaire avec les clés :
            - pays (str): Pays/Lieu (ex: "Thaïlande").
            - supports (list): Liste de supports (ex: ["Téléphone", "PC Portable"]).
            - max_duration (str): Durée maximale (ex: "30 min").
            - min_priority (str): Priorité minimale (ex: "Important").
            - status (str): Statut à exclure (ex: "Terminé").
            - date_limit (str): Date limite (ex: "2026-06-30").
    
    Returns:
        List[Dict[str, Any]]: Liste de tâches filtrées.
    """
    filtered_tasks = []
    max_duration_min = duration_to_minutes(context.get("max_duration", "1 jour +"))
    
    # Ordre de priorité pour le filtrage
    priority_order = {
        "Urgent": 4,
        "Important": 3,
        "Secondaire": 2,
        "Optionnel": 1,
        "Sans priorité": 0
    }
    min_priority_value = priority_order.get(context.get("min_priority", "Sans priorité"), 0)
    
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
        task_priority = props.get("🎯 Priorité", {}).get("select", {}).get("name", "Sans priorité")
        if priority_order.get(task_priority, 0) < min_priority_value:
            continue
        
        # Filtrer par Date Limite
        if context.get("date_limit"):
            task_date_limit = props.get("📅 Date Limite", {}).get("date", {}).get("start", "")
            if task_date_limit and task_date_limit > context["date_limit"]:
                continue
        
        # Filtrer par Contexte (mots-clés)
        if context.get("context_keywords"):
            task_context = props.get("📌 Contexte", {}).get("rich_text", [])
            task_context_text = " ".join([c.get("plain_text", "") for c in task_context]).lower()
            context_keywords = [kw.lower() for kw in context["context_keywords"]]
            if not any(keyword in task_context_text for keyword in context_keywords):
                continue
        
        filtered_tasks.append(task)
    
    return filtered_tasks


# ======================
# Fonctions de Tri des Tâches
# ======================

def sort_tasks_by_priority_and_duration(
    tasks: List[Dict[str, Any]],
    reverse_priority: bool = False
) -> List[Dict[str, Any]]:
    """
    Trie une liste de tâches par priorité (décroissante) puis par durée (croissante).
    
    Args:
        tasks: Liste de tâches Notion.
        reverse_priority: Si True, trie par priorité croissante.
    
    Returns:
        List[Dict[str, Any]]: Liste de tâches triées.
    """
    priority_order = {
        "Urgent": 4,
        "Important": 3,
        "Secondaire": 2,
        "Optionnel": 1,
        "Sans priorité": 0
    }
    
    def get_sort_key(task):
        props = task["properties"]
        priority = props.get("🎯 Priorité", {}).get("select", {}).get("name", "Sans priorité")
        duration = props.get("⏱️ Durée", {}).get("select", {}).get("name", "1 jour +")
        priority_value = priority_order.get(priority, 0)
        duration_min = duration_to_minutes(duration)
        
        if reverse_priority:
            return (priority_value, duration_min)
        else:
            return (-priority_value, duration_min)  # - pour tri décroissant
    
    return sorted(tasks, key=get_sort_key)


def sort_tasks_by_deadline(
    tasks: List[Dict[str, Any]],
    ascending: bool = True
) -> List[Dict[str, Any]]:
    """
    Trie une liste de tâches par date limite.
    
    Args:
        tasks: Liste de tâches Notion.
        ascending: Si True, trie par date croissante (proche → lointaine).
    
    Returns:
        List[Dict[str, Any]]: Liste de tâches triées.
    """
    def get_deadline(task):
        props = task["properties"]
        deadline = props.get("📅 Date Limite", {}).get("date", {}).get("start", "9999-12-31")
        try:
            return datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            return datetime.strptime("9999-12-31", "%Y-%m-%d")
    
    return sorted(tasks, key=get_deadline, reverse=not ascending)


# ======================
# Fonctions de Calcul pour la Gamification
# ======================

def calculate_points_for_task(task: Dict[str, Any]) -> int:
    """
    Calcule les points attribués pour une tâche terminée.
    
    Règles :
    - 10 points par 30 min de durée.
    - +50% pour les tâches Urgent ou Important.
    
    Args:
        task: Tâche Notion (format API).
    
    Returns:
        int: Nombre de points.
    """
    props = task["properties"]
    duration_str = props.get("⏱️ Durée", {}).get("select", {}).get("name", "30 min")
    priority = props.get("🎯 Priorité", {}).get("select", {}).get("name", "Secondaire")
    
    # Points de base (10 points par 30 min)
    duration_min = duration_to_minutes(duration_str)
    base_points = (duration_min / 30) * 10
    
    # Bonus pour priorité
    if priority in ["Urgent", "Important"]:
        base_points *= 1.5
    
    return int(base_points)


def calculate_daily_stats(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcule les statistiques quotidiennes à partir d'une liste de tâches terminées.
    
    Args:
        tasks: Liste de tâches Notion terminées.
    
    Returns:
        Dict[str, Any]: Dictionnaire avec les stats (tâches totales, temps total, points, etc.).
    """
    total_tasks = len(tasks)
    total_time_min = sum(
        duration_to_minutes(task["properties"]["⏱️ Durée"]["select"]["name"]) 
        for task in tasks
    )
    total_points = sum(calculate_points_for_task(task) for task in tasks)
    
    # Répartition par priorité
    priority_counts = {"Urgent": 0, "Important": 0, "Secondaire": 0, "Optionnel": 0}
    for task in tasks:
        priority = task["properties"]["🎯 Priorité"]["select"]["name"]
        if priority in priority_counts:
            priority_counts[priority] += 1
    
    # Répartition par contexte
    context_counts = {}
    for task in tasks:
        context_list = task["properties"].get("📌 Contexte", {}).get("rich_text", [])
        for c in context_list:
            context = c.get("plain_text", "Autre")
            context_counts[context] = context_counts.get(context, 0) + 1
    
    return {
        "total_tasks": total_tasks,
        "total_time_min": total_time_min,
        "total_points": total_points,
        "priority_counts": priority_counts,
        "context_counts": context_counts,
        "hours": total_time_min // 60,
        "minutes": total_time_min % 60
    }


# ======================
# Fonctions de Formatage
# ======================

def format_task_for_display(task: Dict[str, Any]) -> str:
    """
    Formate une tâche pour un affichage lisible (ex: dans un tableau).
    
    Args:
        task: Tâche Notion (format API).
    
    Returns:
        str: Chaîne formatée.
    """
    props = task["properties"]
    name = props.get("Nom", {}).get("title", [{}])[0].get("plain_text", "Sans nom")
    duration = props.get("⏱️ Durée", {}).get("select", {}).get("name", "?")
    priority = props.get("🎯 Priorité", {}).get("select", {}).get("name", "Sans priorité")
    context = ", ".join([
        c.get("plain_text", "") 
        for c in props.get("📌 Contexte", {}).get("rich_text", [])
    ])
    status = props.get("⚙️ Statut", {}).get("status", {}).get("name", "Pas commencé")
    
    return f"{name} | {duration} | {priority} | {context} | {status}"


def format_tasks_as_markdown_table(tasks: List[Dict[str, Any]]) -> str:
    """
    Formate une liste de tâches sous forme de tableau Markdown.
    
    Args:
        tasks: Liste de tâches Notion.
    
    Returns:
        str: Tableau Markdown.
    """
    if not tasks:
        return "Aucune tâche trouvée."
    
    header = "| Tâche | Durée | Priorité | Contexte | Statut |"
    separator = "|-------|-------|----------|---------|--------|"
    rows = []
    
    for task in tasks:
        props = task["properties"]
        name = props.get("Nom", {}).get("title", [{}])[0].get("plain_text", "Sans nom")
        duration = props.get("⏱️ Durée", {}).get("select", {}).get("name", "?")
        priority = props.get("🎯 Priorité", {}).get("select", {}).get("name", "Sans priorité")
        context = ", ".join([
            c.get("plain_text", "") 
            for c in props.get("📌 Contexte", {}).get("rich_text", [])
        ])
        status = props.get("⚙️ Statut", {}).get("status", {}).get("name", "Pas commencé")
        rows.append(f"| {name} | {duration} | {priority} | {context} | {status} |")
    
    return "\n".join([header, separator] + rows)


def format_daily_summary(summary: Dict[str, Any]) -> str:
    """
    Formate un résumé quotidien pour un email ou un affichage.
    
    Args:
        summary: Dictionnaire avec les stats quotidiennes.
    
    Returns:
        str: Résumé formaté.
    """
    hours = summary.get("hours", 0)
    minutes = summary.get("minutes", 0)
    time_str = f"{hours}h{minutes:02d}" if hours > 0 else f"{minutes} min"
    
    priority_str = ", ".join([
        f"{k}: {v}" 
        for k, v in summary.get("priority_counts", {}).items() 
        if v > 0
    ])
    
    context_str = ", ".join([
        f"{k}: {v}" 
        for k, v in summary.get("context_counts", {}).items()
    ])
    
    return f"""
📅 **Résumé Quotidien - {get_today_date_str()]**
✅ **Tâches terminées:** {summary.get('total_tasks', 0)}
⏱️ **Temps total:** {time_str}
🌟 **Points gagnés:** {summary.get('total_points', 0)}
📊 **Répartition par priorité:** {priority_str}
📌 **Répartition par contexte:** {context_str}
"""


# ======================
# Fonctions Diverses
# ======================

def get_time_until_deadline(deadline_str: str) -> Optional[timedelta]:
    """
    Calcule le temps restant jusqu'à une date limite.
    
    Args:
        deadline_str: Date limite au format YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS.
    
    Returns:
        timedelta: Temps restant, ou None si la date est invalide.
    """
    try:
        if "T" in deadline_str:
            deadline = datetime.fromisoformat(deadline_str)
        else:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        now = get_current_time()
        return deadline - now if deadline > now else None
    except ValueError:
        return None


def is_task_overdue(task: Dict[str, Any]) -> bool:
    """
    Vérifie si une tâche est en retard (date limite dépassée).
    
    Args:
        task: Tâche Notion (format API).
    
    Returns:
        bool: True si la tâche est en retard, False sinon.
    """
    deadline_str = task["properties"].get("📅 Date Limite", {}).get("date", {}).get("start", "")
    if not deadline_str:
        return False
    
    time_until = get_time_until_deadline(deadline_str)
    return time_until is None or time_until.total_seconds() < 0


# ======================
# Tests Unitaires (Exemple)
# ======================

if __name__ == "__main__":
    # Exemple 1: Conversion de durée
    print("30 min →", duration_to_minutes("30 min"), "minutes")
    print("1h →", duration_to_minutes("1h"), "minutes")
    print("120 →", minutes_to_duration(120))
    
    # Exemple 2: Date/heure
    print("Date du jour:", get_today_date_str())
    print("Heure actuelle:", get_current_time())
    
    # Exemple 3: Filtrage (simulé)
    mock_tasks = [
        {
            "properties": {
                "Nom": {"title": [{"plain_text": "Tâche 1"}]},
                "⏱️ Durée": {"select": {"name": "30 min"}},
                "💻 Support": {"multi_select": [{"name": "Téléphone"}]},
                "🌍 Pays/Lieu": {"select": {"name": "Thaïlande"}},
                "⚙️ Statut": {"status": {"name": "Pas commencé"}},
                "🎯 Priorité": {"select": {"name": "Urgent"}}
            }
        },
        {
            "properties": {
                "Nom": {"title": [{"plain_text": "Tâche 2"}]},
                "⏱️ Durée": {"select": {"name": "1h"}},
                "💻 Support": {"multi_select": [{"name": "PC Portable"}]},
                "🌍 Pays/Lieu": {"select": {"name": "France"}},
                "⚙️ Statut": {"status": {"name": "Pas commencé"}},
                "🎯 Priorité": {"select": {"name": "Important"}}
            }
        }
    ]
    
    context = {
        "pays": "Thaïlande",
        "supports": ["Téléphone"],
        "max_duration": "1h",
        "status": "Terminé"
    }
    
    filtered = filter_tasks_by_context(mock_tasks, context)
    print(f"\nTâches filtrées ({len(filtered)}):")
    for task in filtered:
        print(f"- {task['properties']['Nom']['title'][0]['plain_text']}")
    
    # Exemple 4: Tri
    sorted_tasks = sort_tasks_by_priority_and_duration(filtered)
    print("\nTâches triées par priorité/durée:")
    for task in sorted_tasks:
        print(f"- {task['properties']['Nom']['title'][0]['plain_text']} ({task['properties']['🎯 Priorité']['select']['name']})")
    
    # Exemple 5: Formatage
    print("\nTableau Markdown:")
    print(format_tasks_as_markdown_table(filtered))
```

---

## 📝 **Explications**

### **1. Fonctions de Date/Heure**
- **`get_current_time()`** : Récupère l’heure actuelle dans le fuseau horaire configuré (par défaut : Asia/Bangkok).
- **`get_today_date_str()`** : Retourne la date du jour au format `YYYY-MM-DD`.
- **`get_time_in_timezone()`** : Convertit un `datetime` dans un fuseau horaire spécifique.

---

### **2. Fonctions de Conversion de Durée**
- **`duration_to_minutes()`** : Convertit une durée Notion (ex: "30 min") en minutes.
- **`minutes_to_duration()`** : Convertit des minutes en durée Notion.

---

### **3. Fonctions de Filtrage**
- **`filter_tasks_by_context()`** : Filtre une liste de tâches selon un contexte (pays, supports, durée, priorité, statut, date limite, mots-clés de contexte).
  - **Exemple d’utilisation** :
    ```python
    context = {
        "pays": "Thaïlande",
        "supports": ["Téléphone"],
        "max_duration": "30 min",
        "min_priority": "Important"
    }
    filtered_tasks = filter_tasks_by_context(tasks, context)
    ```

---

### **4. Fonctions de Tri**
- **`sort_tasks_by_priority_and_duration()`** : Trie les tâches par **priorité (décroissante)** puis par **durée (croissante)**.
- **`sort_tasks_by_deadline()`** : Trie les tâches par **date limite (proche → lointaine)**.

---

### **5. Fonctions de Gamification**
- **`calculate_points_for_task()`** : Calcule les points pour une tâche terminée (10 points par 30 min + bonus pour priorité).
- **`calculate_daily_stats()`** : Calcule les statistiques quotidiennes (tâches totales, temps total, points, répartition par priorité/contexte).

---

### **6. Fonctions de Formatage**
- **`format_task_for_display()`** : Formate une tâche pour un affichage lisible.
- **`format_tasks_as_markdown_table()`** : Formate une liste de tâches en tableau Markdown.
- **`format_daily_summary()`** : Formate un résumé quotidien pour un email.

---

### **7. Fonctions Diverses**
- **`get_time_until_deadline()`** : Calcule le temps restant jusqu’à une date limite.
- **`is_task_overdue()`** : Vérifie si une tâche est en retard.

---

## 🚀 **Utilisation**

### **1. Dans un Script**
Importez les fonctions nécessaires depuis ce module :
```python
from utils.helpers import (
    get_current_time,
    duration_to_minutes,
    filter_tasks_by_context,
    sort_tasks_by_priority_and_duration,
    calculate_daily_stats,
    format_tasks_as_markdown_table
)

# Exemple : Filtrer et trier des tâches
context = {"pays": "Thaïlande", "supports": ["Téléphone"], "max_duration": "30 min"}
filtered_tasks = filter_tasks_by_context(tasks, context)
sorted_tasks = sort_tasks_by_priority_and_duration(filtered_tasks)

# Afficher sous forme de tableau
print(format_tasks_as_markdown_table(sorted_tasks))
```

---

### **2. Exécuter les Tests**
Exécutez le script directement pour voir des exemples d’utilisation :
```bash
python scripts/utils/helpers.py
```

---

## 📚 **Ressources**
- [Python `datetime` Documentation](https://docs.python.org/3/library/datetime.html)
- [Python `pytz` Documentation](https://pythonhosted.org/pytz/)
- [Notion API Property Types](https://developers.notion.com/docs/working-with-databases#property-types)