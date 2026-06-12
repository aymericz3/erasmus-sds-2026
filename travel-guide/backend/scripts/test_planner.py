"""
Terminal test for the multi-day itinerary planner — no frontend needed.

Usage (from backend/, with venv active):
    python scripts/test_planner.py --list
    python scripts/test_planner.py --ids 1,2,3,8,5,6,7 --days 2 --intensity relaxed
    python scripts/test_planner.py                      # default: first 6 places, 1 day

Options:
    --list                 show all places with id / duration / coords
    --ids 1,2,3            ordered place ids to plan (default: first 6)
    --days N               number of days (default 1)
    --intensity KEY        relaxed | moderate | intense (default moderate)
    --start HH:MM          daily start time (default 09:00)
    --break N              break minutes for relaxed days (default 30)
    --transport MODE       walking | cycling | transit (default walking)
"""

import argparse
import sys
from pathlib import Path

# Allow running as a plain script: add backend/ to the import path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal
from app.models.place import Place
from app.services.planner_service import build_daily_itinerary, place_to_attraction


def list_places(db):
    rows = db.query(Place).order_by(Place.id).all()
    print(f"\n{len(rows)} places:\n")
    for p in rows:
        name = p.name_en or p.name_pl
        print(f"  {p.id:>3}  {str(p.duration or '-'):<10}  "
              f"({p.latitude}, {p.longitude})  {name}")
    print()


def print_plan(plan):
    for i, day in enumerate(plan["days"]):
        print(f"\n=== Day {i + 1}  ·  {day['totalMinutes']} min total "
              f"({day['totalMinutes'] // 60}h {day['totalMinutes'] % 60:02d}m) ===")
        if not day["items"]:
            print("  (empty)")
            continue
        for item in day["items"]:
            t = item["type"]
            window = f"{item['start_at']}–{item['end_at']}"
            if t == "attraction":
                name = item.get("name_en") or item.get("name_pl")
                print(f"  {window}  📍 {name}  ({item.get('duration')})")
            elif t == "travel":
                if item["duration"] > 0:
                    dist = f" · {item['distanceKm']} km" if item["distanceKm"] is not None else ""
                    print(f"  {window}     ↳ travel {item['duration']} min{dist}")
            elif t == "break":
                print(f"  {window}     ☕ break {item['duration']} min")

    if plan["overflow"]:
        names = [a.get("name_en") or a.get("name_pl") for a in plan["overflow"]]
        print(f"\n⚠ Overflow (did not fit): {', '.join(names)}")
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--ids", type=str, default=None)
    parser.add_argument("--days", type=int, default=1)
    parser.add_argument("--intensity", type=str, default="moderate")
    parser.add_argument("--start", type=str, default="09:00")
    parser.add_argument("--break", dest="brk", type=int, default=30)
    parser.add_argument("--transport", type=str, default="walking")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        if args.list:
            list_places(db)
            return

        if args.ids:
            ids = [int(x) for x in args.ids.split(",") if x.strip()]
        else:
            ids = [p.id for p in db.query(Place).order_by(Place.id).limit(6).all()]

        places = db.query(Place).filter(Place.id.in_(ids)).all()
        by_id = {p.id: p for p in places}
        attractions = [place_to_attraction(by_id[i]) for i in ids if i in by_id]

        print(f"\nPlanning {len(attractions)} attractions over {args.days} day(s)  ·  "
              f"intensity={args.intensity}  start={args.start}  "
              f"transport={args.transport}  break={args.brk}min")

        plan = build_daily_itinerary(
            attractions,
            num_days=args.days,
            intensity=args.intensity,
            start_time=args.start,
            break_duration_minutes=args.brk,
            transport_mode=args.transport,
        )
        print_plan(plan)
    finally:
        db.close()


if __name__ == "__main__":
    main()
