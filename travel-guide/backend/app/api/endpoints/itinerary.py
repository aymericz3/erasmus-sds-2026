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

    optimized_plan = schedule_itinerary(places, request.total_minutes)

    return {
        "total_minutes": request.total_minutes,
        "scheduled_places": [
            {
                "id": p.id, 
                "name": p.name_en or p.name_pl, 
                "duration": p.duration
            } for p in optimized_plan
        ],
        "count": len(optimized_plan)
    }