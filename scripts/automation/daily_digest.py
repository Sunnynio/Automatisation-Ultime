#!/usr/bin/env python3
"""
daily_digest.py — Génère le Daily Digest depuis le Master Board Notion

Récupère les tâches terminées et les tâches en cours, puis génère
un texte prêt à coller dans n'importe quelle IA (Claude, Mistral, Gemini).

Usage:
  python daily_digest.py
  python daily_digest.py --db <DATABASE_ID>

Prérequis :
  pip install notion-client python-dotenv
  Fichier .env avec NOTION_TOKEN et NOTION_DATABASE_ID
"""

import argparse
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

DURATION_MINUTES = {
    "10 min": 10,
    "30 min": 30,
    "1h": 60,
    "1h30": 90,
    "2h": 120,
    "Demi-journée": 240,
    "1 jour+": 480,
}


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
    return None


def main():
    parser = argparse.ArgumentParser(description="Daily Digest depuis le Master Board Notion")
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

    done = [t for t in all_tasks if get_prop(t, "Statut", "status") == "Terminé"]
    en_cours = [t for t in all_tasks if get_prop(t, "Statut", "status") == "En cours"]
    en_pause = [t for t in all_tasks if get_prop(t, "Statut", "status") == "En pause"]
    pas_commencé = [t for t in all_tasks if get_prop(t, "Statut", "status") == "Pas commencé"]

    total_min = sum(
        DURATION_MINUTES.get(get_prop(t, "Durée", "select") or "", 0)
        for t in done
    )
    h, m = divmod(total_min, 60)
    temps_total = f"{h}h{m:02d}" if h else (f"{m}min" if m else "0min")

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")

    print(f"\n=== DAILY DIGEST — {today} à {now} ===")
    print(f"Terminé : {len(done)} tâches  |  Temps estimé : {temps_total}")
    print(f"En cours : {len(en_cours)}  |  En pause : {len(en_pause)}  |  Pas commencé : {len(pas_commencé)}")

    print()
    if done:
        print("TÂCHES TERMINÉES :")
        for i, t in enumerate(done, 1):
            nom = get_prop(t, "Nom de la tâche", "title") or "(sans titre)"
            dur = get_prop(t, "Durée", "select") or "?"
            prio = get_prop(t, "Priorité", "select") or ""
            cat = get_prop(t, "Catégorie", "select") or ""
            details = " | ".join(x for x in [dur, prio, cat] if x)
            print(f"  {i}. {nom}  [{details}]")
    else:
        print("TÂCHES TERMINÉES : aucune")

    if en_cours:
        print()
        print("EN COURS :")
        for t in en_cours:
            nom = get_prop(t, "Nom de la tâche", "title") or "(sans titre)"
            dur = get_prop(t, "Durée", "select") or "?"
            print(f"  - {nom}  [{dur}]")

    if en_pause:
        print()
        print("EN PAUSE :")
        for t in en_pause:
            nom = get_prop(t, "Nom de la tâche", "title") or "(sans titre)"
            print(f"  - {nom}")

    print()
    print(
        ">>> Tu es mon assistant personnel. Génère un résumé de ma journée :\n"
        "    1. Ce qui a été accompli (groupe les tâches similaires si besoin)\n"
        "    2. Ce qui est encore en cours / en suspens\n"
        "    3. Une observation honnête sur la journée (patterns, efficacité, déséquilibre)\n"
        "    Format : 5-8 lignes max. Sois direct. Pas de congratulations inutiles."
    )


if __name__ == "__main__":
    main()
