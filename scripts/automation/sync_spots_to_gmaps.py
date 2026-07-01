#!/usr/bin/env python3
"""
sync_spots_to_gmaps.py — Notion Spots → Google Maps Saved Places (Playwright)

Pilote Chrome automatiquement pour sauvegarder chaque spot Notion dans tes
listes Google Maps personnelles. Aucune API officielle n'existe pour les
Saved Places — ce script conduit le navigateur à ta place.

─── SETUP (une seule fois) ───────────────────────────────────────────────────
  pip install playwright
  playwright install chromium         # ou utilise PLAYWRIGHT_BROWSERS_PATH

  # Exporte ta session Google (évite la 2FA à chaque run) :
  python scripts/automation/sync_spots_to_gmaps.py --setup

  → Un navigateur s'ouvre. Connecte-toi à ton compte Google.
    Ferme le navigateur quand Maps est chargé. Les cookies sont sauvegardés.

─── USAGE ────────────────────────────────────────────────────────────────────
  python scripts/automation/sync_spots_to_gmaps.py              # sync auto
  python scripts/automation/sync_spots_to_gmaps.py --dry-run    # aperçu seul
  python scripts/automation/sync_spots_to_gmaps.py --visible    # navigateur visible (debug)
  python scripts/automation/sync_spots_to_gmaps.py --all        # re-sync tous les spots

─── MAPPING DES LISTES GOOGLE MAPS ──────────────────────────────────────────
  Statut Notion       → Liste Google Maps
  ─────────────────────────────────────────
  À visiter           → "Vouloir y aller"    (liste intégrée)
  Favori              → "Favoris"            (liste intégrée)
  Visité              → "Lieux visités"      (liste intégrée)

  Personnalisable via GMAPS_LIST_* dans .env
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

# ─── Config ───────────────────────────────────────────────────────────────────

NOTION_TOKEN   = os.getenv("NOTION_TOKEN")
SPOTS_DB_ID    = os.getenv("SPOTS_DATABASE_ID", "70d0d3e6-8fba-4550-ae26-6f3edce40a18")
COOKIES_FILE   = Path(__file__).parent.parent.parent / ".gmaps_session.json"
SYNCED_FILE    = Path(__file__).parent.parent.parent / ".gmaps_synced.json"

# Noms des listes Google Maps (adapter si ton interface est en anglais)
LIST_A_VISITER = os.getenv("GMAPS_LIST_A_VISITER", "Vouloir y aller")
LIST_FAVORI    = os.getenv("GMAPS_LIST_FAVORI",    "Favoris")
LIST_VISITE    = os.getenv("GMAPS_LIST_VISITE",    "Lieux visités")

CHROMIUM_PATH  = os.getenv("PLAYWRIGHT_CHROMIUM_PATH", "/opt/pw-browsers/chromium")

STATUT_TO_LIST = {
    "À visiter": LIST_A_VISITER,
    "Favori":    LIST_FAVORI,
    "Visité":    LIST_VISITE,
}

DELAY_BETWEEN_SPOTS = 3  # secondes entre chaque spot (évite les throttles)


# ─── Notion helpers ───────────────────────────────────────────────────────────

def get_prop(page, name):
    props = page.get("properties", {})
    if name not in props:
        return None
    p = props[name]
    t = p.get("type")
    if t == "title":
        return "".join(r["plain_text"] for r in p.get("title", []))
    if t == "rich_text":
        return "".join(r["plain_text"] for r in p.get("rich_text", []))
    if t == "select":
        return (p.get("select") or {}).get("name")
    if t == "multi_select":
        return [o["name"] for o in p.get("multi_select", [])]
    if t == "number":
        return p.get("number")
    if t == "url":
        return p.get("url")
    return None


def fetch_spots(client, only_unsynced=True, synced_ids=None):
    results, cursor = [], None
    while True:
        resp = client.databases.query(database_id=SPOTS_DB_ID, page_size=100,
                                      **({"start_cursor": cursor} if cursor else {}))
        results.extend(resp["results"])
        if not resp.get("has_more"):
            break
        cursor = resp["next_cursor"]

    spots = []
    for page in results:
        pid   = page["id"]
        nom   = get_prop(page, "Nom") or "Sans nom"
        ville = get_prop(page, "Ville") or ""
        pays  = get_prop(page, "Pays") or ""
        statut = get_prop(page, "Statut") or "À visiter"
        gmap  = get_prop(page, "Google Maps") or ""

        # On ignore les spots déjà synced (sauf --all)
        if only_unsynced and synced_ids and pid in synced_ids:
            continue
        # On ignore les spots avec un vrai URL Maps (déjà résolu manuellement)
        if only_unsynced and gmap and "/maps/place/" in gmap:
            continue

        spots.append({"id": pid, "nom": nom, "ville": ville,
                      "pays": pays, "statut": statut, "gmap": gmap})
    return spots


def update_notion_gmap_url(client, page_id, url):
    try:
        client.pages.update(page_id, properties={"Google Maps": {"url": url}})
    except Exception as e:
        print(f"    ✗ Notion update failed: {e}")


# ─── Synced IDs cache ────────────────────────────────────────────────────────

def load_synced():
    if SYNCED_FILE.exists():
        return set(json.loads(SYNCED_FILE.read_text()))
    return set()


def save_synced(ids):
    SYNCED_FILE.write_text(json.dumps(list(ids), indent=2))


# ─── Playwright core ─────────────────────────────────────────────────────────

def launch_browser(playwright, headless=True):
    kwargs = {"headless": headless, "slow_mo": 300}
    # Utilise le Chromium système si disponible
    if Path(CHROMIUM_PATH).exists():
        kwargs["executable_path"] = CHROMIUM_PATH
    return playwright.chromium.launch(**kwargs)


def make_context(browser):
    """Crée un contexte avec les cookies de session s'ils existent."""
    if COOKIES_FILE.exists():
        state = json.loads(COOKIES_FILE.read_text())
        return browser.new_context(storage_state=state,
                                   locale="fr-FR",
                                   user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                                              "Chrome/120.0.0.0 Safari/537.36")
    return browser.new_context(locale="fr-FR")


