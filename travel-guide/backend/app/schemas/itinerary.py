from pydantic import BaseModel
from typing import List, Optional


class Coordinates(BaseModel):
    # A GPS point used as a day anchor (e.g. hotel, train station, map pin).
    lat: float
    lon: float


class DayConfig(BaseModel):
    # Per-day overrides. Any field left null falls back to the global default
    # on ItineraryRequest. One entry per day in days_config.
    start_time: Optional[str] = None       # e.g. "08:00" — overrides global start_time
    end_time: Optional[str] = None         # e.g. "20:00" — overrides global end_time
    intensity: Optional[str] = None        # overrides global intensity for this day only
    start_anchor: Optional[Coordinates] = None  # where the day should start (hotel, pin…)
    end_anchor: Optional[Coordinates] = None    # where the day should end


class AttractionPin(BaseModel):
    # Guarantees a specific attraction appears on a specific day.
    # The attraction is removed from the free pool before the greedy packer runs,
    # so it is always placed on the requested day regardless of time budget.
    place_id: int
    day: int                    # 0-indexed (0 = first day)
    time: Optional[str] = None  # "14:00" — if set, attraction is scheduled at this exact time


class ItineraryRequest(BaseModel):
    place_ids: List[int]                   # unordered pool — backend determines visit order
    num_days: int = 1
    intensity: str = "moderate"            # global default, can be overridden per day
    start_time: str = "09:00"             # global default daily start
    end_time: str = "21:00"               # global default daily end
    transport_mode: str = "walking"        # default for all legs, per-leg override coming later
    break_duration_minutes: int = 30
    # Optional list of per-day configs. Can be null for a day to use all globals.
    # Example: [{"start_anchor": {"lat": 52.4, "lon": 16.9}}, null, null]
    days_config: Optional[List[Optional[DayConfig]]] = None
    # Optional list of attractions pinned to a specific day (and optionally a time).
    # Example: [{"place_id": 5, "day": 1, "time": "14:00"}]
    pins: Optional[List[AttractionPin]] = None
    # User's preferred categories — attractions in these categories are packed first
    # so they survive the overflow cut when the time budget is tight.
    selected_categories: Optional[List[str]] = None


# ---------------------------------------------------------------------------
# Google finalization — POST /itinerary/finalize
# Called once the user is happy with the ordering. Replaces haversine estimates
# with real Google Distance Matrix times for the selected transport mode.
# ---------------------------------------------------------------------------

class FinalizeDayInput(BaseModel):
    # One day's worth of ordered place_ids as confirmed by the user.
    place_ids: List[int]
    start_time: str = "09:00"
    # Per-gap break durations (same length as place_ids - 1). None = no break.
    break_durations: Optional[List[Optional[int]]] = None


class FinalizeRequest(BaseModel):
    days: List[FinalizeDayInput]
    transport_mode: str = "walking"  # applied to all legs
