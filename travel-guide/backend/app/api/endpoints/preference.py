import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.preference import Preference
from app.schemas.preference import PreferenceSaveRequest

router = APIRouter()

@router.post("/save")
async def save_preferences(request: PreferenceSaveRequest, db: Session = Depends(get_db)):
    try:
        existing_pref = db.query(Preference).filter(Preference.user_id == request.user_id).first()
        
        categories_str = json.dumps(request.selected_categories)

        if existing_pref:
            existing_pref.intensity = request.intensity
            existing_pref.transport_mode = request.transport_mode
            existing_pref.break_duration_minutes = request.break_duration_minutes
            existing_pref.start_time = request.start_time
            existing_pref.selected_categories = categories_str
            db.commit()
            return {"status": "success", "message": "Preferences updated successfully"}
        
        new_pref = Preference(
            user_id=request.user_id,
            intensity=request.intensity,
            transport_mode=request.transport_mode,
            break_duration_minutes=request.break_duration_minutes,
            start_time=request.start_time,
            selected_categories=categories_str
        )
        db.add(new_pref)
        db.commit()
        return {"status": "success", "message": "Preferences saved successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save preferences due to server error")
    
@router.get("/load/{user_id}")
async def load_preferences(user_id: int, db: Session = Depends(get_db)):
    try:
        pref = db.query(Preference).filter(Preference.user_id == user_id).first()
        
        if not pref:
            return {
                "status": "success",
                "is_new_user": True,
                "preferences": {
                    "intensity": "moderate",
                    "transport_mode": "walking",
                    "break_duration_minutes": 30,
                    "start_time": "09:00",
                    "selected_categories": []
                }
            }
            
        try:
            categories_list = json.loads(pref.selected_categories) if pref.selected_categories else []
        except:
            categories_list = []
            
        return {
            "status": "success",
            "is_new_user": False,
            "preferences": {
                "intensity": pref.intensity,
                "transport_mode": pref.transport_mode,
                "break_duration_minutes": pref.break_duration_minutes,
                "start_time": pref.start_time,
                "selected_categories": categories_list
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to load preferences due to server error")