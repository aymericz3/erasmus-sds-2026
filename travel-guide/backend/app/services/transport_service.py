import math
import requests
from app.core.config import settings

GOOGLE_BASE = "https://maps.googleapis.com/maps/api/distancematrix/json"

# Modes sent to Google Distance Matrix API
_GOOGLE_MODES = {
    "walking":  {"mode": "walking"},
    "cycling":  {"mode": "bicycling"},
    "driving":  {"mode": "driving"},
    "tram":     {"mode": "transit", "transit_mode": "tram|rail"},
}


def _haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _round_up_5(minutes: float) -> int:
    return math.ceil(minutes / 5) * 5


def _fallback_minutes(km: float, mode: str) -> int:
    """Rough estimate when Google API is unavailable, rounded up to nearest 5 min."""
    speeds = {"walking": 5, "cycling": 15, "driving": 30, "tram": 20}
    raw = (km / speeds.get(mode, 5)) * 60
    return _round_up_5(raw)


def _call_google(origin_lat, origin_lon, dest_lat, dest_lon, mode_key: str) -> dict | None:
    """
    Call Google Distance Matrix for one mode.
    Returns {"minutes": int, "distance_km": float} or None on failure.
    """
    if not settings.google_maps_api_key or settings.google_maps_api_key == "your_key_here":
        return None

    params = {
        "origins": f"{origin_lat},{origin_lon}",
        "destinations": f"{dest_lat},{dest_lon}",
        "key": settings.google_maps_api_key,
        **_GOOGLE_MODES[mode_key],
    }

    try:
        resp = requests.get(GOOGLE_BASE, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        element = data["rows"][0]["elements"][0]
        if element["status"] != "OK":
            return None
        minutes = math.ceil(element["duration"]["value"] / 60)
        distance_km = round(element["distance"]["value"] / 1000, 2)
        return {"minutes": minutes, "distance_km": distance_km}
    except Exception:
        return None


def get_travel_times(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float) -> dict:
    """
    Return travel time and distance for all 4 modes between two coordinates.
    Falls back to Haversine estimates if Google API is unavailable.

    Returns:
        {
            "walking":  {"minutes": int, "distance_km": float, "source": "google"|"estimate"},
            "cycling":  {...},
            "driving":  {...},
            "tram":     {...},
        }
    """
    km = _haversine_km(origin_lat, origin_lon, dest_lat, dest_lon)
    results = {}

    for mode in _GOOGLE_MODES:
        google = _call_google(origin_lat, origin_lon, dest_lat, dest_lon, mode)
        if google:
            results[mode] = {**google, "source": "google"}
        else:
            results[mode] = {
                "minutes": _fallback_minutes(km, mode),
                "distance_km": round(km, 2),
                "source": "estimate",
            }

    return results
