"""
planner_service.py — all itinerary scheduling logic.

There are two generations of planners in this file:

  GENERATION 1 (Sprint 1 / obsolete)
    schedule_itinerary  →  used by POST /itinerary/plan
    Simple single-day greedy scheduler. No travel time, no multi-day.
    Will be removed when /plan is dropped.

  GENERATION 2 (Sprint 2 I3 / to be replaced)
    build_daily_itinerary  →  used by POST /itinerary/generate
    Multi-day greedy packer ported 1:1 from the frontend (utils.js).
    Respects the place_ids order sent by the client.
    Will be removed when the frontend switches to /plan-optimized.

  GENERATION 3 (current / active development)
    build_optimized_itinerary  →  used by POST /itinerary/plan-optimized
    Same greedy packer but backend-driven: per-day time windows, per-day
    intensity overrides, anchor-based routing, and route optimisation.
    Steps being added incrementally (see endpoints/itinerary.py for the list).

All three generations share the same set of private helpers (_haversine_km,
_compute_day_items, etc.) defined below.
"""

import math
import re

from app.core.planning_config import get_intensity_config, get_transport_speed


# ---------------------------------------------------------------------------
# Time helpers — used by all three generations
# ---------------------------------------------------------------------------

def _time_to_minutes(t: str) -> int:
    # "HH:MM" → total minutes from midnight. e.g. "09:30" → 570
    h, m = map(int, t.split(":"))
    return h * 60 + m

def _minutes_to_time(total: int) -> str:
    # Total minutes from midnight → "HH:MM". Wraps at 24h.
    h = (total // 60) % 24
    m = total % 60
    return f"{h:02d}:{m:02d}"


# ---------------------------------------------------------------------------
# Generation 1 helpers — only used by schedule_itinerary / POST /plan
# ---------------------------------------------------------------------------

def _parse_duration(duration: str) -> int:
    # Parses "Xh Ymin" / "Xh" / "Ymin" → minutes. Defaults to 60 if empty.
    # Used only by the old schedule_itinerary; Generation 2+ uses _duration_minutes.
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


# ---------------------------------------------------------------------------
# GENERATION 1 — obsolete, kept until POST /itinerary/plan is removed
# ---------------------------------------------------------------------------

def schedule_itinerary(places, total_minutes, start_time="09:00", break_duration_minutes=30, intensity="moderate"):
    """
    Single-day greedy scheduler (Sprint 1).
    Iterates places in the given order and stops when total_minutes is exhausted.
    No travel time between places. Inserts breaks only in relaxed mode.
    """
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

    if not plan and places:
        for place in places:
            duration_val = _parse_duration(place.duration)
            if duration_val <= total_minutes:
                start_at = _minutes_to_time(current)
                current += duration_val
                plan.append({
                    "type": "attraction",
                    "id": place.id,
                    "name": place.name_en or place.name_pl,
                    "duration": place.duration,
                    "start_at": start_at,
                    "end_at": _minutes_to_time(current),
                })
                break

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
# Shared helpers — used by Generation 2 and Generation 3
# ---------------------------------------------------------------------------

def _duration_minutes(duration: str | None) -> int:
    """
    Parse 'Xh Ymin' / 'Xh' / 'Ymin' into minutes. Returns 0 if empty.
    Differs from _parse_duration (Gen 1) which defaults to 60 — this matches
    the JS behaviour (parseDurationToMinutes returns 0 for empty).
    """
    if not duration:
        return 0
    total = 0
    hours = re.search(r"(\d+)\s*h", duration)
    mins  = re.search(r"(\d+)\s*min", duration)
    if hours:
        total += int(hours.group(1)) * 60
    if mins:
        total += int(mins.group(1))
    return total


def _js_round2(value: float) -> float:
    """Round to 2 decimal places using JS semantics (round half up, not banker's rounding)."""
    return math.floor(value * 100 + 0.5) / 100


def _haversine_km(a: dict | None, b: dict | None) -> float | None:
    """
    Straight-line distance in km between two attraction dicts (need latitude/longitude keys).
    Returns None if either point is missing coordinates — callers treat None as 0 travel time.
    """
    if not a or not b:
        return None
    if a.get("latitude") is None or a.get("longitude") is None:
        return None
    if b.get("latitude") is None or b.get("longitude") is None:
        return None
    R = 6371
    lat1  = math.radians(a["latitude"])
    lat2  = math.radians(b["latitude"])
    d_lat = math.radians(b["latitude"]  - a["latitude"])
    d_lon = math.radians(b["longitude"] - a["longitude"])
    h = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h))


