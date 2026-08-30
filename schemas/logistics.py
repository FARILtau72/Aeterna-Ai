"""
AETERNA AI — Logistics Plan & Operational Simulation Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class FleetBreakdown(BaseModel):
    truck_capacity_ton: float = 15.0
    load_factor: float = 0.95
    effective_capacity_ton: float = 14.25
    base_trucks: int
    operational_buffer_percent: float = 5.0
    recommended_trucks: int
    required_truck_loads: float

class ManpowerBreakdown(BaseModel):
    drivers: int
    collectors: int
    total_personnel: int
    crew_per_truck: int = 3

class CollectionTimeBreakdown(BaseModel):
    raw_hours: float
    adjusted_hours: float
    collection_rate_ton_per_hour_per_truck: float = 2.0
    average_trips_per_truck: float
    factors: Dict[str, float]

class OperationalEfficiencyBreakdown(BaseModel):
    score_percent: float
    status: str
    display: str
    breakdown: Dict[str, float]

class ReliabilityBreakdown(BaseModel):
    score_percent: float
    display: str
    label: str
    breakdown: Dict[str, float]

class UIPresentation(BaseModel):
    recommended_fleet_display: str
    fleet_subtitle: str
    crew_display: str
    crew_subtitle: str
    collection_time_display: str
    collection_time_subtitle: str
    truck_loads_display: str
    efficiency_display: str
    reliability_display: str

class LogisticsPlan(BaseModel):
    forecast_volume_ton: Optional[float] = None
    trucks_needed: int
    manpower: int
    estimated_duration_hours: float
    efficiency_rate: str
    required_truck_loads: Optional[float] = None
    recommended_fleet: Optional[FleetBreakdown] = None
    manpower_breakdown: Optional[ManpowerBreakdown] = None
    collection_time: Optional[CollectionTimeBreakdown] = None
    operational_factors: Optional[Dict[str, float]] = None
    operational_efficiency: Optional[OperationalEfficiencyBreakdown] = None
    reliability: Optional[ReliabilityBreakdown] = None
    ui_presentation: Optional[UIPresentation] = None
    operational_assumptions: Optional[Dict[str, Any]] = None
    calculation_method: Optional[str] = None
