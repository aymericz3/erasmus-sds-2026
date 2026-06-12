from pydantic import BaseModel
from typing import List, Optional


# ---------------------------------------------------------------------------
# OBSOLETE — used only by POST /itinerary/plan (Sprint 1, single-day only).
# The frontend never calls /plan directly; it was only used for early testing.
# Can be removed once /plan is dropped.
# ---------------------------------------------------------------------------
class ItineraryRequest(BaseModel):
    place_ids: List[int]
    total_minutes: int          # hard time cap computed by the frontend
    intensity: str = "moderate"
    start_time: str = "09:00"
    break_duration_minutes: int = 30


# ---------------------------------------------------------------------------
# Used by POST /itinerary/generate (Sprint 2 I3, multi-day).
# Preserves the place_ids order sent by the frontend — ordering was the
# frontend's responsibility. /generate will be replaced by /plan-optimized
# once the frontend is updated; this schema can be removed at that point.
# ---------------------------------------------------------------------------
class ItineraryPlanRequest(BaseModel):
    place_ids: List[int]        # ordered by the frontend (click order)
    num_days: int = 1
    intensity: str = "moderate" # controls time cap + attraction count per day
    start_time: str = "09:00"
    break_duration_minutes: int = 30
    transport_mode: str = "walking"


# ---------------------------------------------------------------------------
# Current — used by POST /itinerary/plan-optimized.
# The backend is now responsible for ordering: it receives an unordered pool
# of place_ids and returns an optimized route with per-day time windows,
# per-day intensity overrides, start/end anchor support, and warnings.
# ---------------------------------------------------------------------------

class Coordinates(BaseModel):
    # A GPS point used as a day anchor (e.g. hotel, train station, map pin).
    lat: float
    lon: float


class DayConfig(BaseModel):
    # Per-day overrides. Any field left null falls back to the global default
    # on OptimizedItineraryRequest. One entry per day in days_config.
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


class OptimizedItineraryRequest(BaseModel):
    place_ids: List[int]                   # unordered pool — backend determines visit order
    num_days: int = 1
    intensity: str = "moderate"            # global default, can be overridden per day
    start_time: str = "09:00"             # global default daily start
    end_time: str = "17:00"               # global default daily end (replaces max_minutes)
    transport_mode: str = "walking"        # default for all legs, per-leg override coming later
    break_duration_minutes: int = 30
    # Optional list of per-day configs. Can be null for a day to use all globals.
    # Example: [{"start_anchor": {"lat": 52.4, "lon": 16.9}}, null, null]
    days_config: Optional[List[Optional[DayConfig]]] = None
    # Optional list of attractions pinned to a specific day (and optionally a time).
    # Example: [{"place_id": 5, "day": 1, "time": "14:00"}]
    pins: Optional[List[AttractionPin]] = None


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
