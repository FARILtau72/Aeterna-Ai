"""
AETERNA AI — Alert Service
"""

from datetime import timedelta
from typing import List, Dict, Any, Optional
from core.config import KECAMATAN_DATABASE
from core.timezone import get_jakarta_now
import core.model_loader as ml

def compute_alerts(location_filter: Optional[str] = None, horizon_days: int = 3) -> List[Dict[str, Any]]:
    """Compute active threshold warning alerts across all kecamatan for the next few days."""
    alerts = []
    today = get_jakarta_now().date()

    for i in range(horizon_days):
        d_str = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        evt = ml.events_data.get(d_str)

        for loc, config in KECAMATAN_DATABASE.items():
            if location_filter and loc != location_filter:
                continue

            baseline_vol = config["normal_avg"]
            if evt and evt.get("crowd_scale", 0) > 0 and (loc.lower() in evt["location"].lower() or evt["location"].lower() == "jakarta"):
                baseline_vol = config["normal_avg"] * 1.5

            status = "CRITICAL" if baseline_vol > config["critical_threshold"] else "WARNING" if baseline_vol > config["warning_threshold"] else "SAFE"

            if status != "SAFE":
                alerts.append({
                    "date": d_str,
                    "location": loc,
                    "status": status,
                    "estimated_volume_ton": baseline_vol,
                    "message": f"Alert: {status} volume expected at {loc}"
                })

    return alerts
