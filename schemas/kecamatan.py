"""
AETERNA AI — Kecamatan Metadata Schemas
"""

from pydantic import BaseModel
from typing import Dict, Any, List

class KecamatanDetail(BaseModel):
    name: str
    latitude: float
    longitude: float
    population_jiwa: int
    normal_avg: float
    warning_threshold: float
    critical_threshold: float
    city: str
    zone: str
    radius: str

class KecamatanListResponse(BaseModel):
    status: str
    count: int
    data: Dict[str, Dict[str, Any]]
