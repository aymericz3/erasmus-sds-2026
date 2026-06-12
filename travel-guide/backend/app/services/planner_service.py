"""
planner_service.py — all itinerary scheduling logic.

  build_itinerary  →  POST /itinerary/plan
    Backend-driven multi-day planner: per-day time windows, per-day intensity
    overrides, start/end anchor-based routing, nearest-neighbour + 2-opt route
    optimisation, pinned attractions, and validation warnings.

Private helpers (_haversine_km, _compute_day_items, etc.) are used by both
build_itinerary and the /finalize endpoint.
"""

import math
import re

from app.core.planning_config import get_intensity_config, get_transport_speed, get_min_rest_minutes


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
# Shared helpers
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


def _pad_travel(minutes: int) -> int:
    """
    Round travel time UP to the nearest 10-minute interval.
    The gap in the schedule is always a round number so the user has leeway —
    e.g. 7 min → 10 min, 17 min → 20 min, 25 min → 30 min.
    Returns 0 for zero-duration legs (same location).
    The raw travel time is preserved separately on the item as 'actualMinutes'.
    """
    if minutes <= 0:
        return 0
    return math.ceil(minutes / 10) * 10


def _recalculate_item_times(
    items: list[dict],
    start_time: str,
    pin_conflicts: list | None = None,
) -> list[dict]:
    """
    Walk through a flat list of attraction/travel/break items and assign
    sequential start_at / end_at clock strings to each one.

    If an attraction has a 'pinned_time' key the clock jumps forward to that
    time before scheduling it. If the preceding items already ran past
    pinned_time, a conflict entry is appended to pin_conflicts (if provided)
    and the attraction is scheduled at the earliest available moment instead.
    """
    current = _time_to_minutes(start_time)
    result  = []
    for item in items:
        if item["type"] == "attraction" and item.get("pinned_time"):
            target = _time_to_minutes(item["pinned_time"])
            if current > target:
                if pin_conflicts is not None:
                    pin_conflicts.append({
                        "type":     "pin_time_conflict",
                        "place_id": item.get("id"),
                        "name":     item.get("name_en") or item.get("name_pl"),
                        "message": (
                            f"'{item.get('name_en') or item.get('name_pl')}' is pinned at "
                            f"{item['pinned_time']} but the schedule reaches that point at "
                            f"{_minutes_to_time(current)}. Scheduled at earliest available time."
                        ),
                    })
            else:
                current = target  # jump forward; gap before this attraction is free time

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


def _compute_day_items(
    attractions, travel_minutes, break_durations, start_time,
    travel_km=None, pin_conflicts: list | None = None,
):
    """
    Build the flat [attraction, travel, break, attraction, travel, break, ...] list
    for one day, then stamp clock times via _recalculate_item_times.

    - travel_minutes[i]  = minutes to travel from attraction i to i+1
    - break_durations[i] = break duration after gap i, or None if no break
    - travel_km[i]       = distance for gap i (display only, not used for timing)
    - gapIndex on travel/break items is the index of the preceding attraction,
      used by the frontend to identify which gap a travel/break belongs to.
    - pin_conflicts: if provided, any pinned_time conflicts are appended to it.
    """
    travel_km  = travel_km or []
    raw_items  = []
    last_index = len(attractions) - 1

    for i, attr in enumerate(attractions):
        raw_items.append({"type": "attraction", **attr})
        if i < last_index:
            travel = travel_minutes[i] if i < len(travel_minutes) else 0
            raw_items.append({
                "type":          "travel",
                "id":            f"travel-{attr['id']}",
                "duration":      _pad_travel(travel),  # rounded up to nearest 10 — drives the clock
                "actualMinutes": travel,               # raw travel time shown to the user
                "gapIndex":      i,
                "distanceKm":    travel_km[i] if i < len(travel_km) else None,
            })
            break_dur = break_durations[i] if i < len(break_durations) else None
            if break_dur is not None:
                raw_items.append({
                    "type":     "break",
                    "id":       f"break-{attr['id']}",
                    "duration": break_dur,
                    "gapIndex": i,
                })

    return _recalculate_item_times(raw_items, start_time, pin_conflicts)


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
# Planner helpers
# ---------------------------------------------------------------------------

