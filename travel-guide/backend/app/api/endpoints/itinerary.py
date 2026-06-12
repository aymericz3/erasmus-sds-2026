from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.place import Place
from app.schemas.itinerary import ItineraryRequest, ItineraryPlanRequest
from app.services.planner_service import (
    schedule_itinerary,
    build_daily_itinerary,
    place_to_attraction,
    rank_attractions,
)

router = APIRouter()

@router.post("/plan")
async def create_plan(request: ItineraryRequest, db: Session = Depends(get_db)):
    places = db.query(Place).filter(Place.id.in_(request.place_ids)).all()

    if not places:
        raise HTTPException(status_code=404, detail="No places found for given IDs")
    
    categories = getattr(request, "selected_categories", [])
    ranked_places = rank_attractions(places, categories)

    items = schedule_itinerary(
        ranked_places,
        request.total_minutes,
        start_time=request.start_time,
        break_duration_minutes=request.break_duration_minutes,
        intensity=request.intensity,
    )

    scheduled = [i for i in items if i["type"] == "attraction"]
    return {
        "total_minutes": request.total_minutes,
        "start_time": request.start_time,
        "intensity": request.intensity,
        "items": items,
        "count": len(scheduled),
    }


@router.post("/generate")
async def generate_itinerary(request: ItineraryPlanRequest, db: Session = Depends(get_db)):
    """
    Build a full multi-day itinerary (clock times, travel, breaks, overflow).
    place_ids order is preserved so the greedy packer respects the user's selection.
    """
    places = db.query(Place).filter(Place.id.in_(request.place_ids)).all()

    if not places:
        raise HTTPException(status_code=404, detail="No places found for given IDs")

    # Preserve the order the client sent, since packing is order-sensitive.
    by_id = {p.id: p for p in places}
    attractions = [place_to_attraction(by_id[pid]) for pid in request.place_ids if pid in by_id]

    return build_daily_itinerary(
        attractions,
        num_days=request.num_days,
        intensity=request.intensity,
        start_time=request.start_time,
        break_duration_minutes=request.break_duration_minutes,
        transport_mode=request.transport_mode,
    )
