"""
Plaece schema used for API representation of places.
"""

from pydantic import BaseModel
from typing import Optional


class PlaceOut(BaseModel):
    id:            int
    name_en:       Optional[str] = None
    name_pl:       Optional[str] = None
    category:      str
    description:   Optional[str] = None
    opening_hours: Optional[str] = None
    duration:      Optional[str] = None
    price_range:   Optional[str] = None
    image_url:     Optional[str] = None
    latitude:      Optional[float] = None
    longitude:     Optional[float] = None

    # Enrichment fields (OpenStreetMap + Wikipedia)
    address:           Optional[str] = None
    website:           Optional[str] = None
    image_attribution: Optional[str] = None

    model_config = {"from_attributes": True}
