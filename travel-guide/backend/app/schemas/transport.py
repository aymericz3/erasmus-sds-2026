from pydantic import BaseModel

class TransportRequest(BaseModel):
    origin_lat: float
    origin_lon: float
    dest_lat: float
    dest_lon: float

class TransportMode(BaseModel):
    minutes: int
    distance_km: float
    source: str  # "google" or "estimate"

class TransportResponse(BaseModel):
    walking: TransportMode
    cycling: TransportMode
    driving: TransportMode
    tram: TransportMode
