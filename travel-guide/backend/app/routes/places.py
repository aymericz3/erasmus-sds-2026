"""
Places API routes.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.schemas.place import PlaceOut
from app.services.place_service import get_places

router = APIRouter()

# List places with an optional category filter
@router.get("/places", response_model=list[PlaceOut])
def list_places(
    category: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return get_places(db, category=category)
