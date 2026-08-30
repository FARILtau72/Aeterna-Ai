"""
AETERNA AI — Curated News Router
"""

from fastapi import APIRouter
from services.news_service import get_curated_news

router = APIRouter(tags=["News"])

@router.get("/api/v1/news")
async def get_latest_news():
    """Returns curated static reference articles about waste management in DKI Jakarta."""
    return get_curated_news()
