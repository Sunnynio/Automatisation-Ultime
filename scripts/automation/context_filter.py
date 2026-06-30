#!/usr/bin/env python3
"""
context_filter.py — Session Planning interactif depuis le Master Board Notion

Guide l'utilisateur à construire un agenda de session depuis ses tâches Notion.
Sans arguments : mode interactif (questions-réponses).
Avec arguments : mode CLI direct.

Usage:
  python context_filter.py                                        # mode interactif
  python context_filter.py --temps 3h                            # 3h, tous supports, partout
  python context_filter.py --temps 45min --support Téléphone     # 45min sur téléphone
  python context_filter.py --temps 2h --support "PC Portable" --pays France
  python context_filter.py --temps 1h30 --support Téléphone --pays Thaïlande --context "matinée calme"

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
# Connexion Notion
# ---------------------------------------------------------------------------

def get_notion():
    if not NOTION_TOKEN:
        print("ERREUR : NOTION_TOKEN manquant dans .env", file=sys.stderr)
        sys.exit(1)
    return Client(auth=NOTION_TOKEN)


def fetch_all(notion):
    db_id = NOTION_DATABASE_ID
    if not db_id:
        print("ERREUR : NOTION_DATABASE_ID manquant dans .env", file=sys.stderr)
        sys.exit(1)
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
    if kind == "date":
        d = p.get("date")
        return d["start"] if d else None
    return None


# ---------------------------------------------------------------------------
# Parsing du temps
# ---------------------------------------------------------------------------

def parse_time(s):
    """Convertit '3h', '45min', '1h30', '120' en minutes."""
    s = s.strip().lower().replace(" ", "")
    if "h" in s and "min" in s:
        h_part, rest = s.split("h")
        return int(h_part) * 60 + int(rest.replace("min", ""))
    if "h" in s:
        parts = s.split("h")
        return int(parts[0]) * 60 + (int(parts[1]) if parts[1] else 0)
    if "min" in s:
        return int(s.replace("min", ""))
    try:
        return int(s)
    except ValueError:
        return None


def durees_dans_budget(budget_min):
    return [k for k, v in DURATION_MINUTES.items() if v <= budget_min]


# ---------------------------------------------------------------------------
# Filtrage et tri
# ---------------------------------------------------------------------------

def filter_and_sort(tasks, supports, durees_ok, pays):
    result = [t for t in tasks if get_prop(t, "Statut", "status") != "Terminé"]

    if pays and pays != "Global":
        result = [
            t for t in result
            if get_prop(t, "Pays / Lieu", "select") in (pays, "Global", None)
        ]

    if supports:
        def ok(t):
            s = get_prop(t, "Support", "multi_select") or []
            return "Global" in s or any(x in s for x in supports)
        result = [t for t in result if ok(t)]

    if durees_ok:
        result = [t for t in result if get_prop(t, "Durée", "select") in durees_ok]

    def key(t):
        p = PRIORITY_ORDER.get(get_prop(t, "Priorité", "select"), 99)
        d = DURATION_MINUTES.get(get_prop(t, "Durée", "select"), 9999)
        e = get_prop(t, "Échéance", "date") or "9999-12-31"
        return (p, d, e)

    result.sort(key=key)
    return result


# ---------------------------------------------------------------------------
# Mode interactif
# ---------------------------------------------------------------------------

def prompt_interactif():
    print("=" * 55)
    print("     SESSION PLANNING — Automatisation-Ultime")
    print("=" * 55)
    print()

    temps_str = input("Combien de temps as-tu ? (ex: 3h, 45min, 1h30) : ").strip()
    budget = parse_time(temps_str)
    if not budget:
        print(f"Durée non reconnue : '{temps_str}'. Exemples valides : 3h, 45min, 1h30, 120")
        sys.exit(1)

    print()
    print("Supports disponibles : Téléphone / PC Portable / PC Fixe")
    support_str = input("Sur quel(s) support(s) ? (Entrée = tous) : ").strip()
    supports = [s.strip() for s in support_str.split(",")] if support_str else None

    print()
    print("Lieux : Global / Thaïlande / France / Saudi Arabia / Avion / Hôtel")
    pays_str = input("Pays/Lieu actuel ? (Entrée = tous) : ").strip()
    pays = pays_str if pays_str else None

    print()
    contexte = input("Contexte additionnel ? (ex: matinée calme, avion, en déplacement — Entrée pour ignorer) : ").strip()

    return budget, supports, pays, contexte


# ---------------------------------------------------------------------------
# Génération du prompt
# ---------------------------------------------------------------------------

def build_prompt(tasks, budget, supports, pays, contexte):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    h, m = divmod(budget, 60)
    budget_str = f"{h}h{m:02d}" if h else f"{m}min"

    ctx_parts = [f"Temps disponible : {budget_str}"]
    if supports:
        ctx_parts.append(f"Support : {', '.join(supports)}")
    if pays:
        ctx_parts.append(f"Lieu : {pays}")
    if contexte:
        ctx_parts.append(contexte)

    print()
    print(f"=== SESSION PLANNING — {now} ===")
    print(" | ".join(ctx_parts))
    print(f"Tâches éligibles ({len(tasks)}) :")
    print()

    if not tasks:
        print("  Aucune tâche ne correspond à ce contexte.")
        print()
        print("  Conseils : élargir le support ou le pays, ou vérifier le Master Board.")
        return

    for i, t in enumerate(tasks, 1):
        nom = get_prop(t, "Nom de la tâche", "title") or "(sans titre)"
        prio = get_prop(t, "Priorité", "select") or ""
        dur = get_prop(t, "Durée", "select") or ""
        sup = ", ".join(get_prop(t, "Support", "multi_select") or [])
        ech = get_prop(t, "Échéance", "date") or ""
        details = " | ".join(x for x in [dur, prio, sup, ech] if x)
        print(f"{i}. {nom}  [{details}]")

    print()
    print(
        f">>> Construis un mini-agenda pour cette session.\n"
        f"    Budget total : {budget_str}.\n"
        f"    Règles :\n"
        f"    - Remplis le budget au maximum sans dépasser\n"
        f"    - Ajoute une pause de 10 min si la session dépasse 1h30\n"
        f"    - Ordre de priorité : Priorité > Durée courte > Échéance\n"
        f"    - Présente sous forme d'agenda avec les horaires (ex: 09:00 Tâche A — 30 min)\n"
        f"    - Si des tâches restent, liste-les en 'réserve' pour plus tard"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Session Planning interactif depuis le Master Board Notion"
    )
    parser.add_argument("--temps", metavar="DUREE", help="Ex: 3h, 45min, 1h30")
    parser.add_argument("--support", nargs="+", metavar="S", help="Ex: Téléphone 'PC Portable'")
    parser.add_argument("--pays", metavar="P", help="Ex: Thaïlande France Global")
    parser.add_argument("--context", metavar="TEXTE", help="Contexte libre additionnel")
    args = parser.parse_args()

    if args.temps:
        budget = parse_time(args.temps)
        if not budget:
            print(f"ERREUR : Durée non reconnue : {args.temps}", file=sys.stderr)
            sys.exit(1)
        supports = args.support
        pays = args.pays
        contexte = args.context or ""
    else:
        budget, supports, pays, contexte = prompt_interactif()

    print(f"\n[Notion] Connexion...", file=sys.stderr)
    notion = get_notion()
    all_tasks = fetch_all(notion)
    print(f"[Notion] {len(all_tasks)} tâches chargées.", file=sys.stderr)

    durees_ok = durees_dans_budget(budget)
    tasks = filter_and_sort(all_tasks, supports, durees_ok, pays)

    build_prompt(tasks, budget, supports, pays, contexte)


if __name__ == "__main__":
    main()
