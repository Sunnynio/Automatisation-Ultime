#!/usr/bin/env python3
"""
fetch_tasks.py — Récupère les tâches du Master Board Notion et génère un prompt IA.

Usage:
  python fetch_tasks.py                               # liste toutes les tâches actives
  python fetch_tasks.py --done                        # tâches terminées (daily digest)
  python fetch_tasks.py --zombie                      # tâches bloquées > 21 jours
  python fetch_tasks.py --support Téléphone           # filtre par support
  python fetch_tasks.py --duree "30 min" "10 min"    # filtre par durée(s)
  python fetch_tasks.py --pays France                 # filtre par pays/lieu
  python fetch_tasks.py --context "j'ai 2h sur PC"   # contexte libre pour l'IA
  python fetch_tasks.py --support Téléphone --duree "30 min" --pays Thaïlande

Prérequis :
  pip install notion-client python-dotenv
  Fichier .env avec NOTION_TOKEN et NOTION_DATABASE_ID
"""

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

PRIORITY_ORDER = {
    "🔴 Urgent": 0,
    "🟠 Important": 1,
    "🟡 Secondaire": 2,
    "⚪ Optionnel": 3,
}

DURATION_MINUTES = {
    "10 min": 10,
    "30 min": 30,
    "1h": 60,
    "1h30": 90,
    "2h": 120,
    "Demi-journée": 240,
    "1 jour+": 480,
}


# ---------------------------------------------------------------------------
# Connexion
# ---------------------------------------------------------------------------

def get_client():
    if not NOTION_TOKEN:
        print("ERREUR : NOTION_TOKEN manquant. Ajoutez-le dans .env", file=sys.stderr)
        sys.exit(1)
    return Client(auth=NOTION_TOKEN)


def get_db_id(override=None):
    db_id = override or NOTION_DATABASE_ID
    if not db_id:
        print(
            "ERREUR : NOTION_DATABASE_ID manquant. Ajoutez-le dans .env ou utilisez --db",
            file=sys.stderr,
        )
        sys.exit(1)
    return db_id


# ---------------------------------------------------------------------------
# Extraction des propriétés Notion
# ---------------------------------------------------------------------------

def prop(task, name, kind):
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


# ---------------------------------------------------------------------------
# Récupération paginée
# ---------------------------------------------------------------------------

