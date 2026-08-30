"""
AETERNA AI — Alert Schemas
"""

from pydantic import BaseModel
from typing import List, Dict, Any

class AlertItem(BaseModel):
    date: str
    location: str
    status: str
    estimated_volume_ton: float
    message: str

class AlertResponse(BaseModel):
    status: str
    alert_count: int
    alerts: List[Dict[str, Any]]
    last_updated: str
