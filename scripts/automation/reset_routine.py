#!/usr/bin/env python3
"""
reset_routine.py — Décoche toutes les cases d'une page de routine Notion

Usage:
  python reset_routine.py --matin       # Routine du Matin
  python reset_routine.py --aeroport    # Avant Aéroport
  python reset_routine.py --page <ID>   # Page personnalisée (ID sans tirets)

Prérequis :
  pip install notion-client python-dotenv
  Fichier .env avec NOTION_TOKEN
  Optionnel : ROUTINE_MATIN_ID et ROUTINE_AEROPORT_ID dans .env
"""

import argparse
import os
import sys

from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
ROUTINE_MATIN_ID = os.getenv("ROUTINE_MATIN_ID", "38fcace54fe1819e8b68f3208b6c7d1c")
ROUTINE_AEROPORT_ID = os.getenv("ROUTINE_AEROPORT_ID", "38fcace54fe1819fa390d727895c733e")


def get_notion():
    if not NOTION_TOKEN:
        print("ERREUR : NOTION_TOKEN manquant dans .env", file=sys.stderr)
        sys.exit(1)
    return Client(auth=NOTION_TOKEN)


def get_all_blocks(notion, page_id):
    results, cursor = [], None
    while True:
        params = {"block_id": page_id, "page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        resp = notion.blocks.children.list(**params)
        results.extend(resp["results"])
        cursor = resp.get("next_cursor")
        if not cursor:
            break
    return results


def reset_checkboxes(notion, page_id, page_name):
    blocks = get_all_blocks(notion, page_id)
    todo_blocks = [b for b in blocks if b.get("type") == "to_do"]
    checked = [b for b in todo_blocks if b.get("to_do", {}).get("checked", False)]

    if not checked:
        print(f"[{page_name}] Aucune case cochée — rien à faire.")
        return 0

    print(f"[{page_name}] {len(checked)}/{len(todo_blocks)} cases cochées → reset...")
    for block in checked:
        notion.blocks.update(block_id=block["id"], to_do={"checked": False})
    print(f"[{page_name}] ✓ {len(checked)} case(s) décochée(s).")
    return len(checked)


def main():
    parser = argparse.ArgumentParser(description="Reset les cases d'une routine Notion")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--matin", action="store_true", help="☀️ Routine du Matin")
    group.add_argument("--aeroport", action="store_true", help="✈️ Avant Aéroport")
    group.add_argument("--page", metavar="ID", help="ID de page Notion personnalisé")
    args = parser.parse_args()

    notion = get_notion()

    if args.matin:
        reset_checkboxes(notion, ROUTINE_MATIN_ID, "☀️ Routine du Matin")
    elif args.aeroport:
        reset_checkboxes(notion, ROUTINE_AEROPORT_ID, "✈️ Avant Aéroport")
    else:
        reset_checkboxes(notion, args.page, f"Page {args.page[:8]}...")


if __name__ == "__main__":
    main()
