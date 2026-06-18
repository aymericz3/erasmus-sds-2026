from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.place import Place
from app.schemas.itinerary import ItineraryRequest, FinalizeRequest
from app.services.planner_service import (
    build_itinerary,
    place_to_attraction,
    rank_attractions,
    filter_places_by_preferences,
    _compute_day_items,
    _duration_minutes,
)
from app.services.transport_service import get_single_travel_time

router = APIRouter()

@router.post("/plan")
async def create_plan(request: ItineraryRequest, db: Session = Depends(get_db)):
    places = db.query(Place).filter(Place.id.in_(request.place_ids)).all()

    if not places:
        raise HTTPException(status_code=404, detail="No places found for given IDs")
    
    budget_val = getattr(request, "budget", "moderate")
    categories = getattr(request, "selected_categories", [])
    
    filtered_places = filter_places_by_preferences(places, budget_val, categories)
    ranked_places = rank_attractions(filtered_places, categories)

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
    places = db.query(Place).filter(Place.id.in_(request.place_ids)).all()

    if not places:
        raise HTTPException(status_code=404, detail="No places found for given IDs")

    budget_val = getattr(request, "budget", "moderate")
    categories = getattr(request, "selected_categories", [])
    
    filtered_places = filter_places_by_preferences(places, budget_val, categories)

    by_id = {p.id: p for p in filtered_places}
    attractions = [place_to_attraction(by_id[pid]) for pid in request.place_ids if pid in by_id]

    days_config = [
        dc.model_dump() if dc is not None else None
        for dc in request.days_config
    ] if request.days_config else None

    pins = [p.model_dump() for p in request.pins] if request.pins else None

    return build_itinerary(
        attractions,
        num_days=request.num_days,
        global_intensity=request.intensity,
        global_start_time=request.start_time,
        global_end_time=request.end_time,
        transport_mode=request.transport_mode,
        break_duration_minutes=request.break_duration_minutes,
        days_config=days_config,
        pins=pins,
        selected_categories=request.selected_categories,
    )


# ---------------------------------------------------------------------------
# POST /itinerary/finalize
# Called once the user approves the ordering from /plan.
# Replaces haversine travel estimates with real Google Distance Matrix times
# for the selected transport mode. Returns the same days shape so the frontend
# can swap the displayed times without changing its data model.
# ---------------------------------------------------------------------------
@router.post("/finalize")
async def finalize_itinerary(request: FinalizeRequest, db: Session = Depends(get_db)):
    all_ids = [pid for day in request.days for pid in day.place_ids]
    places  = db.query(Place).filter(Place.id.in_(all_ids)).all()
    if not places:
        raise HTTPException(status_code=404, detail="No places found for given IDs")
    by_id = {p.id: place_to_attraction(p) for p in places}

    result_days = []
    for day_input in request.days:
        atts = [by_id[pid] for pid in day_input.place_ids if pid in by_id]

        travel_minutes, travel_km, sources = [], [], []
        for i in range(len(atts) - 1):
            a, b = atts[i], atts[i + 1]
            if a["latitude"] and a["longitude"] and b["latitude"] and b["longitude"]:
                leg = get_single_travel_time(
                    a["latitude"], a["longitude"],
                    b["latitude"], b["longitude"],
                    request.transport_mode,
                )
                travel_minutes.append(leg["minutes"])
                travel_km.append(leg["distance_km"])
                sources.append(leg["source"])
            else:
                travel_minutes.append(0)
                travel_km.append(None)
                sources.append("estimate")

        break_durations = day_input.break_durations or [None] * max(0, len(atts) - 1)
        items = _compute_day_items(atts, travel_minutes, break_durations, day_input.start_time, travel_km)

        for item in items:
            if item["type"] == "travel":
                item["source"] = sources[item["gapIndex"]] if item["gapIndex"] < len(sources) else "estimate"

        total = sum(
            _duration_minutes(item.get("duration")) if item["type"] == "attraction"
            else item["duration"]
            for item in items
        )

        result_days.append({
            "attractions":    atts,
            "travelMinutes":  travel_minutes,
            "travelKm":       travel_km,
            "breakDurations": break_durations,
            "items":          items,
            "totalMinutes":   total,
            "transportMode":  request.transport_mode,
        })

    return {"days": result_days}
