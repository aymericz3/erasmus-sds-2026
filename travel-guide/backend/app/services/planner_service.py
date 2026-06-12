import math
import re

from app.core.planning_config import get_intensity_config, get_transport_speed


def _time_to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m

def _minutes_to_time(total: int) -> str:
    h = (total // 60) % 24
    m = total % 60
    return f"{h:02d}:{m:02d}"

def _parse_duration(duration: str) -> int:
    if not duration:
        return 60
    if "h" in duration and "min" in duration:
        parts = duration.split("h")
        return int(parts[0].strip()) * 60 + int(parts[1].replace("min", "").strip())
    if "h" in duration:
        return int(duration.split("h")[0].strip()) * 60
    if "min" in duration:
        return int(duration.split("min")[0].strip())
    return 60

def schedule_itinerary(places, total_minutes, start_time="09:00", break_duration_minutes=30, intensity="moderate"):
    plan = []
    elapsed = 0
    current = _time_to_minutes(start_time)
    is_relaxed = intensity == "relaxed"

    for place in places:
        duration_val = _parse_duration(place.duration)

        if is_relaxed and plan:
            current += break_duration_minutes
            elapsed += break_duration_minutes
            plan.append({
                "type": "break",
                "duration": break_duration_minutes,
                "start_at": _minutes_to_time(current - break_duration_minutes),
                "end_at": _minutes_to_time(current),
            })

        if elapsed + duration_val > total_minutes:
            break

        start_at = _minutes_to_time(current)
        current += duration_val
        elapsed += duration_val

        plan.append({
            "type": "attraction",
            "id": place.id,
            "name": place.name_en or place.name_pl,
            "duration": place.duration,
            "start_at": start_at,
            "end_at": _minutes_to_time(current),
        })

    return plan
  
def rank_attractions(places, selected_categories: list) -> list:
    if not selected_categories:
        return places

    ranked_places = []
    for place in places:
        weight = 0
        if place.category in selected_categories:
            weight = 100
        ranked_places.append((weight, place))

    ranked_places.sort(key=lambda x: x[0], reverse=True)
    return [p[1] for p in ranked_places]

# ---------------------------------------------------------------------------
# Multi-day planner
#
# Ported 1:1 from the frontend (utils.js -> buildDailyItinerary) so the backend
# produces results identical to the original client-side algorithm. Output uses
# the same field names as the frontend `days` structure (camelCase) so the
# frontend can swap its local call for a fetch with no shape changes.
# ---------------------------------------------------------------------------

def _duration_minutes(duration: str | None) -> int:
    """Parse 'Xh Ymin' / 'Xh' / 'Y min' into minutes. Empty -> 0 (matches JS)."""
    if not duration:
        return 0
    total = 0
    hours = re.search(r"(\d+)\s*h", duration)
    mins = re.search(r"(\d+)\s*min", duration)
    if hours:
        total += int(hours.group(1)) * 60
    if mins:
        total += int(mins.group(1))
    return total


def _js_round2(value: float) -> float:
    """Match JS Math.round(value * 100) / 100 (round half up)."""
    return math.floor(value * 100 + 0.5) / 100


def _haversine_km(a: dict | None, b: dict | None) -> float | None:
    if not a or not b:
        return None
    if a.get("latitude") is None or a.get("longitude") is None:
        return None
    if b.get("latitude") is None or b.get("longitude") is None:
        return None
    R = 6371
    lat1 = math.radians(a["latitude"])
    lat2 = math.radians(b["latitude"])
    d_lat = math.radians(b["latitude"] - a["latitude"])
    d_lon = math.radians(b["longitude"] - a["longitude"])
    h = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h))


def _haversine_minutes(a: dict | None, b: dict | None, speed_kmh: int = 5) -> int:
    """Straight-line travel minutes, rounded UP to the nearest 5 (matches JS)."""
    km = _haversine_km(a, b)
    if km is None:
        return 0
    raw = (km / speed_kmh) * 60
    return math.ceil(raw / 5) * 5


