"""
Place service used for business logic related to places.
"""

from sqlalchemy.orm import Session
from typing import Optional

from app.models.place import Place

# Get places with an optional list of category filters
def get_places(db: Session, categories: Optional[list[str]] = None) -> list[Place]:
    query = db.query(Place)
    if categories:
        query = query.filter(Place.category.in_(categories))
    return query.all()
