"""
Build the places table from scripts/poznan_places.py (101 curated places) enriched
with OpenStreetMap (Nominatim) + Wikipedia data.

For each place the source provides name + category + description. This script adds:
    - OSM:        latitude, longitude, address, opening_hours, website, osm_id
    - Wikipedia:  description (upgraded), image_url, image_attribution, wikipedia_title
    - defaults:   duration and price_range by category (planner needs duration)

Matching: each place is searched by its English and Polish names; only results
inside the Poznań region bounding box are accepted (rejects same-name hits
elsewhere). Responses are cached to scripts/.enrich_cache.json so re-runs are fast.

Usage (from backend/, venv active):
    python scripts/enrich_places.py              # PREVIEW: fetch + report coverage, no DB writes
    python scripts/enrich_places.py --limit 10   # preview first 10 only
    python scripts/enrich_places.py --apply       # REPLACE the places table with enriched rows

Then regenerate the committed seed:
    python scripts/dump_seed.py

Etiquette: Nominatim allows <= 1 req/sec with a descriptive User-Agent.
"""

import argparse
import json
import sys
import time
import urllib.parse
from pathlib import Path

import requests
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parent))        # for poznan_places
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))    # for app.*

from poznan_places import PLACES
from app.db.session import SessionLocal
from app.models.place import Place

USER_AGENT = "erasmus-sds-2026-travel-guide/1.0 (educational project)"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
WIKIPEDIA_SUMMARY = "https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
WIKIDATA_ENTITY = "https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

NOMINATIM_DELAY = 1.1
WIKI_DELAY = 0.6
CACHE_FILE = Path(__file__).resolve().parent / ".enrich_cache.json"

# Poznań + day-trip region (Kórnik, Rogalin, Morasko fall inside this box).
REGION = (52.00, 52.75, 16.45, 17.45)  # lat_min, lat_max, lon_min, lon_max

# Visit duration the planner schedules per category, and a rough price band.
DURATION_BY_CATEGORY = {
    "landmark": "45 min", "culture": "1h 30min", "art": "1h", "outdoor": "1h 30min",
    "family": "2h", "sport": "1h 30min", "food": "1h 30min", "hotel": "1h",
}
PRICE_BY_CATEGORY = {
    "landmark": "free", "outdoor": "free", "culture": "€", "art": "€",
    "family": "€€", "sport": "€", "food": "€€", "hotel": "€€€",
}

ENRICHMENT_COLUMNS = ["address", "website", "osm_id", "wikipedia_title",
                      "image_attribution", "source"]

# Exact OSM search strings for notable places whose English name doesn't resolve.
# These are used verbatim (no ", Poznań, Poland" suffix), so day-trip towns work.
OSM_QUERY_OVERRIDES = {
    "Archcathedral Basilica of St. Peter and St. Paul": "Katedra Poznańska",
    "Museum of Musical Instruments": "Muzeum Instrumentów Muzycznych Poznań",
    "Stary Browar Art Stations": "Stary Browar Poznań",
    "Śródka Mural": "Mural Śródka Poznań",
    "Kórnik Arboretum & Castle": "Zamek w Kórniku",
    "Rogalin Palace & Oaks": "Pałac w Rogalinie",
    "Greater Poland Military Museum": "Wielkopolskie Muzeum Wojskowe Poznań",
    "Genius Loci Archaeological Reserve": "Rezerwat Archeologiczny Genius Loci Poznań",
    "Maltanka Park Railway": "Kolejka Parkowa Maltanka Poznań",
    "Morasko Meteorite Reserve": "Rezerwat przyrody Meteoryt Morasko",
    "Sheraton Poznań Hotel": "Sheraton Poznań",
    "Mercure Poznań Centrum": "Mercure Poznań Centrum",
}

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "en,pl"})
_cache = json.loads(CACHE_FILE.read_text(encoding="utf-8")) if CACHE_FILE.exists() else {}


def _cached(key, producer):
    if key in _cache:
        return _cache[key]
    value = producer()
    _cache[key] = value
    CACHE_FILE.write_text(json.dumps(_cache, ensure_ascii=False, indent=2), encoding="utf-8")
    return value


