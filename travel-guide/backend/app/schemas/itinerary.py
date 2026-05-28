from pydantic import BaseModel
from typing import List

class ItineraryRequest(BaseModel):
    place_ids: List[int]
    total_minutes: int
    intensity: str = "moderate"
    start_time: str = "09:00"
    break_duration_minutes: int = 30
