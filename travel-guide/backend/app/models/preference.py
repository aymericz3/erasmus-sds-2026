from sqlalchemy import Column, Integer, Text
from app.db.session import Base

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    intensity = Column(Text, default="moderate")
    transport_mode = Column(Text, default="walking")
    break_duration_minutes = Column(Integer, default=30)
    start_time = Column(Text, default="09:00")
    selected_categories = Column(Text)