def _get_json(url, params=None, retries=4):
    """GET JSON with exponential backoff on rate-limit / transient errors."""
    for attempt in range(retries):
        try:
            r = session.get(url, params=params, timeout=20)
            if r.status_code in (429, 503):
                wait = 2 ** attempt + 1
                print(f"    … {r.status_code} rate-limited, backing off {wait}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError) as exc:
            print(f"    ! request failed: {exc}")
            return None
    print("    ! gave up after retries")
    return None


# --------------------------------------------------------------------------- #
# Parsing the source names
# --------------------------------------------------------------------------- #

def split_name(full: str) -> tuple[str, str | None]:
    """'Old Market Square (Stary Rynek)' -> ('Old Market Square', 'Stary Rynek')."""
    if "(" in full and ")" in full:
        en = full[: full.index("(")].strip()
        pl = full[full.index("(") + 1: full.rindex(")")].strip()
        return en or full.strip(), (pl or None)
    return full.strip(), None


def _in_region(lat: float, lon: float) -> bool:
    return REGION[0] <= lat <= REGION[1] and REGION[2] <= lon <= REGION[3]


# --------------------------------------------------------------------------- #
# OpenStreetMap
# --------------------------------------------------------------------------- #

def nominatim_lookup(names: list[str], exact_query: str | None = None) -> dict | None:
    """Try each name; return the first in-region hit, preferring wiki-tagged ones."""
    queries = [exact_query] if exact_query else [f"{n}, Poznań, Poland" for n in names if n]

    def _do():
        collected = []
        for q in queries:
            data = _get_json(NOMINATIM_URL, {
                "q": q, "format": "jsonv2",
                "addressdetails": 1, "extratags": 1, "limit": 5,
            })
            time.sleep(NOMINATIM_DELAY)
            for hit in (data or []):
                if _in_region(float(hit["lat"]), float(hit["lon"])):
                    collected.append(hit)
            if collected:  # stop at the first name that yields a local match
                break
        if not collected:
            return None
        collected.sort(key=lambda h: 0 if (h.get("extratags") or {}).get("wikidata") else 1)
        hit = collected[0]
        extra = hit.get("extratags") or {}
        addr = hit.get("address") or {}
        road = " ".join(p for p in (addr.get("road", ""), addr.get("house_number", "")) if p).strip()
        readable = ", ".join(p for p in (
            road, addr.get("postcode", ""),
            addr.get("city") or addr.get("town") or addr.get("village", ""),
            addr.get("country", ""),
        ) if p)
        return {
            "latitude": float(hit["lat"]),
            "longitude": float(hit["lon"]),
            "address": readable or hit.get("display_name", ""),
            "opening_hours": extra.get("opening_hours", ""),
            "website": extra.get("website") or extra.get("contact:website", ""),
            "osm_id": f"{hit.get('osm_type')}/{hit.get('osm_id')}",
            "wikidata": extra.get("wikidata", ""),
            "wikipedia": extra.get("wikipedia", ""),
        }
    return _cached("osm::" + "|".join(queries), _do)


# --------------------------------------------------------------------------- #
# Wikipedia / Wikidata / Commons
# --------------------------------------------------------------------------- #

def _commons_filename(src: str | None) -> str | None:
    """Extract the Commons file name from any upload.wikimedia.org URL."""
    if not src:
        return None
    parts = src.split("/")
    name = parts[-2] if "thumb" in parts else parts[-1]
    return name.split("?")[0]


def _commons_image_url(filename: str, width: int = 1024) -> str:
    """Special:FilePath redirect — always serves a valid thumbnail capped at the
    original width (direct /<W>px- thumbnail URLs 400 for some files)."""
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{filename}?width={width}"


def wikipedia_summary(lang: str, title: str) -> dict:
    def _do():
        enc = urllib.parse.quote(title.replace(" ", "_"), safe="")
        data = _get_json(WIKIPEDIA_SUMMARY.format(lang=lang, title=enc))
        time.sleep(WIKI_DELAY)
        if not data:
            return {}
        src = (data.get("originalimage") or data.get("thumbnail") or {}).get("source")
        filename = _commons_filename(src)
        return {
            "description": data.get("extract", ""),
            "image_url": _commons_image_url(filename) if filename else None,
            "image_filename": filename,
            "wikipedia_title": f"{lang}:{title}",
        }
    return _cached(f"wiki::{lang}:{title}", _do)


def wikidata_to_wikipedia(qid: str) -> tuple[str, str] | None:
    def _do():
        data = _get_json(WIKIDATA_ENTITY.format(qid=qid))
        time.sleep(WIKI_DELAY)
        links = (data or {}).get("entities", {}).get(qid, {}).get("sitelinks", {})
        for wiki in ("enwiki", "plwiki"):
            if wiki in links:
                return [wiki.replace("wiki", ""), links[wiki]["title"]]
        return None
    return _cached(f"wd::{qid}", _do)


def wikimedia_attribution(filename: str) -> str:
    def _do():
        import re
        data = _get_json(COMMONS_API, {
            "action": "query", "titles": f"File:{urllib.parse.unquote(filename)}",
            "prop": "imageinfo", "iiprop": "extmetadata", "format": "json",
        })
        time.sleep(WIKI_DELAY)
        try:
            meta = next(iter(data["query"]["pages"].values()))["imageinfo"][0]["extmetadata"]
            artist = re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip()
            lic = meta.get("LicenseShortName", {}).get("value", "").strip()
            bits = [b for b in (artist, lic) if b]
            return f"{' · '.join(bits)} (via Wikimedia Commons)" if bits else "via Wikimedia Commons"
        except Exception:
            return "via Wikimedia Commons"
    return _cached(f"attr::{filename}", _do)


def resolve_wikipedia(osm: dict) -> dict:
    """Prefer the wikidata tag (lets us pick English), fall back to the wikipedia tag."""
    ref = None
    if osm.get("wikidata"):
        ref = wikidata_to_wikipedia(osm["wikidata"])
    if not ref and osm.get("wikipedia") and ":" in osm["wikipedia"]:
        lang, title = osm["wikipedia"].split(":", 1)
        ref = [lang.strip(), title.strip()]
    if not ref:
        return {}
    summary = wikipedia_summary(ref[0], ref[1])
    if summary.get("image_url"):
        summary["image_attribution"] = wikimedia_attribution(summary["image_filename"])
    return summary


# --------------------------------------------------------------------------- #
# Build one enriched record
# --------------------------------------------------------------------------- #

def build_record(place: dict) -> dict:
    name_en, name_pl = split_name(place["name"])
    osm = nominatim_lookup([name_en, name_pl], OSM_QUERY_OVERRIDES.get(name_en)) or {}
    wiki = resolve_wikipedia(osm) if osm else {}
    category = place["category"]

    return {
        "name_en": name_en,
        "name_pl": name_pl,
        "category": category,
        # Wikipedia description upgrades the source blurb when available.
        "description": wiki.get("description") or place["description"],
        "opening_hours": osm.get("opening_hours") or None,
        "duration": DURATION_BY_CATEGORY.get(category),
        "price_range": PRICE_BY_CATEGORY.get(category),
        "image_url": wiki.get("image_url") or None,
        "latitude": osm.get("latitude"),
        "longitude": osm.get("longitude"),
        "address": osm.get("address") or None,
        "website": osm.get("website") or None,
        "osm_id": osm.get("osm_id") or None,
        "wikipedia_title": wiki.get("wikipedia_title") or None,
        "image_attribution": wiki.get("image_attribution") or None,
        "source": "osm+wikipedia",
    }


# --------------------------------------------------------------------------- #
# DB write
# --------------------------------------------------------------------------- #

def ensure_columns(db):
    for col in ENRICHMENT_COLUMNS:
        db.execute(text(f"ALTER TABLE places ADD COLUMN IF NOT EXISTS {col} TEXT"))
    db.commit()


def replace_places(db, records: list[dict]):
    ensure_columns(db)
    db.execute(text("DELETE FROM places"))
    db.execute(text("ALTER SEQUENCE places_id_seq RESTART WITH 1"))
    for rec in records:
        db.add(Place(**rec))
    db.commit()


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="replace the places table")
    parser.add_argument("--limit", type=int, default=None, help="only process the first N")
    args = parser.parse_args()

    source = PLACES[: args.limit] if args.limit else PLACES
    mode = "APPLY — table will be replaced" if args.apply else "PREVIEW — no DB writes"
    print(f"\n{mode}. Enriching {len(source)} places from OSM + Wikipedia...\n")

    records, no_coords, no_image = [], [], []
    for i, place in enumerate(source, 1):
        rec = build_record(place)
        records.append(rec)
        mark = "📍" if rec["latitude"] is not None else "  "
        img = "🖼" if rec["image_url"] else "  "
        if rec["latitude"] is None:
            no_coords.append(rec["name_en"])
        if not rec["image_url"]:
            no_image.append(rec["name_en"])
        print(f"  [{i:>3}/{len(source)}] {mark}{img} {rec['name_en']}")

    print(f"\n— Coverage: {len(records)} places · "
          f"{len(records) - len(no_coords)} with coords · "
          f"{len(records) - len(no_image)} with image —")
    if no_coords:
        print(f"\nNo coordinates ({len(no_coords)}): {', '.join(no_coords)}")

    if args.apply:
        db = SessionLocal()
        try:
            placed = [r for r in records if r["latitude"] is not None]
            print(f"\nWriting {len(placed)} located places (skipping {len(no_coords)} without coords)...")
            replace_places(db, placed)
            print("Done. Now run: python scripts/dump_seed.py")
        finally:
            db.close()


if __name__ == "__main__":
    main()
