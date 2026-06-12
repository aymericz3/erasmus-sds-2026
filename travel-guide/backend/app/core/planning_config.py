"""
Planning constants — ported 1:1 from the frontend (constants.js) so the backend
planner produces results identical to the original client-side algorithm.
"""

# Itinerary intensity levels: per-day time budget and attraction cap.
# max_attractions_per_day = None means "no cap".
INTENSITY_OPTIONS = [
    {"key": "relaxed",  "max_minutes_per_day": 240, "max_attractions_per_day": 3},
    {"key": "moderate", "max_minutes_per_day": 360, "max_attractions_per_day": 5},
    {"key": "intense",  "max_minutes_per_day": 480, "max_attractions_per_day": None},
]

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
