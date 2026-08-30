"""
AETERNA AI — Alerts Router
"""

from fastapi import APIRouter, HTTPException, Query
from schemas.alert import AlertResponse
from services.alert_service import compute_alerts
from core.timezone import get_jakarta_now
import core.model_loader as ml

router = APIRouter(tags=["Alerts"])

@router.get("/api/v1/alerts", response_model=AlertResponse)
async def get_alerts(location: str = Query(None)):
    """Real-time threshold overflow warning alerts endpoint."""
    if ml.df_history is None:
        raise HTTPException(503, "Models not ready")
    
    alerts = compute_alerts(location_filter=location, horizon_days=3)
    return AlertResponse(
        status="success",
        alert_count=len(alerts),
        alerts=alerts,
        last_updated=get_jakarta_now().isoformat()
    )
