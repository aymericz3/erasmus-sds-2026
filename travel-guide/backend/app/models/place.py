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