def _check_intensity_window(day_index: int, resolved: list[dict]) -> dict | None:
    """
    Warn if the day's time window is too short or too long for its intensity.
    E.g. a 10h window with relaxed intensity (designed for ~2–6h) is a mismatch.
    Returns a warning dict or None if everything looks fine.
    """
    r           = resolved[day_index]
    config      = get_intensity_config(r["intensity"])
    window      = r["max_minutes"]
    min_window  = config["min_window_minutes"]
    max_window  = config["max_window_minutes"]

    if window < min_window:
        return {
            "type":    "intensity_mismatch",
            "day":     day_index + 1,  # 1-indexed for display
            "message": (
                f"Day {day_index + 1}: {r['intensity']} intensity expects at least "
                f"{min_window // 60}h but the window is only {window // 60}h "
                f"{window % 60:02d}min ({r['start_time']}–{r['end_time']})."
            ),
        }
    if window > max_window:
        return {
            "type":    "intensity_mismatch",
            "day":     day_index + 1,
            "message": (
                f"Day {day_index + 1}: {r['intensity']} intensity is designed for up to "
                f"{max_window // 60}h but the window is {window // 60}h "
                f"{window % 60:02d}min ({r['start_time']}–{r['end_time']}). "
                f"Consider switching to a more intense setting."
            ),
        }
    return None


def _check_inter_day_rest(day_index: int, days: list[dict], resolved: list[dict]) -> dict | None:
    """
    Warn if there is less than MIN_REST_MINUTES of rest between the actual end
    of day N and the configured start of day N+1.
    Rest is computed across the midnight boundary (day N ends at e.g. 20:00,
    day N+1 starts at 09:00 → 13h rest).
    """
    if day_index >= len(days) - 1:
        return None  # no next day to compare against

    day = days[day_index]

    # Actual end: last item's end_at, or the configured end_time if day is empty.
    if day["items"]:
        actual_end_str = day["items"][-1]["end_at"]
    else:
        actual_end_str = resolved[day_index]["end_time"]

    next_start_str = resolved[day_index + 1]["start_time"]

    end_min   = _time_to_minutes(actual_end_str)
    start_min = _time_to_minutes(next_start_str)

    # Rest spans midnight: add 24h if next start is earlier in the clock than current end.
    rest_minutes = start_min - end_min
    if rest_minutes < 0:
        rest_minutes += 24 * 60

    min_rest = get_min_rest_minutes()
    if rest_minutes < min_rest:
        rest_h   = rest_minutes // 60
        rest_min = rest_minutes % 60
        return {
            "type":          "insufficient_rest",
            "between_days":  [day_index + 1, day_index + 2],  # 1-indexed
            "rest_hours":    round(rest_minutes / 60, 1),
            "message": (
                f"Only {rest_h}h {rest_min:02d}min of rest between day {day_index + 1} "
                f"(ends {actual_end_str}) and day {day_index + 2} "
                f"(starts {next_start_str}). "
                f"Recommended minimum is {min_rest // 60}h."
            ),
        }
    return None


# Default city-centre anchor used when no explicit start/end is provided.
_CITY_CENTRE = {"latitude": 52.40825, "longitude": 16.93364}  # Stary Rynek


def _km_cached(a, b, cache: dict | None) -> float | None:
    """
    Return km between two points, using the pre-built distance cache when both
    points carry an 'id' key (i.e. they are attraction dicts, not raw anchors).
    Falls back to haversine for anchor points that have no id.
    """
    if cache is not None and a and b:
        a_id = a.get("id")
        b_id = b.get("id")
        if a_id is not None and b_id is not None:
            return cache.get((a_id, b_id))
    return _haversine_km(a, b)


