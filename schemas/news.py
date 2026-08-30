"""
AETERNA AI — News Schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class NewsItem(BaseModel):
    title: str = Field(..., description="Judul berita persampahan DKI Jakarta")
    source: str = Field(..., description="Sumber penerbit berita (misal: Kompas.com, Antara News)")
    url: str = Field(..., description="Tautan/URL artikel asli berita")
    date_fetched: str = Field(..., description="Tanggal pengambilan berita (format: YYYY-MM-DD)")
    summary: str = Field(..., description="Ringkasan isi berita persampahan")

class NewsResponse(BaseModel):
    status: str
    articles: List[NewsItem]
    data_source: str
    disclaimer: str
    last_curated: str
    message: Optional[str] = None