def setup_session():
    """Ouvre un navigateur visible pour que l'utilisateur se connecte."""
    from playwright.sync_api import sync_playwright
    print("🔐 Setup — Connexion à Google Maps")
    print("   → Un navigateur va s'ouvrir. Connecte-toi à ton compte Google.")
    print("   → Quand Google Maps est chargé, ferme le navigateur.")
    print()

    with sync_playwright() as p:
        browser = launch_browser(p, headless=False)
        ctx = browser.new_context(locale="fr-FR")
        page = ctx.new_page()
        page.goto("https://www.google.com/maps")

        # Attendre que l'utilisateur ferme le navigateur
        try:
            while True:
                time.sleep(1)
        except Exception:
            pass
        finally:
            ctx.storage_state(path=str(COOKIES_FILE))
            browser.close()

    print(f"✅ Session sauvegardée dans {COOKIES_FILE}")
    print("   Tu peux maintenant lancer la sync sans --setup.")


def find_and_save_spot(page, spot, target_list, dry_run=False):
    """
    Navigue vers le spot dans Google Maps et le sauvegarde dans target_list.
    Retourne l'URL Maps réelle du spot si trouvé, None sinon.
    """
    nom, ville, pays = spot["nom"], spot["ville"], spot["pays"]
    query = f"{nom} {ville} {pays}".strip().replace(" ", "+")
    search_url = f"https://www.google.com/maps/search/{query}"

    print(f"   🔍 Recherche : {nom} ({ville or pays})")

    if dry_run:
        print(f"      [dry-run] Skippe → {search_url}")
        return None

    try:
        page.goto(search_url, wait_until="networkidle", timeout=20_000)
        page.wait_for_timeout(2000)

        # ── Cas 1 : résultat unique → la fiche s'ouvre directement ──
        # ── Cas 2 : liste de résultats → cliquer le premier ──────────
        first_result = page.locator('a[href*="/maps/place/"]').first
        if first_result.count() > 0:
            first_result.click()
            page.wait_for_timeout(2000)

        # ── Récupère l'URL réelle de la fiche ─────────────────────────
        real_url = page.url
        if "/maps/place/" not in real_url and "/maps/search/" in real_url:
            # Pas de fiche trouvée — peut-être sélectionner le 1er résultat
            print(f"      ⚠ Aucune fiche trouvée directement. Tentative résultats…")
            page.locator('[data-value="Résultats de la recherche"] a, [jsaction*="placeCard"] a').first.click()
            page.wait_for_timeout(2000)
            real_url = page.url

        if "/maps/place/" not in real_url:
            print(f"      ✗ Lieu introuvable sur Google Maps")
            return None

        print(f"      ✓ Fiche trouvée : {real_url[:80]}…")

        # ── Bouton Sauvegarder ────────────────────────────────────────
        save_btn = page.locator(
            'button[aria-label*="nregistrer"], '   # Enregistrer / sauvegarder
            'button[aria-label*="avoriser"], '     # Favoriser
            'button[data-value*="save"], '
            'button[jsaction*="save"]'
        ).first
        if not save_btn.is_visible(timeout=5000):
            # Fallback : chercher par icône SVG bookmark
            save_btn = page.locator('button[data-tab-index="0"]').nth(2)

        save_btn.click()
        page.wait_for_timeout(1500)

        # ── Sélectionner la liste ──────────────────────────────────────
        # Le dialog affiche les listes disponibles
        list_option = page.locator(f'div[aria-label*="{target_list}"], '
                                   f'span:text("{target_list}"), '
                                   f'li:has-text("{target_list}")').first
        if list_option.is_visible(timeout=5000):
            list_option.click()
            page.wait_for_timeout(1000)
            print(f"      ✅ Sauvegardé dans « {target_list} »")
        else:
            # Ferme le dialog et log l'erreur
            page.keyboard.press("Escape")
            print(f"      ⚠ Liste « {target_list} » introuvable — spot ouvert mais pas sauvegardé")
            print(f"         Vérifie le nom de la liste dans .env (GMAPS_LIST_*)")

        return real_url

    except Exception as e:
        print(f"      ✗ Erreur : {e}")
        return None


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Notion Spots → Google Maps Saved Places")
    parser.add_argument("--setup",    action="store_true", help="Exporter la session Google (à faire une fois)")
    parser.add_argument("--dry-run",  action="store_true", help="Aperçu sans rien sauvegarder")
    parser.add_argument("--visible",  action="store_true", help="Navigateur visible (debug)")
    parser.add_argument("--all",      action="store_true", help="Re-sync tous les spots (ignore le cache)")
    args = parser.parse_args()

    if args.setup:
        setup_session()
        return

    if not NOTION_TOKEN:
        print("❌ NOTION_TOKEN non configuré dans .env")
        sys.exit(1)

    if not COOKIES_FILE.exists() and not args.dry_run:
        print("❌ Pas de session Google sauvegardée.")
        print("   Lance d'abord : python scripts/automation/sync_spots_to_gmaps.py --setup")
        sys.exit(1)

    client  = Client(auth=NOTION_TOKEN)
    synced  = load_synced()
    spots   = fetch_spots(client, only_unsynced=not args.all, synced_ids=synced)

    if not spots:
        print("✅ Tous les spots sont déjà synchronisés avec Google Maps.")
        return

    print(f"📋 {len(spots)} spot(s) à synchroniser\n")

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = launch_browser(p, headless=not args.visible)
        ctx     = make_context(browser)
        page    = ctx.new_page()

        # Vérifie que la session est valide
        page.goto("https://www.google.com/maps", wait_until="networkidle", timeout=20_000)
        if "accounts.google.com" in page.url:
            browser.close()
            print("❌ Session expirée. Relance avec --setup pour te reconnecter.")
            sys.exit(1)

        ok, fail = 0, 0
        for spot in spots:
            target_list = STATUT_TO_LIST.get(spot["statut"], LIST_A_VISITER)
            real_url    = find_and_save_spot(page, spot, target_list, dry_run=args.dry_run)

            if real_url and not args.dry_run:
                update_notion_gmap_url(client, spot["id"], real_url)
                synced.add(spot["id"])
                save_synced(synced)
                ok += 1
            elif not real_url and not args.dry_run:
                fail += 1

            time.sleep(DELAY_BETWEEN_SPOTS)

        ctx.storage_state(path=str(COOKIES_FILE))  # rafraîchit les cookies
        browser.close()

    print(f"\n{'─'*50}")
    print(f"✅ {ok} spot(s) sauvegardés dans Google Maps")
    if fail:
        print(f"⚠  {fail} spot(s) introuvables — ajoute l'URL Google Maps manuellement dans Notion")
    print(f"\n📌 Pour mettre à jour la carte My Maps :")
    print(f"   python scripts/automation/sync_spots_to_kml.py --output spots.kml")


if __name__ == "__main__":
    main()