def _recalculate_item_times(items: list[dict], start_time: str) -> list[dict]:
    """Assign sequential start_at/end_at clock times to every item in a day."""
    current = _time_to_minutes(start_time)
    result = []
    for item in items:
        duration = (
            _duration_minutes(item.get("duration"))
            if item["type"] == "attraction"
            else item["duration"]
        )
        start_at = _minutes_to_time(current)
        current += duration
        end_at = _minutes_to_time(current)
        result.append({**item, "start_at": start_at, "end_at": end_at})
    return result


def _compute_day_items(attractions, travel_minutes, break_durations, start_time, travel_km=None):
    """Build the flat attraction/travel/break list for one day, with clock times."""
    travel_km = travel_km or []
    raw_items = []
    last_index = len(attractions) - 1
    for i, attr in enumerate(attractions):
        raw_items.append({"type": "attraction", **attr})
        if i < last_index:
            travel = travel_minutes[i] if i < len(travel_minutes) else 0
            raw_items.append({
                "type": "travel",
                "id": f"travel-{attr['id']}",
                "duration": travel,
                "gapIndex": i,
                "distanceKm": travel_km[i] if i < len(travel_km) else None,
            })
            break_dur = break_durations[i] if i < len(break_durations) else None
            if break_dur is not None:
                raw_items.append({
                    "type": "break",
                    "id": f"break-{attr['id']}",
                    "duration": break_dur,
                    "gapIndex": i,
                })
    return _recalculate_item_times(raw_items, start_time)


def place_to_attraction(place) -> dict:
    """Serialize a Place ORM row into the attraction dict the planner expects."""
    return {
        "id": place.id,
        "name_en": place.name_en,
        "name_pl": place.name_pl,
        "category": place.category,
        "description": place.description,
        "opening_hours": place.opening_hours,
        "duration": place.duration,
        "price_range": place.price_range,
        "image_url": place.image_url,
        "latitude": place.latitude,
        "longitude": place.longitude,
    }


def build_daily_itinerary(
    attractions: list[dict],
    num_days: int,
    intensity: str = "moderate",
    start_time: str = "09:00",
    break_duration_minutes: int = 30,
    transport_mode: str = "walking",
) -> dict:
    """
    Greedily pack ordered attractions into days under the intensity budget,
    inserting travel time and (for relaxed) breaks. Returns {"days", "overflow"}.
    """
    config = get_intensity_config(intensity)
    max_minutes = config["max_minutes_per_day"]
    max_attractions = config["max_attractions_per_day"]
    is_relaxed = intensity == "relaxed"
    speed = get_transport_speed(transport_mode)

    days = [
        {
            "attractions": [],
            "travelMinutes": [],
            "travelKm": [],
            "breakDurations": [],
            "items": [],
            "totalMinutes": 0,
        }
        for _ in range(num_days)
    ]
    overflow = []

    for attraction in attractions:
        duration = _duration_minutes(attraction.get("duration"))

        day_index = -1
        for idx, day in enumerate(days):
            last = day["attractions"][-1] if day["attractions"] else None
            travel = _haversine_minutes(last, attraction, speed) if last else 0
            break_overhead = break_duration_minutes if (is_relaxed and day["attractions"]) else 0
            fits_time = day["totalMinutes"] + travel + break_overhead + duration <= max_minutes
            fits_count = max_attractions is None or len(day["attractions"]) < max_attractions
            if fits_time and fits_count:
                day_index = idx
                break

        if day_index != -1:
            day = days[day_index]
            if day["attractions"]:
                last = day["attractions"][-1]
                travel = _haversine_minutes(last, attraction, speed)
                km = _haversine_km(last, attraction)
                day["travelMinutes"].append(travel)
                day["travelKm"].append(_js_round2(km) if km is not None else None)
                day["totalMinutes"] += travel
                day["breakDurations"].append(break_duration_minutes if is_relaxed else None)
                if is_relaxed:
                    day["totalMinutes"] += break_duration_minutes
            day["attractions"].append(attraction)
            day["totalMinutes"] += duration
        else:
            overflow.append(attraction)

    for day in days:
        day["items"] = _compute_day_items(
            day["attractions"],
            day["travelMinutes"],
            day["breakDurations"],
            start_time,
            day["travelKm"],
        )

    return {"days": days, "overflow": overflow}