def _route_distance(attractions: list[dict], start_anchor, end_anchor, speed: int,
                    cache: dict | None = None) -> int:
    """
    Total estimated travel time for a route: start_anchor → attractions → end_anchor.
    end_anchor may be None (open end), in which case only the inter-attraction legs count.
    Used as the objective function for 2-opt.
    """
    total = 0
    prev  = start_anchor
    for a in attractions:
        km     = _km_cached(prev, a, cache)
        total += int(math.ceil((km / speed) * 60 / 5) * 5) if km else 0
        prev   = a
    if end_anchor:
        km     = _km_cached(prev, end_anchor, cache)
        total += int(math.ceil((km / speed) * 60 / 5) * 5) if km else 0
    return total


def _nearest_neighbour(
    attractions: list[dict],
    start_anchor,
    cache: dict | None = None,
) -> list[dict]:
    """
    Greedy nearest-neighbour ordering starting from start_anchor.
    At each step, pick the unvisited attraction closest (in km) to the current
    position. Speed is not needed here — all legs share the same speed so
    closest km == closest time. Uses dist_cache for attraction-to-attraction lookups.
    """
    if not attractions:
        return []

    unvisited = list(attractions)
    ordered   = []
    current   = start_anchor

    while unvisited:
        nearest = min(unvisited, key=lambda a: (
            _km_cached(current, a, cache) or _haversine_km(current, a) or 0
        ))
        ordered.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return ordered


def _two_opt(
    attractions: list[dict],
    start_anchor,
    end_anchor,
    speed: int,
    cache: dict | None = None,
) -> list[dict]:
    """
    Improve a route by trying all pairs of edge swaps (2-opt).
    Reverses the sub-sequence between indices i and k whenever doing so reduces
    the total route distance. Stops when no improving swap is found.
    The start_anchor and end_anchor are included in the distance objective so the
    route stays anchored to them even after swaps.
    """
    best     = list(attractions)
    improved = True
    while improved:
        improved = False
        best_dist = _route_distance(best, start_anchor, end_anchor, speed, cache)
        for i in range(len(best) - 1):
            for k in range(i + 1, len(best)):
                candidate      = best[:i] + best[i:k + 1][::-1] + best[k + 1:]
                candidate_dist = _route_distance(candidate, start_anchor, end_anchor, speed, cache)
                if candidate_dist < best_dist:
                    best      = candidate
                    best_dist = candidate_dist
                    improved  = True


    return best


def _optimise_day_order(
    attractions: list[dict],
    start_anchor,
    end_anchor,
    speed: int,
    cache: dict | None = None,
) -> list[dict]:
    """
    Return attractions in the optimised visiting order for one day.
    Runs nearest-neighbour first (fast, good starting point), then 2-opt
    (removes route crossings). Both respect the start and end anchors.
    """
    if len(attractions) <= 1:
        return attractions
    ordered = _nearest_neighbour(attractions, start_anchor, cache)
    return _two_opt(ordered, start_anchor, end_anchor, speed, cache)


