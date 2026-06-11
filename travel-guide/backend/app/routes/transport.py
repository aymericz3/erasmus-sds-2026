from fastapi import APIRouter
from app.schemas.transport import TransportRequest, TransportResponse
from app.services.transport_service import get_travel_times

router = APIRouter()

@router.post("/times", response_model=TransportResponse)
def travel_times(req: TransportRequest):
    """Return walking, cycling, driving, and tram travel times between two coordinates."""
    return get_travel_times(req.origin_lat, req.origin_lon, req.dest_lat, req.dest_lon)