def _haversine_minutes(a: dict | None, b: dict | None, speed_kmh: int = 5) -> int:
    """
    Estimated travel time in minutes between two points, rounded UP to the nearest 5.
    Used for budget checks and route optimisation (not for display — Google times are used there).
    """
    km = _haversine_km(a, b)
    if km is None:
        return 0
    raw = (km / speed_kmh) * 60
    return math.ceil(raw / 5) * 5


def _recalculate_item_times(items: list[dict], start_time: str) -> list[dict]:
    """
    Walk through a flat list of attraction/travel/break items and assign
    sequential start_at / end_at clock strings to each one.
    Each item's duration drives the clock forward.
    """
    current = _time_to_minutes(start_time)
    result  = []
    for item in items:
        duration = (
            _duration_minutes(item.get("duration"))
            if item["type"] == "attraction"
            else item["duration"]
        )
        start_at = _minutes_to_time(current)
        current += duration
        end_at   = _minutes_to_time(current)
        result.append({**item, "start_at": start_at, "end_at": end_at})
    return result


def _compute_day_items(attractions, travel_minutes, break_durations, start_time, travel_km=None):
    """
    Build the flat [attraction, travel, break, attraction, travel, break, ...] list
    for one day, then stamp clock times via _recalculate_item_times.

    - travel_minutes[i]  = minutes to travel from attraction i to i+1
    - break_durations[i] = break duration after gap i, or None if no break
    - travel_km[i]       = distance for gap i (display only, not used for timing)
    - gapIndex on travel/break items is the index of the preceding attraction,
      used by the frontend to identify which gap a travel/break belongs to.
    """
    travel_km  = travel_km or []
    raw_items  = []
    last_index = len(attractions) - 1

    for i, attr in enumerate(attractions):
        raw_items.append({"type": "attraction", **attr})
        if i < last_index:
            travel = travel_minutes[i] if i < len(travel_minutes) else 0
            raw_items.append({
                "type":       "travel",
                "id":         f"travel-{attr['id']}",
                "duration":   travel,
                "gapIndex":   i,
                "distanceKm": travel_km[i] if i < len(travel_km) else None,
            })
            break_dur = break_durations[i] if i < len(break_durations) else None
            if break_dur is not None:
                raw_items.append({
                    "type":     "break",
                    "id":       f"break-{attr['id']}",
                    "duration": break_dur,
                    "gapIndex": i,
                })

    return _recalculate_item_times(raw_items, start_time)


def place_to_attraction(place) -> dict:
    """Convert a Place ORM row to the plain dict the planner works with internally."""
    return {
        "id":           place.id,
        "name_en":      place.name_en,
        "name_pl":      place.name_pl,
        "category":     place.category,
        "description":  place.description,
        "opening_hours":place.opening_hours,
        "duration":     place.duration,
        "price_range":  place.price_range,
        "image_url":    place.image_url,
        "latitude":     place.latitude,
        "longitude":    place.longitude,
    }


# ---------------------------------------------------------------------------
# GENERATION 2 — to be removed when /itinerary/generate is retired
# ---------------------------------------------------------------------------

def build_daily_itinerary(
    attractions: list[dict],
    num_days: int,
    intensity: str = "moderate",
    start_time: str = "09:00",
    break_duration_minutes: int = 30,
    transport_mode: str = "walking",
) -> dict:
    """
    Multi-day greedy packer ported 1:1 from the frontend buildDailyItinerary (utils.js).
    Respects the order of attractions as received — ordering is the caller's responsibility.
    Time budget per day comes from intensity config (max_minutes_per_day).
    Used by POST /itinerary/generate; will be retired when /plan-optimized is live.
    """
    config          = get_intensity_config(intensity)
    max_minutes     = config["max_minutes_per_day"]
    max_attractions = config["max_attractions_per_day"]
    is_relaxed      = intensity == "relaxed"
    speed           = get_transport_speed(transport_mode)

    days = [
        {
            "attractions":    [],
            "travelMinutes":  [],
            "travelKm":       [],
            "breakDurations": [],
            "items":          [],
            "totalMinutes":   0,
        }
        for _ in range(num_days)
    ]
    overflow = []

    for attraction in attractions:
        duration = _duration_minutes(attraction.get("duration"))

        # Try to fit into the first day that has room (time + count budget).
        day_index = -1
        for idx, day in enumerate(days):
            last           = day["attractions"][-1] if day["attractions"] else None
            travel         = _haversine_minutes(last, attraction, speed) if last else 0
            break_overhead = break_duration_minutes if (is_relaxed and day["attractions"]) else 0
            fits_time      = day["totalMinutes"] + travel + break_overhead + duration <= max_minutes
            fits_count     = max_attractions is None or len(day["attractions"]) < max_attractions
            if fits_time and fits_count:
                day_index = idx
                break

        if day_index != -1:
            day = days[day_index]
            if day["attractions"]:
                last   = day["attractions"][-1]
                travel = _haversine_minutes(last, attraction, speed)
                km     = _haversine_km(last, attraction)
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