def _resolve_anchors(
    num_days: int,
    days_config: list | None,
    days: list[dict],
) -> list[dict]:
    """
    Determine the start and end anchor for each day following these rules:

    Start anchor priority (per day):
      1. Explicit start_anchor in days_config for this day
      2. Day 1 → city centre (Stary Rynek)
         Day 2+ → previous day's explicit end_anchor if set,
                  otherwise last attraction of the previous day

    End anchor priority (per day):
      1. Explicit end_anchor in days_config for this day
      2. Last day → city centre (Stary Rynek)
         Middle days → next day's explicit start_anchor if set,
                       otherwise None (optimizer is free to end anywhere)

    Returns a list of {"start": dict|None, "end": dict|None} per day.
    The dicts have "latitude"/"longitude" keys so _haversine_* functions work directly.
    """
    def _cfg(day_index):
        if days_config and day_index < len(days_config):
            return days_config[day_index] or {}
        return {}

    def _anchor_coords(anchor_dict):
        if not anchor_dict:
            return None
        return {"latitude": anchor_dict["lat"], "longitude": anchor_dict["lon"]}

    anchors = []
    for i in range(num_days):
        cfg      = _cfg(i)
        cfg_next = _cfg(i + 1) if i < num_days - 1 else {}

        # --- start anchor ---
        if cfg.get("start_anchor"):
            start = _anchor_coords(cfg["start_anchor"])
        elif i == 0:
            start = _CITY_CENTRE
        else:
            prev_cfg = _cfg(i - 1)
            if prev_cfg.get("end_anchor"):
                start = _anchor_coords(prev_cfg["end_anchor"])
            else:
                prev_attractions = days[i - 1]["attractions"]
                start = prev_attractions[-1] if prev_attractions else _CITY_CENTRE

        # --- end anchor ---
        if cfg.get("end_anchor"):
            end = _anchor_coords(cfg["end_anchor"])
        elif i == num_days - 1:
            end = _CITY_CENTRE
        else:
            if cfg_next.get("start_anchor"):
                end = _anchor_coords(cfg_next["start_anchor"])
            else:
                end = None  # optimizer is free

        anchors.append({"start": start, "end": end})

    return anchors


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
# Main planner — POST /itinerary/plan
# ---------------------------------------------------------------------------

