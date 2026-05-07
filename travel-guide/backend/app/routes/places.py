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

# List places with an optional comma-separated categories filter
# Examples: /places  /places?categories=art  /places?categories=art,sport
@router.get("/places", response_model=list[PlaceOut])
def list_places(
    categories: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    category_list = [c.strip() for c in categories.split(",")] if categories else None
    return get_places(db, categories=category_list)
