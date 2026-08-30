"""
AETERNA AI — Autopilot City-Wide Overview Router
"""

import hashlib
from datetime import timedelta
import pandas as pd
from fastapi import APIRouter, HTTPException

from core.config import KECAMATAN_DATABASE
from core.timezone import get_jakarta_now
from config.settings import ZONE_MAPPING
import core.model_loader as ml
from services.weather_service import fetch_rainfall_forecast
from services.logistics_engine import calculate_fleet_requirements

router = APIRouter(tags=["Autonomous"])

@router.get("/api/v1/autopilot")
async def get_autopilot_data():
    """Autonomous city-wide overview forecasting for all 44 kecamatan for today."""
    if ml.df_history is None:
        raise HTTPException(503, "Models not ready")
        
    today = get_jakarta_now()
    d_str = today.strftime("%Y-%m-%d")
    yesterday_str = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    
    total_vol = 0.0
    total_trucks = 0
    kecamatan_results = []
    rainy_count = 0
    
    evt = ml.events_data.get(d_str)
    zone_map = ml.model_meta.get("zone_map", ZONE_MAPPING)
    
    m_val = today.month
    is_mudik = 1 if ((m_val == 4 and 5 <= today.day <= 18) or (m_val == 3 and 25 <= today.day <= 31)) else 0
    
    for loc, config in KECAMATAN_DATABASE.items():
        weather_forecast = await fetch_rainfall_forecast(config["latitude"], config["longitude"], 1)
        rain_val = weather_forecast.get(d_str, 0.0)
        rain_lag1 = weather_forecast.get(yesterday_str, 0.0)
        if rain_val > 1.0:
            rainy_count += 1
            
        event_pop = 0.0
        if evt and (loc.lower() in evt["location"].lower() or evt["location"].lower() == "jakarta"):
            event_pop = float(evt.get("jumlah_jiwa", evt.get("crowd_scale", 0.0)))
            
        target_pop = float(config.get("population_jiwa", 100000))
        total_day_jiwa = target_pop + event_pop
        has_event = 1 if (event_pop > 0) else 0
        zone_code = zone_map.get(config.get("zone", "Pusat Komersial"), 1)
        
        features = pd.DataFrame([{
            'Population_Jiwa': total_day_jiwa,
            'Normal_Avg_Ton': float(config["normal_avg"]),
            'Zone_Type_Code': zone_code,
            'Rainfall_mm': float(rain_val),
            'Rain_Lag_1': float(rain_lag1),
            'Is_Weekend': 1 if today.weekday() >= 5 else 0,
            'Hari_Dalam_Minggu': today.weekday(),
            'Bulan': today.month,
            'Is_Mudik': is_mudik,
            'Ada_Event': has_event,
            'Event_Crowd_Headcount': float(event_pop)
        }])
        
        if ml.model_gbr is not None:
            raw_pred = float(ml.model_gbr.predict(features)[0])
            seed_val = int(hashlib.md5(f"{d_str}_{loc}".encode()).hexdigest(), 16)
            daily_variance = 1.0 + ((seed_val % 100) - 50) / 2000.0
            raw_pred *= daily_variance
            calibrated_volume = round(max(0.1, raw_pred), 2)
        else:
            calibrated_volume = round(float(config["normal_avg"]), 2)
            
        trucks = calculate_fleet_requirements(calibrated_volume)["recommended_trucks"]
        norm = config["normal_avg"]
        status = "CRITICAL" if calibrated_volume > norm * 1.30 else "WARNING" if calibrated_volume > norm * 1.12 else "SAFE"
        
        total_vol += calibrated_volume
        total_trucks += trucks
        
        kecamatan_results.append({
            "location": loc,
            "volume_ton": calibrated_volume,
            "trucks": trucks,
            "status": status,
            "city": config["city"],
            "latitude": config["latitude"],
            "longitude": config["longitude"]
        })
        
    kecamatan_results.sort(key=lambda x: x["volume_ton"], reverse=True)
    top_5 = kecamatan_results[:5]
    
    event_label = "Routine Operations"
    if evt:
        event_label = evt["event_name"]
    elif rainy_count > 10:
        event_label = "Heavy Rainy Weather"
    elif today.weekday() >= 5:
        event_label = "Weekend Activity"
        
    return {
        "status": "success",
        "date": d_str,
        "total_volume_ton": round(total_vol, 2),
        "total_trucks": total_trucks,
        "top_kecamatan": top_5,
        "rainy_regions": rainy_count,
        "event_today": event_label
    }
