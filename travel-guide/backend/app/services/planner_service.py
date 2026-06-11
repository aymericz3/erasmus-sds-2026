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
