"""
Place service used for business logic related to places.
"""

from sqlalchemy.orm import Session
from typing import Optional

from app.models.place import Place

# Get places with an optional category filter
def get_places(db: Session, category: Optional[str] = None) -> list[Place]:
    query = db.query(Place)
    if category:
        query = query.filter(Place.category == category)
    return query.all()
