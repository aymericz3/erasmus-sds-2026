"""
Place model used for database representation of places.
"""

from sqlalchemy import Column, Integer, Float, Text
from app.db.session import Base


class Place(Base):
    __tablename__ = "places"

    id            = Column(Integer, primary_key=True)
    name_en       = Column(Text)
    name_pl       = Column(Text)
    category      = Column(Text, nullable=False)
    description   = Column(Text)
    opening_hours = Column(Text)
    duration      = Column(Text)
    price_range   = Column(Text)
    image_url     = Column(Text)
    latitude      = Column(Float)
    longitude     = Column(Float)

    # Enrichment fields (OpenStreetMap + Wikipedia) — see scripts/enrich_places.py
    address           = Column(Text)
    website           = Column(Text)
    osm_id            = Column(Text)
    wikipedia_title   = Column(Text)
    image_attribution = Column(Text)
    source            = Column(Text)
