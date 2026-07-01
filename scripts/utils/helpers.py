from datetime import datetime, timedelta, timezone

DURATION_MINUTES = {
    "10 min": 10,
    "30 min": 30,
    "1h": 60,
    "1h30": 90,
    "2h": 120,
    "Demi-journée": 240,
    "1 jour+": 480,
}

URGENCE_ORDER = {
    "🔴 Urgent": 0,
    "🟡 Normal": 1,
    "⚪ Non urgent": 2,
}

IMPORTANCE_ORDER = {
    "🔴 Critique": 0,
    "🟠 Important": 1,
    "🟡 Secondaire": 2,
    "⚪ Optionnel": 3,
}


def get_prop(task: dict, name: str, kind: str):
    """Extrait la valeur d'une propriété Notion de façon sécurisée."""
    p = task.get("properties", {}).get(name, {})
    if kind == "title":
        items = p.get("title", [])
        return items[0]["plain_text"] if items else ""
    if kind == "select":
        s = p.get("select")
        return s["name"] if s else None
    if kind == "multi_select":
        return [s["name"] for s in p.get("multi_select", [])]
    if kind == "status":
        s = p.get("status")
        return s["name"] if s else None
    if kind == "rich_text":
        items = p.get("rich_text", [])
        return items[0]["plain_text"] if items else ""
    if kind == "date":
        d = p.get("date")
        return d["start"] if d else None
    return None


def filter_active(tasks: list) -> list:
    return [t for t in tasks if get_prop(t, "Statut", "status") != "Terminé"]


def filter_zombie(tasks: list, days: int = 21) -> list:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return [
        t for t in tasks
        if get_prop(t, "Statut", "status") == "Pas commencé"
        and datetime.fromisoformat(t["created_time"]) < cutoff
    ]


def sort_by_priority(tasks: list) -> list:
    """Tri Eisenhower : Urgence > Importance > Durée > Échéance."""
    def key(t):
        u = URGENCE_ORDER.get(get_prop(t, "🚨 Urgence", "select"), 99)
        i = IMPORTANCE_ORDER.get(get_prop(t, "💡 Importance", "select"), 99)
        d = DURATION_MINUTES.get(get_prop(t, "Durée", "select"), 9999)
        e = get_prop(t, "Échéance", "date") or "9999-12-31"
        return (u, i, d, e)
    return sorted(tasks, key=key)