def fetch_all(notion, db_id):
    results, cursor = [], None
    while True:
        params = {"database_id": db_id, "page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        resp = notion.databases.query(**params)
        results.extend(resp["results"])
        cursor = resp.get("next_cursor")
        if not cursor:
            break
    return results


# ---------------------------------------------------------------------------
# Filtres
# ---------------------------------------------------------------------------

def filter_active(tasks):
    return [t for t in tasks if prop(t, "Statut", "status") != "Terminé"]


def filter_done(tasks):
    return [t for t in tasks if prop(t, "Statut", "status") == "Terminé"]


def filter_zombie(tasks, days=21):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return [
        t for t in tasks
        if prop(t, "Statut", "status") == "Pas commencé"
        and datetime.fromisoformat(t["created_time"]) < cutoff
    ]


def filter_session(tasks, supports=None, durees=None, pays=None):
    result = filter_active(tasks)

    if pays and pays != "Global":
        result = [
            t for t in result
            if prop(t, "Pays / Lieu", "select") in (pays, "Global", None)
        ]

    if supports:
        def ok_support(t):
            s = prop(t, "Support", "multi_select") or []
            return "Global" in s or any(x in s for x in supports)
        result = [t for t in result if ok_support(t)]

    if durees:
        result = [t for t in result if prop(t, "Durée", "select") in durees]

    def sort_key(t):
        p = PRIORITY_ORDER.get(prop(t, "Priorité", "select"), 99)
        d = DURATION_MINUTES.get(prop(t, "Durée", "select"), 9999)
        e = prop(t, "Échéance", "date") or "9999-12-31"
        return (p, d, e)

    result.sort(key=sort_key)
    return result


# ---------------------------------------------------------------------------
# Formatage
# ---------------------------------------------------------------------------

def task_line(t, i=None):
    nom = prop(t, "Nom de la tâche", "title") or "(sans titre)"
    statut = prop(t, "Statut", "status") or ""
    prio = prop(t, "Priorité", "select") or ""
    dur = prop(t, "Durée", "select") or ""
    sup = ", ".join(prop(t, "Support", "multi_select") or [])
    pays = prop(t, "Pays / Lieu", "select") or ""
    ech = prop(t, "Échéance", "date") or ""
    prefix = f"{i}. " if i is not None else "- "
    details = " | ".join(x for x in [dur, prio, sup, pays, ech] if x)
    return f"{prefix}{nom}  [{details}]  ({statut})"


def print_prompt(tasks, mode, context=None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if mode == "digest":
        print(f"=== DAILY DIGEST — {now} ===")
        print(f"Tâches terminées : {len(tasks)}\n")
        for i, t in enumerate(tasks, 1):
            print(task_line(t, i))
        print()
        print(
            ">>> Génère un résumé de la journée en 5 lignes max : ce qui a été accompli, "
            "patterns observés, ce qui reste en suspens. Sois direct et concis."
        )

    elif mode == "zombie":
        print(f"=== NETTOYAGE ZOMBIE — {now} ===")
        print(f"Tâches bloquées depuis > 21 jours : {len(tasks)}\n")
        for i, t in enumerate(tasks, 1):
            created = t.get("created_time", "")[:10]
            nom = prop(t, "Nom de la tâche", "title") or "(sans titre)"
            print(f"{i}. {nom}  [créée le {created}]")
        print()
        print(">>> Pour chaque tâche : indique GARDER / ARCHIVER / DÉCOMPOSER et pourquoi en une ligne.")

    elif mode == "session":
        print(f"=== SESSION PLANNING — {now} ===")
        if context:
            print(f"Contexte : {context}")
        print(f"Tâches disponibles ({len(tasks)}) :\n")
        for i, t in enumerate(tasks, 1):
            print(task_line(t, i))
        print()
        print(
            ">>> Construis un mini-agenda pour cette session. "
            "Regroupe les tâches dans le temps disponible. Ajoute des pauses si > 1h30. "
            "Priorise selon : Priorité > Durée courte > Échéance."
        )

    else:
        print(f"=== TÂCHES ACTIVES — {now} ({len(tasks)}) ===\n")
        for i, t in enumerate(tasks, 1):
            print(task_line(t, i))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Récupère les tâches Notion et génère un prompt pour n'importe quelle IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--done", action="store_true", help="Tâches terminées (daily digest)")
    parser.add_argument("--zombie", action="store_true", help="Tâches bloquées > 21 jours")
    parser.add_argument("--support", nargs="+", metavar="S", help="Ex: Téléphone 'PC Portable'")
    parser.add_argument("--duree", nargs="+", metavar="D", help="Ex: '30 min' '10 min' 1h")
    parser.add_argument("--pays", metavar="P", help="Ex: France Thaïlande Global")
    parser.add_argument("--context", metavar="TEXTE", help="Contexte libre pour l'IA")
    parser.add_argument("--db", metavar="ID", help="Remplace NOTION_DATABASE_ID du .env")
    args = parser.parse_args()

    db_id = get_db_id(args.db)
    notion = get_client()

    print(f"[Notion] Connexion... base: {db_id[:8]}...", file=sys.stderr)
    all_tasks = fetch_all(notion, db_id)
    print(f"[Notion] {len(all_tasks)} tâches chargées.", file=sys.stderr)

    if args.done:
        tasks = filter_done(all_tasks)
        print_prompt(tasks, "digest")
    elif args.zombie:
        tasks = filter_zombie(all_tasks)
        print_prompt(tasks, "zombie")
    elif args.support or args.duree or args.pays:
        tasks = filter_session(all_tasks, args.support, args.duree, args.pays)
        print_prompt(tasks, "session", args.context)
    elif args.context:
        tasks = filter_active(all_tasks)
        print_prompt(tasks, "session", args.context)
    else:
        tasks = filter_active(all_tasks)
        print_prompt(tasks, "list")


if __name__ == "__main__":
    main()
