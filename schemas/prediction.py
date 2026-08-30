"""
AETERNA AI — Prediction Request & Response Schemas
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from core.config import ALLOWED_LOCATIONS
from schemas.logistics import LogisticsPlan

class PredictionRequest(BaseModel):
    forecast_days: int = Field(7, ge=1, le=30, description="Forecast horizon in days (1-30)")
    rainfall_mm: float = Field(0.0, ge=0, description="Precipitation override. 0.0 means Auto (Open-Meteo)")
    event_scale: Optional[int] = Field(0, ge=0, description="Legacy crowd scale (optional fallback)")
    jumlah_jiwa: Optional[int] = Field(None, ge=0, description="Target headcount / population override (Jumlah Jiwa)")
    location: str = Field(..., description="Target sub-district (Kecamatan)")
    start_date: Optional[str] = Field(None, description="Start date: YYYY-MM-DD")
    granularity: str = Field("daily", pattern="^(daily|hourly)$", description="Granularity")
    model_type: str = Field("chronos", pattern="^(chronos|gradient_boosting)$", description="AI model type")

    @field_validator("location")
    @classmethod
    def validate_location(cls, v: str) -> str:
        if v not in ALLOWED_LOCATIONS:
            raise ValueError(f"Kecamatan '{v}' not recognized. Use one of the 44 sub-districts in Jakarta.")
        return v

class PredictionResult(BaseModel):
    date: str
    location: str
    total_volume_ton: float
    organic_waste_ton: float
    plastic_waste_ton: float
    paper_waste_ton: float
    metal_waste_ton: float
    glass_waste_ton: float
    textile_waste_ton: float
    other_waste_ton: float
    recommended_trucks: int
    risk_status: str
    event_info: Optional[str] = None
    hourly_breakdown: Optional[List[Dict[str, Any]]] = None

class PredictionData(BaseModel):
    prediction_results: List[PredictionResult]
    logistics_plan: LogisticsPlan

class APIResponse(BaseModel):
    status: str
    message: str
    confidence_score: float
    data_status: str = "FORECAST"
    forecast_type: str = "MODEL_OUTPUT"
    model_version: str = "AETERNA Stacking v1.0"
    training_data_type: str = "SYNTHETIC"
    weather_source: str = "Open-Meteo (EXTERNAL_REALTIME)"
    population_source: str = "BPS DKI Jakarta 2023 (UNVERIFIED — needs validation)"
    disclaimer: str = "Forecasts are decision-support estimates derived from a research prototype trained on synthetic simulation data. Requires validation against authoritative DLH/SIPSN field data before operational deployment."
    generated_at: Optional[str] = None
    data: PredictionData
