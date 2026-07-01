#!/usr/bin/env python3
"""
sync_spots_to_kml.py — Notion Spots → KML (Google My Maps)

Reads spots from the Notion Spots database, geocodes them via Nominatim
(free, no API key), and writes a .kml file importable into Google My Maps
with pins organized by type and colored accordingly.

Usage:
  python scripts/automation/sync_spots_to_kml.py
  python scripts/automation/sync_spots_to_kml.py --output spots.kml
  python scripts/automation/sync_spots_to_kml.py --status "À visiter"
  python scripts/automation/sync_spots_to_kml.py --pays Thaïlande
  python scripts/automation/sync_spots_to_kml.py --update-notion

Options:
  --output FILE        Output KML file (default: spots.kml)
  --status STATUT      Filter: À visiter / Visité / Favori / Fermé
  --pays PAYS          Filter: France / Thaïlande / Vietnam / …
  --update-notion      Fill Google Maps search URLs in Notion for spots missing them
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

from notion_client import Client
from dotenv import load_dotenv

try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderServiceError
    HAS_GEOPY = True
except ImportError:
    HAS_GEOPY = False
    print("⚠ geopy not installed — run: pip install geopy")

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
SPOTS_DB_ID = os.getenv("SPOTS_DATABASE_ID", "70d0d3e6-8fba-4550-ae26-6f3edce40a18")
GEOCODE_CACHE_FILE = Path(__file__).parent.parent.parent / ".geocode_cache.json"

# Pin icons per type — Google Maps dot icons (work in My Maps import)
TYPE_ICONS = {
    "Restaurant": "https://maps.google.com/mapfiles/ms/icons/orange-dot.png",
    "Bar":        "https://maps.google.com/mapfiles/ms/icons/purple-dot.png",
    "Activité":   "https://maps.google.com/mapfiles/ms/icons/blue-dot.png",
    "Hôtel":      "https://maps.google.com/mapfiles/ms/icons/green-dot.png",
    "Coffee Shop":"https://maps.google.com/mapfiles/ms/icons/yellow-dot.png",
    "Weed Shop":  "https://maps.google.com/mapfiles/ms/icons/ltblue-dot.png",
    "Lounge":     "https://maps.google.com/mapfiles/ms/icons/pink-dot.png",
    "Brunch":     "https://maps.google.com/mapfiles/ms/icons/red-dot.png",
    "Spa":        "https://maps.google.com/mapfiles/ms/icons/yellow-dot.png",
    "Favori":     "https://maps.google.com/mapfiles/ms/icons/red-pushpin.png",
}

TYPE_ORDER = ["Restaurant", "Bar", "Activité", "Hôtel", "Coffee Shop", "Weed Shop", "Lounge", "Brunch", "Spa"]

EMOJI_MAP = {
    "Restaurant": "🍽️", "Bar": "🍹", "Activité": "🏛️", "Hôtel": "🏨",
    "Coffee Shop": "☕", "Weed Shop": "🌿", "Lounge": "🛋️", "Brunch": "🍳", "Spa": "💆",
}

# Style ID must be ASCII for KML
TYPE_STYLE_ID = {
    "Restaurant": "restaurant", "Bar": "bar", "Activité": "activite",
    "Hôtel": "hotel", "Coffee Shop": "coffee_shop", "Weed Shop": "weed_shop",
    "Lounge": "lounge", "Brunch": "brunch", "Spa": "spa",
}


# ─── Geocoding ────────────────────────────────────────────────────────────────

def load_cache():
    if GEOCODE_CACHE_FILE.exists():
        return json.loads(GEOCODE_CACHE_FILE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache):
    GEOCODE_CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")


def geocode(name, ville, pays, cache):
    """Returns [lat, lon] or None. Caches results to avoid re-querying."""
    key = f"{name}||{ville}||{pays}"
    if key in cache:
        return cache[key]

    if not HAS_GEOPY:
        return None

    geolocator = Nominatim(user_agent="automatisation-ultime-spots/1.0 (personal use)")
    queries = [
        f"{name}, {ville}, {pays}",
        f"{name}, {pays}",
        f"{ville}, {pays}",
    ]

    for query in queries:
        try:
            time.sleep(1.2)  # Nominatim ToS: max 1 req/sec
            loc = geolocator.geocode(query, timeout=10)
            if loc:
                result = [loc.latitude, loc.longitude]
                cache[key] = result
                save_cache(cache)
                return result
        except (GeocoderTimedOut, GeocoderServiceError):
            continue

    cache[key] = None
    save_cache(cache)
    return None


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


def fetch_all_spots(client, extra_filter=None):
    results, cursor = [], None
    while True:
        kwargs = {"database_id": SPOTS_DB_ID, "page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor
        if extra_filter:
            kwargs["filter"] = extra_filter
        resp = client.databases.query(**kwargs)
        results.extend(resp["results"])
        if not resp.get("has_more"):
            break
        cursor = resp["next_cursor"]
    return results


# ─── KML builder ──────────────────────────────────────────────────────────────

def _style(doc, sid, icon_url):
    s = SubElement(doc, "Style", id=sid)
    icon_style = SubElement(s, "IconStyle")
    icon = SubElement(icon_style, "Icon")
    SubElement(icon, "href").text = icon_url


def _placemark(folder, spot, style_id):
    if not spot.get("coords"):
        return
    pm = SubElement(folder, "Placemark")
    SubElement(pm, "name").text = spot["nom"]
    SubElement(pm, "description").text = _description(spot)
    SubElement(pm, "styleUrl").text = f"#{style_id}"
    pt = SubElement(pm, "Point")
    lat, lon = spot["coords"]
    SubElement(pt, "coordinates").text = f"{lon},{lat},0"


def _description(s):
    lines = []
    if s.get("note"):
        lines.append(f"⭐ Note : {s['note']}/10")
    if s.get("statut"):
        lines.append(f"📌 {s['statut']}")
    if s.get("prix"):
        lines.append(f"💰 {s['prix']}")
    if s.get("ambiance"):
        lines.append(f"🎭 {', '.join(s['ambiance'])}")
    if s.get("commentaire"):
        lines.append("")
        lines.append(s["commentaire"])
    if s.get("ville"):
        lines.append("")
        lines.append(f"📍 {s['ville']}, {s.get('pays', '')}")
    return "\n".join(lines)


def build_kml(spots_by_type, favoris):
    kml = Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = SubElement(kml, "Document")
    SubElement(doc, "name").text = "Spots — Franck Savin"
    SubElement(doc, "description").text = "Carte personnelle générée depuis Notion. Mise à jour via sync_spots_to_kml.py"

    # Register styles
    for type_name, sid in TYPE_STYLE_ID.items():
        _style(doc, sid, TYPE_ICONS[type_name])
    _style(doc, "favori", TYPE_ICONS["Favori"])

    # ⭐ Favoris folder first
    if favoris:
        folder = SubElement(doc, "Folder")
        SubElement(folder, "name").text = "⭐ Favoris"
        for spot in favoris:
            _placemark(folder, spot, "favori")

    # One folder per type
    for type_name in TYPE_ORDER:
        spots = spots_by_type.get(type_name, [])
        if not spots:
            continue
        folder = SubElement(doc, "Folder")
        emoji = EMOJI_MAP.get(type_name, "📍")
        SubElement(folder, "name").text = f"{emoji} {type_name}s"
        sid = TYPE_STYLE_ID.get(type_name, "activite")
        for spot in spots:
            _placemark(folder, spot, sid)

    raw = tostring(kml, encoding="unicode")
    return parseString(raw).toprettyxml(indent="  ")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Notion Spots → KML for Google My Maps")
    parser.add_argument("--output", default="spots.kml", help="Output KML file")
    parser.add_argument("--status", help="Filter by Statut")
    parser.add_argument("--pays", help="Filter by Pays")
    parser.add_argument("--update-notion", action="store_true",
                        help="Fill Google Maps search URLs in Notion for spots missing them")
    args = parser.parse_args()

    if not NOTION_TOKEN:
        print("❌ NOTION_TOKEN not set in .env — copy .env.example to .env and fill it")
        sys.exit(1)

    client = Client(auth=NOTION_TOKEN)

    # Build Notion filter
    conditions = []
    if args.status:
        conditions.append({"property": "Statut", "select": {"equals": args.status}})
    if args.pays:
        conditions.append({"property": "Pays", "select": {"equals": args.pays}})
    notion_filter = None
    if len(conditions) == 1:
        notion_filter = conditions[0]
    elif conditions:
        notion_filter = {"and": conditions}

    print("📥 Fetching spots from Notion...")
    pages = fetch_all_spots(client, notion_filter)
    print(f"   → {len(pages)} spots trouvés")

    cache = load_cache()
    spots = []

    for page in pages:
        nom = get_prop(page, "Nom") or "Sans nom"
        types = get_prop(page, "Type") or []
        statut = get_prop(page, "Statut") or "À visiter"
        pays = get_prop(page, "Pays") or ""
        ville = get_prop(page, "Ville") or ""
        prix = get_prop(page, "Prix") or ""
        ambiance = get_prop(page, "Ambiance") or []
        note = get_prop(page, "Note")
        commentaire = get_prop(page, "Commentaire") or ""
        gmap_url = get_prop(page, "Google Maps") or ""

        print(f"   📍 Geocoding : {nom} ({ville or pays})...", end=" ", flush=True)
        coords = geocode(nom, ville, pays, cache)
        print("✓" if coords else "✗ non trouvé")

        spot = {
            "id": page["id"],
            "nom": nom, "types": types, "statut": statut,
            "pays": pays, "ville": ville, "prix": prix,
            "ambiance": ambiance, "note": note,
            "commentaire": commentaire, "gmap_url": gmap_url,
            "coords": coords,
        }
        spots.append(spot)

        # Optionally fill Google Maps search URL in Notion
        if args.update_notion and not gmap_url and coords:
            query = f"{nom} {ville} {pays}".replace(" ", "+")
            new_url = f"https://www.google.com/maps/search/?api=1&query={query}"
            try:
                client.pages.update(page["id"], properties={"Google Maps": {"url": new_url}})
                print(f"        ✓ URL Google Maps mise à jour dans Notion")
            except Exception as e:
                print(f"        ✗ Erreur Notion : {e}")

    # Organise by primary type + favoris
    spots_by_type = {t: [] for t in TYPE_ORDER}
    favoris = []
    no_coords = 0

    for spot in spots:
        if not spot["coords"]:
            no_coords += 1
            continue
        if spot["statut"] == "Favori":
            favoris.append(spot)
        primary = spot["types"][0] if spot["types"] else "Activité"
        if primary in spots_by_type:
            spots_by_type[primary].append(spot)

    total_pins = sum(len(v) for v in spots_by_type.values())
    print(f"\n✍️  Génération KML : {total_pins} pins ({no_coords} spots sans coordonnées ignorés)...")

    kml_content = build_kml(spots_by_type, favoris)
    out = Path(args.output)
    out.write_text(kml_content, encoding="utf-8")

    print(f"✅ KML écrit : {out.absolute()}")
    print(f"\n📌 Pour importer dans Google My Maps :")
    print(f"   1. Ouvre https://mymaps.google.com")
    print(f"   2. Clique 'Créer une nouvelle carte'")
    print(f"   3. Clique 'Importer' → uploade {out.name}")
    print(f"   4. Les {total_pins} spots apparaissent avec des pins colorés par catégorie")
    if no_coords:
        print(f"\n⚠ {no_coords} spots sans coordonnées (geocoding échoué) — ajoute l'URL Google Maps dans Notion pour les inclure")


if __name__ == "__main__":
    main()
