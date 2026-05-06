from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

"""
Dependency to get DB session for FastAPI routes
"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Ensure the database session is closed after use
