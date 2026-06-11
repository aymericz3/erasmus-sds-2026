"""
Terminal test script for the transport service.

Usage (from travel-guide/backend/):
    source .venv/bin/activate
    python scripts/test_transport.py

Optionally test a specific pair by index:
    python scripts/test_transport.py --pair 0 2
"""

import sys
import os
import argparse

# Allow importing from the app package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import get_db
from app.models.place import Place
from app.services.transport_service import get_travel_times
from app.core.config import settings

ICONS = {"walking": "🚶", "cycling": "🚲", "driving": "🚗", "tram": "🚋"}
SEPARATOR = "─" * 60


def fmt(mode_data: dict) -> str:
    src = "~est" if mode_data["source"] == "estimate" else "  "
    return f"{mode_data['minutes']:>3} min  {mode_data['distance_km']:>5.1f} km  {src}"


def run_pair(a, b):
    print(f"\n  {a.name_en or a.name_pl}")
    print(f"  → {b.name_en or b.name_pl}")
    print(f"  ({a.latitude:.4f},{a.longitude:.4f}) → ({b.latitude:.4f},{b.longitude:.4f})")
    print()

    times = get_travel_times(a.latitude, a.longitude, b.latitude, b.longitude)
    for mode, icon in ICONS.items():
        data = times[mode]
        print(f"  {icon}  {mode:<8}  {fmt(data)}")


def main():
    parser = argparse.ArgumentParser(description="Test transport travel times between attractions")
    parser.add_argument("--pair", nargs=2, type=int, metavar=("FROM", "TO"),
                        help="Test a specific pair by DB row index (0-based)")
    parser.add_argument("--list", action="store_true", help="List all attractions with indices")
    args = parser.parse_args()

    api_configured = settings.google_maps_api_key and settings.google_maps_api_key != "your_key_here"

    print(SEPARATOR)
    print("  Transport Service Test")
    print(f"  Google API: {'✅ configured' if api_configured else '⚠️  not set — using Haversine estimates'}")
    print(SEPARATOR)

    db = next(get_db())
    places = db.query(Place).filter(Place.latitude.isnot(None), Place.longitude.isnot(None)).all()

    if not places:
        print("  ❌ No places with coordinates found in DB.")
        return

    if args.list:
        print("\n  Attractions with coordinates:\n")
        for i, p in enumerate(places):
            print(f"  [{i:2}]  {p.name_en or p.name_pl:<35} ({p.latitude:.4f}, {p.longitude:.4f})")
        print()
        return

    if args.pair:
        i, j = args.pair
        if i >= len(places) or j >= len(places):
            print(f"  ❌ Index out of range. Max index: {len(places) - 1}")
            return
        print(SEPARATOR)
        run_pair(places[i], places[j])
        print()
        return

    # Default: test all consecutive pairs
    print(f"\n  Testing {len(places) - 1} consecutive pairs ({len(places)} attractions)\n")
    for i in range(len(places) - 1):
        print(SEPARATOR)
        run_pair(places[i], places[i + 1])

    print(f"\n{SEPARATOR}")
    print("  Done.")
    if not api_configured:
        print("  Tip: set GOOGLE_MAPS_API_KEY in .env to get real times from Google.")
    print(SEPARATOR)


if __name__ == "__main__":
    main()
