from fastapi import APIRouter
from app.core.constants import CATEGORIES

router = APIRouter()

@router.get("/categories")
def list_categories():
    return CATEGORIES