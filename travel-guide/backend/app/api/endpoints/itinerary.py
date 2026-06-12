from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.place import Place
from app.schemas.itinerary import ItineraryRequest, ItineraryPlanRequest, OptimizedItineraryRequest
from app.services.planner_service import (
    schedule_itinerary,
    build_daily_itinerary,
    build_optimized_itinerary,
    place_to_attraction,
    rank_attractions,
)

router = APIRouter()


# ---------------------------------------------------------------------------
# OBSOLETE — POST /itinerary/plan
# Sprint 1 single-day scheduler. Takes a flat total_minutes cap and returns
# a list of attractions that fit within it. No travel time, no multi-day,
# no transport mode. The frontend never calls this; kept only for reference.
# Remove together with ItineraryRequest once /plan-optimized is live.
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# TO BE REPLACED — POST /itinerary/generate
# Sprint 2 I3 multi-day planner. Accepts place_ids in the order the frontend
# sent them (click order) and packs them greedily into days.
# Will be replaced by /plan-optimized once the frontend is updated.
# Remove together with ItineraryPlanRequest at that point.
# ---------------------------------------------------------------------------
@router.post("/generate")
async def generate_itinerary(request: ItineraryPlanRequest, db: Session = Depends(get_db)):
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


# ---------------------------------------------------------------------------
# CURRENT — POST /itinerary/plan-optimized
# Backend-driven itinerary planner. Receives an unordered pool of place_ids
# and handles ordering, time windows, per-day intensity, anchor-based routing,
# and validation warnings. Steps added incrementally:
#   Step 1 (done):  schema + skeleton
#   Step 2 (done):  per-day time windows + per-day intensity
#   Step 3 (done):  validation warnings (intensity vs window, inter-day rest)
#   Step 4:         anchor resolution (Stary Rynek default, prev/next day logic)
#   Step 5:         route optimization (nearest-neighbor + 2-opt)
#   Step 6:         Google finalization endpoint for accurate travel times
# ---------------------------------------------------------------------------
@router.post("/plan-optimized")
async def plan_optimized(request: OptimizedItineraryRequest, db: Session = Depends(get_db)):
    places = db.query(Place).filter(Place.id.in_(request.place_ids)).all()

    if not places:
        raise HTTPException(status_code=404, detail="No places found for given IDs")

    by_id = {p.id: p for p in places}
    attractions = [place_to_attraction(by_id[pid]) for pid in request.place_ids if pid in by_id]

    # Serialize days_config to plain dicts so planner_service has no Pydantic dependency.
    days_config = [
        dc.model_dump() if dc is not None else None
        for dc in request.days_config
    ] if request.days_config else None

    return build_optimized_itinerary(
        attractions,
        num_days=request.num_days,
        global_intensity=request.intensity,
        global_start_time=request.start_time,
        global_end_time=request.end_time,
        transport_mode=request.transport_mode,
        break_duration_minutes=request.break_duration_minutes,
        days_config=days_config,
    )
