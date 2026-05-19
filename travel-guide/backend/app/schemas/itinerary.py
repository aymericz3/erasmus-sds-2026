from pydantic import BaseModel
from typing import List

class ItineraryRequest(BaseModel):
    place_ids: List[int]
    total_minutes: int