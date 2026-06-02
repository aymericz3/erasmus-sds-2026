from pydantic import BaseModel
from typing import List, Optional

class PreferenceSaveRequest(BaseModel):
    user_id: int
    intensity: Optional[str] = "moderate"
    transport_mode: Optional[str] = "walking"
    break_duration_minutes: Optional[int] = 30
    start_time: Optional[str] = "09:00"
    selected_categories: Optional[List[str]] = []