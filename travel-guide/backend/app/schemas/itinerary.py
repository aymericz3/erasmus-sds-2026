from pydantic import BaseModel
from typing import List

class ItineraryRequest(BaseModel):
    place_ids: List[int]
    total_minutes: int
    intensity: str = "moderate"
    start_time: str = "09:00"
    break_duration_minutes: int = 30


class ItineraryPlanRequest(BaseModel):
    """Request for the multi-day planner. place_ids order is preserved."""
    place_ids: List[int]
    num_days: int = 1
    intensity: str = "moderate"
    start_time: str = "09:00"
    break_duration_minutes: int = 30
    budget: str = "moderate"
    selected_categories: List[str] = []
    transport_mode: str = "walking"
    budget: str = "moderate"
    selected_categories: List[str] = []
