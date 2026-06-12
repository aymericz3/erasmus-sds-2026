"""
Planning constants — ported 1:1 from the frontend (constants.js) so the backend
planner produces results identical to the original client-side algorithm.
"""

# Itinerary intensity levels.
# max_minutes_per_day: used only by the old build_daily_itinerary (Generation 2).
#   Generation 3 derives the time budget from end_time - start_time instead.
# min_window_minutes / max_window_minutes: the "sensible" day-window range for
#   this intensity, used to detect mismatches and warn the user.
# max_attractions_per_day: None means no cap.
INTENSITY_OPTIONS = [
    {
        "key": "relaxed",
        "max_minutes_per_day": 240,
        "max_attractions_per_day": 3,
        "min_window_minutes": 120,   # warn if day window < 2h with relaxed
        "max_window_minutes": 360,   # warn if day window > 6h with relaxed
    },
    {
        "key": "moderate",
        "max_minutes_per_day": 360,
        "max_attractions_per_day": 5,
        "min_window_minutes": 240,   # warn if day window < 4h with moderate
        "max_window_minutes": 600,   # warn if day window > 10h with moderate
    },
    {
        "key": "intense",
        "max_minutes_per_day": 480,
        "max_attractions_per_day": None,
        "min_window_minutes": 360,   # warn if day window < 6h with intense
        "max_window_minutes": 960,   # warn if day window > 16h with intense (unrealistic)
    },
]

# Minimum rest between end of one day and start of the next before a warning
# is issued. Tweakable here without touching any planner logic.
MIN_REST_MINUTES = 600  # 10 hours

# Transport modes and the average speed (km/h) used for travel-time estimates.
TRANSPORT_OPTIONS = [
    {"key": "walking", "speed_kmh": 5},
    {"key": "cycling", "speed_kmh": 15},
    {"key": "transit", "speed_kmh": 20},
]

_DEFAULT_INTENSITY = INTENSITY_OPTIONS[1]  # moderate
_DEFAULT_SPEED = 5  # walking


def get_intensity_config(key: str) -> dict:
    return next((o for o in INTENSITY_OPTIONS if o["key"] == key), _DEFAULT_INTENSITY)


def get_transport_speed(mode: str) -> int:
    return next((o["speed_kmh"] for o in TRANSPORT_OPTIONS if o["key"] == mode), _DEFAULT_SPEED)


def get_min_rest_minutes() -> int:
    """Minimum rest between days before a warning is issued. Tune via MIN_REST_MINUTES."""
    return MIN_REST_MINUTES