# ---------------------------------------------------------------------------
# GENERATION 3 helpers
# ---------------------------------------------------------------------------

def _resolve_day_settings(
    day_index: int,
    global_start: str,
    global_end: str,
    global_intensity: str,
    days_config: list | None,
) -> dict:
    """
    Merge global defaults with the optional per-day override for one day.
    days_config is a list of plain dicts (serialised from DayConfig by the endpoint);
    a None entry means "use all globals for this day".

    Returns a dict with: start_time, end_time, intensity, max_minutes, max_attractions.
    max_minutes = end_time - start_time (intensity no longer controls the time budget).
    max_attractions comes from the intensity config (its only remaining role).
    """
    override = None
    if days_config and day_index < len(days_config):
        override = days_config[day_index]

    start_time = (override.get("start_time") or global_start)     if override else global_start
    end_time   = (override.get("end_time")   or global_end)       if override else global_end
    intensity  = (override.get("intensity")  or global_intensity) if override else global_intensity

    max_minutes = _time_to_minutes(end_time) - _time_to_minutes(start_time)
    config      = get_intensity_config(intensity)

    return {
        "start_time":      start_time,
        "end_time":        end_time,
        "intensity":       intensity,
        "max_minutes":     max_minutes,
        "max_attractions": config["max_attractions_per_day"],
    }


# ---------------------------------------------------------------------------
# GENERATION 3 — active, used by POST /itinerary/plan-optimized
# ---------------------------------------------------------------------------

def build_optimized_itinerary(
    attractions: list[dict],
    num_days: int,
    global_intensity: str = "moderate",
    global_start_time: str = "09:00",
    global_end_time: str = "17:00",
    transport_mode: str = "walking",
    break_duration_minutes: int = 30,
    days_config: list | None = None,
) -> dict:
    """
    Greedy packer with per-day time windows and per-day intensity overrides.

    Key differences from build_daily_itinerary (Gen 2):
    - Time budget per day = end_time - start_time, NOT intensity.max_minutes_per_day.
      Intensity only controls the attraction count cap for each day.
    - Each day in the response includes startTime, endTime, intensity fields.
    - days_config allows overriding any of these per day.

    Steps still to be added (see endpoints/itinerary.py for the full roadmap):
    - Pinned attractions: pre-assign specific place_ids to specific days before
      the greedy loop runs (place_ids in pins are removed from the free pool).
    - Anchor resolution: Stary Rynek default, prev/next day handoff logic.
    - Route optimisation: nearest-neighbour + 2-opt within each day.
    """
    speed    = get_transport_speed(transport_mode)
    resolved = [
        _resolve_day_settings(i, global_start_time, global_end_time, global_intensity, days_config)
        for i in range(num_days)
    ]

    days = [
        {
            "attractions":    [],
            "travelMinutes":  [],
            "travelKm":       [],
            "breakDurations": [],
            "items":          [],
            "totalMinutes":   0,
            "startTime":      r["start_time"],
            "endTime":        r["end_time"],
            "intensity":      r["intensity"],
        }
        for r in resolved
    ]
    overflow = []

    # TODO (pinned attractions step): pre-assign pinned attractions here before
    # the loop below, so the greedy packer treats them as already placed.

    for attraction in attractions:
        duration = _duration_minutes(attraction.get("duration"))

        # Try to fit into the first day with room (time + count budget).
        day_index = -1
        for idx, day in enumerate(days):
            r          = resolved[idx]
            is_relaxed = r["intensity"] == "relaxed"
            last       = day["attractions"][-1] if day["attractions"] else None
            travel     = _haversine_minutes(last, attraction, speed) if last else 0
            break_oh   = break_duration_minutes if (is_relaxed and day["attractions"]) else 0
            fits_time  = day["totalMinutes"] + travel + break_oh + duration <= r["max_minutes"]
            fits_count = r["max_attractions"] is None or len(day["attractions"]) < r["max_attractions"]
            if fits_time and fits_count:
                day_index = idx
                break

        if day_index != -1:
            day        = days[day_index]
            is_relaxed = resolved[day_index]["intensity"] == "relaxed"
            if day["attractions"]:
                last   = day["attractions"][-1]
                travel = _haversine_minutes(last, attraction, speed)
                km     = _haversine_km(last, attraction)
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

    for i, day in enumerate(days):
        day["items"] = _compute_day_items(
            day["attractions"],
            day["travelMinutes"],
            day["breakDurations"],
            resolved[i]["start_time"],
            day["travelKm"],
        )

    return {"days": days, "overflow": overflow}
