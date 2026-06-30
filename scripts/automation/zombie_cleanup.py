#!/usr/bin/env python3
"""
zombie_cleanup.py — Nettoyage des tâches zombies du Master Board Notion

Remonte les tâches avec Statut = "Pas commencé" créées depuis plus de N jours
et génère un prompt de décision pour l'IA.

Usage:
  python zombie_cleanup.py                  # seuil par défaut : 21 jours
  python zombie_cleanup.py --jours 30       # seuil personnalisé
  python zombie_cleanup.py --db <ID>        # base alternative

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


def get_notion():
    if not NOTION_TOKEN:
        print("ERREUR : NOTION_TOKEN manquant dans .env", file=sys.stderr)
        sys.exit(1)
    return Client(auth=NOTION_TOKEN)


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


def get_prop(task, name, kind):
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
    return None


def main():
    parser = argparse.ArgumentParser(description="Nettoyage des tâches zombies")
    parser.add_argument("--jours", type=int, default=21, help="Seuil en jours (défaut: 21)")
    parser.add_argument("--db", metavar="ID", help="Remplace NOTION_DATABASE_ID du .env")
    args = parser.parse_args()

    db_id = args.db or NOTION_DATABASE_ID
    if not db_id:
        print("ERREUR : NOTION_DATABASE_ID manquant dans .env", file=sys.stderr)
        sys.exit(1)

    print("[Notion] Connexion...", file=sys.stderr)
    notion = get_notion()
    all_tasks = fetch_all(notion, db_id)
    print(f"[Notion] {len(all_tasks)} tâches chargées.", file=sys.stderr)

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.jours)
    zombies = [
        t for t in all_tasks
        if get_prop(t, "Statut", "status") == "Pas commencé"
        and datetime.fromisoformat(t["created_time"]) < cutoff
    ]

    today = datetime.now().strftime("%Y-%m-%d")

    print(f"\n=== NETTOYAGE ZOMBIE — {today} ===")
    print(f"Tâches 'Pas commencé' depuis > {args.jours} jours : {len(zombies)}")

    if not zombies:
        print("\nAucune tâche zombie. Base de données propre !")
        return

    print()
    for i, t in enumerate(zombies, 1):
        nom = get_prop(t, "Nom de la tâche", "title") or "(sans titre)"
        created = t.get("created_time", "")[:10]
        prio = get_prop(t, "Priorité", "select") or "sans priorité"
        cat = get_prop(t, "Catégorie", "select") or ""
        notes = get_prop(t, "Notes", "rich_text") or ""

        age_days = (datetime.now(timezone.utc) - datetime.fromisoformat(t["created_time"])).days

        details = f"créée le {created} ({age_days}j), {prio}"
        if cat:
            details += f", {cat}"

        print(f"{i}. {nom}")
        print(f"   [{details}]")
        if notes:
            print(f'   Notes : "{notes[:80]}"')
        print()

    print(
        f">>> Pour chaque tâche ci-dessus, réponds avec exactement ce format :\n"
        f"    N. [DÉCISION] — raison en une ligne\n\n"
        f"    Décisions possibles :\n"
        f"    GARDER    — la tâche est encore valide, sera faite bientôt\n"
        f"    ARCHIVER  — obsolète, abandonnée, ou plus pertinente\n"
        f"    DÉCOMPOSER — trop vague ou trop grosse, besoin de sous-tâches\n\n"
        f"    Sois direct et honnête. Une ligne par tâche. Pas de justification longue."
    )


if __name__ == "__main__":
    main()
