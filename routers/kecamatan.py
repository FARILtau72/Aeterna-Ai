"""
AETERNA AI — Kecamatan Metadata Router (Dynamic Single Source of Truth)
"""

from fastapi import APIRouter, HTTPException
from core.config import KECAMATAN_DATABASE
from schemas.kecamatan import KecamatanListResponse

router = APIRouter(tags=["Kecamatan Metadata"])

@router.get("/api/v1/kecamatan", response_model=KecamatanListResponse)
def list_all_kecamatan():
    """Retrieve full metadata for all 44 sub-districts (coordinates, baseline, population)."""
    return {
        "status": "success",
        "count": len(KECAMATAN_DATABASE),
        "data": KECAMATAN_DATABASE
    }

@router.get("/api/v1/kecamatan/{location}")
def get_kecamatan_detail(location: str):
    """Retrieve metadata for a specific sub-district."""
    if location not in KECAMATAN_DATABASE:
        raise HTTPException(404, f"Kecamatan '{location}' not found.")
    return {
        "status": "success",
        "location": location,
        "data": KECAMATAN_DATABASE[location]
    }