def build_itinerary(
    attractions: list[dict],
    num_days: int,
    global_intensity: str = "moderate",
    global_start_time: str = "09:00",
    global_end_time: str = "21:00",
    transport_mode: str = "walking",
    break_duration_minutes: int = 30,
    days_config: list | None = None,
    pins: list | None = None,
    selected_categories: list | None = None,
) -> dict:
    """
    Greedy multi-day packer with route optimisation and per-day configuration.

    Time budget per day = end_time - start_time.
    Intensity controls the attraction count cap (not time budget).
    Each day in the response includes startTime, endTime, intensity fields.
    days_config allows overriding any of these per day.

    Steps still to be added (see endpoints/itinerary.py for the full roadmap):
    - Pinned attractions: pre-assign specific place_ids to specific days before
      the greedy loop runs (place_ids in pins are removed from the free pool).
    - Route optimisation: nearest-neighbour + 2-opt within each day,
      consuming startAnchor/endAnchor already resolved on each day dict.
    """
    speed    = get_transport_speed(transport_mode)
    warnings: list = []  # collected throughout; returned at the end

    # Pre-build pairwise haversine distance matrix (km) for all attractions.
    # Keyed by (id_a, id_b); symmetric so both directions are stored.
    # The optimizer functions look up from this cache instead of recomputing,
    # which matters most in the 2-opt inner loop (O(N²) evaluations per pass).
    dist_cache: dict = {}
    for a in attractions:
        for b in attractions:
            if a["id"] != b["id"] and (a["id"], b["id"]) not in dist_cache:
                km = _haversine_km(a, b)
                dist_cache[(a["id"], b["id"])] = km
                dist_cache[(b["id"], a["id"])] = km

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

    # Pre-assign pinned attractions to their designated days.
    # They are removed from the free pool so the greedy packer never double-places them.
    # If a pin specifies a time, it is stored on the attraction dict so
    # _recalculate_item_times can jump the clock to that time when it reaches it.
    pinned_ids: set = set()
    if pins:
        for pin in pins:
            day_idx  = pin.get("day", -1)
            place_id = pin.get("place_id")
            if day_idx < 0 or day_idx >= num_days:
                warnings.append({
                    "type":     "invalid_pin",
                    "place_id": place_id,
                    "message":  f"Pin for place {place_id} targets day {day_idx + 1} "
                                f"which does not exist (trip has {num_days} day(s)).",
                })
                continue
            attr = next((a for a in attractions if a["id"] == place_id), None)
            if attr is None:
                continue
            pinned_attr = dict(attr)
            if pin.get("time"):
                pinned_attr["pinned_time"] = pin["time"]
            days[day_idx]["attractions"].append(pinned_attr)
            days[day_idx]["totalMinutes"] += _duration_minutes(attr.get("duration"))
            pinned_ids.add(place_id)

    # Free pool: all attractions not already pinned to a specific day.
    # Sort preferred categories first so they win the overflow cut when the
    # time budget is tight — non-preferred attractions are the ones left out.
    preferred = set(selected_categories) if selected_categories else set()
    free_attractions = sorted(
        [a for a in attractions if a["id"] not in pinned_ids],
        key=lambda a: 0 if a.get("category") in preferred else 1,
    )

    for attraction in free_attractions:
        duration = _duration_minutes(attraction.get("duration"))

        # Try to fit into the first day with room (time + count budget).
        day_index = -1
        for idx, day in enumerate(days):
            r          = resolved[idx]
            is_relaxed = r["intensity"] == "relaxed"
            last       = day["attractions"][-1] if day["attractions"] else None
            travel     = _pad_travel(_haversine_minutes(last, attraction, speed)) if last else 0
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
                day["totalMinutes"] += _pad_travel(travel)
                day["breakDurations"].append(break_duration_minutes if is_relaxed else None)
                if is_relaxed:
                    day["totalMinutes"] += break_duration_minutes
            day["attractions"].append(attraction)
            day["totalMinutes"] += duration
        else:
            overflow.append(attraction)

    # Resolve anchors after packing — start anchors for day 2+ may depend on
    # the last attraction placed in the previous day.
    anchors = _resolve_anchors(num_days, days_config, days)
    for i, day in enumerate(days):
        day["startAnchor"] = anchors[i]["start"]
        day["endAnchor"]   = anchors[i]["end"]

    # Re-order each day's attractions using nearest-neighbour + 2-opt, then
    # recompute travel/break/total from the new order.
    for i, day in enumerate(days):
        if len(day["attractions"]) > 1:
            day["attractions"] = _optimise_day_order(
                day["attractions"],
                anchors[i]["start"],
                anchors[i]["end"],
                speed,
                dist_cache,
            )

        # Recompute travel and break arrays from the optimised order.
        # Uses dist_cache for attraction-to-attraction legs.
        is_relaxed = resolved[i]["intensity"] == "relaxed"
        atts       = day["attractions"]
        t_mins, t_km, b_durs, total = [], [], [], 0

        for j, attr in enumerate(atts):
            total += _duration_minutes(attr.get("duration"))
            if j < len(atts) - 1:
                km     = _km_cached(attr, atts[j + 1], dist_cache)
                travel = int(math.ceil((km / speed) * 60 / 5) * 5) if km else 0
                t_mins.append(travel)      # raw nearest-5 — stored for display
                t_km.append(_js_round2(km) if km is not None else None)
                total += _pad_travel(travel)  # nearest-10 — drives totalMinutes
                b_durs.append(break_duration_minutes if is_relaxed else None)
                if is_relaxed:
                    total += break_duration_minutes

        day["travelMinutes"]  = t_mins
        day["travelKm"]       = t_km
        day["breakDurations"] = b_durs
        day["totalMinutes"]   = total

    pin_conflicts: list = []
    for i, day in enumerate(days):
        day["items"] = _compute_day_items(
            day["attractions"],
            day["travelMinutes"],
            day["breakDurations"],
            resolved[i]["start_time"],
            day["travelKm"],
            pin_conflicts,
        )

    # Collect remaining warnings after items are built (rest check needs actual end times).
    for i in range(num_days):
        w = _check_intensity_window(i, resolved)
        if w:
            warnings.append(w)
        w = _check_inter_day_rest(i, days, resolved)
        if w:
            warnings.append(w)

    return {"days": days, "overflow": overflow, "warnings": warnings + pin_conflicts}
