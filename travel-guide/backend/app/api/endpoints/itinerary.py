from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.place import Place
from app.schemas.itinerary import ItineraryRequest
from app.services.planner_service import schedule_itinerary

router = APIRouter()

@router.post("/plan")
async def create_plan(request: ItineraryRequest, db: Session = Depends(get_db)):
    places = db.query(Place).filter(Place.id.in_(request.place_ids)).all()

    if not places:
        raise HTTPException(status_code=404, detail="No places found for given IDs")

    items = schedule_itinerary(
        places,
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
