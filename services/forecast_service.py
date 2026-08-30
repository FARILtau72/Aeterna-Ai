"""
AETERNA AI — Machine Learning Forecasting & Hourly Breakdown Service
"""

import hashlib
import numpy as np
import pandas as pd
import torch
from datetime import timedelta
from typing import List, Dict, Any, Tuple
from fastapi.concurrency import run_in_threadpool

from config.settings import HOURLY_PATTERN, COMPOSITION_RATIOS, ZONE_MAPPING
from core.config import KECAMATAN_DATABASE
from core.timezone import get_jakarta_now, parse_flexible_date
import core.model_loader as ml
from services.weather_service import fetch_rainfall_forecast
from services.logistics_engine import calculate_fleet_requirements, calculate_full_logistics_plan
from schemas.prediction import PredictionRequest, PredictionResult, PredictionData, APIResponse, LogisticsPlan
from schemas.logistics import (
    FleetBreakdown, ManpowerBreakdown, CollectionTimeBreakdown,
    OperationalEfficiencyBreakdown, ReliabilityBreakdown, UIPresentation
)

def get_risk_status(volume: float, location: str) -> str:
    config = KECAMATAN_DATABASE.get(location, KECAMATAN_DATABASE["Menteng"])
    norm = config["normal_avg"]
    if volume > norm * 1.30:
        return "CRITICAL"
    elif volume > norm * 1.12:
        return "WARNING"
    return "SAFE"

def distribute_to_hourly(daily_volume: float) -> List[Dict[str, Any]]:
    pattern = HOURLY_PATTERN.copy()
    total_factor = sum(pattern.values())
    hourly_results = []
    
    high_thresh = (daily_volume / 24) * 2.0
    med_thresh = (daily_volume / 24) * 1.2
    
    for h in range(24):
        vol = round(daily_volume * (pattern[h] / total_factor), 2)
        risk = "HIGH" if vol > high_thresh else "MEDIUM" if vol > med_thresh else "LOW"
        
        hourly_results.append({
            "hour": f"{h:02d}:00",
            "estimated_volume_ton": vol,
            "risk_indicator": risk,
            "confidence_range": {"lower": round(vol * 0.85, 2), "upper": round(vol * 1.15, 2)}
        })
    return hourly_results

def perform_chronos_inference(ctx: torch.Tensor, steps: int) -> np.ndarray:
    torch.manual_seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(42)
    forecast = ml.pipeline.predict(ctx.unsqueeze(0), steps)
    return np.quantile(forecast[0].numpy(), 0.5, axis=0)

async def generate_prediction_pipeline(req: PredictionRequest) -> APIResponse:
    if ml.df_history is None or ml.pipeline is None:
        raise RuntimeError("Forecasting models not initialized.")

    start_date = parse_flexible_date(req.start_date) if req.start_date else pd.Timestamp(get_jakarta_now().date())
    config = KECAMATAN_DATABASE[req.location]
    weather_forecast = await fetch_rainfall_forecast(config["latitude"], config["longitude"], req.forecast_days)

    baseline_pop = float(config.get("population_jiwa", 100000))
    if req.jumlah_jiwa is not None and req.jumlah_jiwa > 0:
        target_pop = float(req.jumlah_jiwa)
    elif req.event_scale and req.event_scale > 0:
        target_pop = baseline_pop + (req.event_scale * 20000.0 if req.event_scale <= 5 else float(req.event_scale))
    else:
        target_pop = float(baseline_pop)

    df_loc = ml.df_history[ml.df_history["Location"] == req.location]
    if df_loc.empty:
        df_loc = ml.df_history[ml.df_history["Location"] == "Menteng"]
    df_loc = df_loc.sort_values("TANGGAL").reset_index(drop=True)

    dataset_mean = df_loc["Volume_Sampah_Ton"].mean()
    real_baseline = config["normal_avg"]
    calibration_factor = real_baseline / dataset_mean

    o_r = COMPOSITION_RATIOS["organic"]
    p_r = COMPOSITION_RATIOS["plastic"]
    paper_r = COMPOSITION_RATIOS["paper"]
    metal_r = COMPOSITION_RATIOS["metal"]
    glass_r = COMPOSITION_RATIOS["glass"]
    textile_r = COMPOSITION_RATIOS["textile"]
    other_r = COMPOSITION_RATIOS["other"]

    results = []
    total_vol = 0.0
    max_risk = "SAFE"

    # 1. Chronos Neural Time-Series
    if req.model_type == "chronos":
        ctx = torch.tensor(df_loc["Volume_Sampah_Ton"].values[-500:], dtype=torch.float32)
        forecast_vals = await run_in_threadpool(perform_chronos_inference, ctx, req.forecast_days)

        for i, base in enumerate(forecast_vals):
            curr_date = start_date + timedelta(days=i)
            d_str = curr_date.strftime("%Y-%m-%d")

            rain_val = req.rainfall_mm if (req.rainfall_mm > 0.0 and i == 0) else weather_forecast.get(d_str, 0.0)
            rain_m = 1.0
            if rain_val > 5.0:
                rain_m = 1.0 + min(rain_val * 0.002, 0.20)

            evt = ml.events_data.get(d_str)
            event_pop = 0.0
            info = None
            if evt and (req.location.lower() in evt["location"].lower() or evt["location"].lower() == "jakarta"):
                event_pop = float(evt.get("jumlah_jiwa", evt.get("crowd_scale", 0.0)))
                info = f"{evt['event_name']} ({int(event_pop):,} Jiwa) @ {evt['location']}"

            if info is None:
                if rain_val > 15.0:
                    info = f"Rain Impact ({rain_val} mm)"
                elif curr_date.weekday() >= 5:
                    info = "Weekend Activity"
                else:
                    info = "Routine Operations"

            total_day_jiwa = target_pop + event_pop
            pop_scaling_factor = total_day_jiwa / baseline_pop

            raw_prediction = base * rain_m * pop_scaling_factor
            seed_val = int(hashlib.md5(f"{d_str}_{req.location}".encode()).hexdigest(), 16)
            daily_variance = 1.0 + ((seed_val % 100) - 50) / 2000.0
            raw_prediction *= daily_variance

            calibrated_volume = round(float(raw_prediction * calibration_factor), 2)
            total_vol += calibrated_volume
            risk = get_risk_status(calibrated_volume, req.location)
            if risk == "CRITICAL":
                max_risk = "CRITICAL"
            elif risk == "WARNING" and max_risk != "CRITICAL":
                max_risk = "WARNING"

            hourly = distribute_to_hourly(calibrated_volume) if req.granularity == "hourly" else None

            results.append(PredictionResult(
                date=d_str, location=req.location, total_volume_ton=calibrated_volume,
                organic_waste_ton=round(calibrated_volume * o_r, 2), plastic_waste_ton=round(calibrated_volume * p_r, 2),
                paper_waste_ton=round(calibrated_volume * paper_r, 2), metal_waste_ton=round(calibrated_volume * metal_r, 2),
                glass_waste_ton=round(calibrated_volume * glass_r, 2), textile_waste_ton=round(calibrated_volume * textile_r, 2),
                other_waste_ton=round(calibrated_volume * other_r, 2),
                recommended_trucks=calculate_fleet_requirements(calibrated_volume)["recommended_trucks"],
                risk_status=risk, event_info=info, hourly_breakdown=hourly
            ))

    # 2. Stacking Regressor ML Engine
    elif req.model_type == "gradient_boosting":
        if ml.model_gbr is None:
            raise RuntimeError("Stacking Regressor model not initialized.")

        zone_code = ZONE_MAPPING.get(config.get("zone", "Pusat Komersial"), 1)

        for i in range(req.forecast_days):
            curr_date = start_date + timedelta(days=i)
            d_str = curr_date.strftime("%Y-%m-%d")

            rain_val = req.rainfall_mm if (req.rainfall_mm > 0.0 and i == 0) else weather_forecast.get(d_str, 0.0)
            rain_lag1 = req.rainfall_mm if (req.rainfall_mm > 0.0 and i == 1) else weather_forecast.get((curr_date - timedelta(days=1)).strftime("%Y-%m-%d"), 0.0)

            evt = ml.events_data.get(d_str)
            event_pop = 0.0
            info = None
            if evt and (req.location.lower() in evt["location"].lower() or evt["location"].lower() == "jakarta"):
                event_pop = float(evt.get("jumlah_jiwa", evt.get("crowd_scale", 0.0)))
                info = f"{evt['event_name']} ({int(event_pop):,} Jiwa) @ {evt['location']}"

            if info is None:
                if rain_val > 15.0:
                    info = f"Rain Impact ({rain_val} mm)"
                elif curr_date.weekday() >= 5:
                    info = "Weekend Activity"
                else:
                    info = "Routine Operations"

            total_day_jiwa = target_pop + event_pop
            has_event = 1 if (event_pop > 0) else 0

            m_val = curr_date.month
            is_mudik = 1 if ((m_val == 4 and 5 <= curr_date.day <= 18) or (m_val == 3 and 25 <= curr_date.day <= 31)) else 0

            features = pd.DataFrame([{
                'Population_Jiwa': total_day_jiwa,
                'Normal_Avg_Ton': float(config["normal_avg"]),
                'Zone_Type_Code': zone_code,
                'Rainfall_mm': float(rain_val),
                'Rain_Lag_1': float(rain_lag1),
                'Is_Weekend': 1 if curr_date.weekday() >= 5 else 0,
                'Hari_Dalam_Minggu': curr_date.weekday(),
                'Bulan': curr_date.month,
                'Is_Mudik': is_mudik,
                'Ada_Event': has_event,
                'Event_Crowd_Headcount': float(event_pop)
            }])

            raw_pred = float(ml.model_gbr.predict(features)[0])
            pop_extrapolate_factor = target_pop / baseline_pop
            raw_pred *= pop_extrapolate_factor

            seed_val = int(hashlib.md5(f"{d_str}_{req.location}".encode()).hexdigest(), 16)
            daily_variance = 1.0 + ((seed_val % 100) - 50) / 2000.0
            raw_pred *= daily_variance

            calibrated_volume = round(max(0.1, raw_pred), 2)
            total_vol += calibrated_volume
            risk = get_risk_status(calibrated_volume, req.location)
            if risk == "CRITICAL":
                max_risk = "CRITICAL"
            elif risk == "WARNING" and max_risk != "CRITICAL":
                max_risk = "WARNING"

            hourly = distribute_to_hourly(calibrated_volume) if req.granularity == "hourly" else None

            results.append(PredictionResult(
                date=d_str, location=req.location, total_volume_ton=calibrated_volume,
                organic_waste_ton=round(calibrated_volume * o_r, 2), plastic_waste_ton=round(calibrated_volume * p_r, 2),
                paper_waste_ton=round(calibrated_volume * paper_r, 2), metal_waste_ton=round(calibrated_volume * metal_r, 2),
                glass_waste_ton=round(calibrated_volume * glass_r, 2), textile_waste_ton=round(calibrated_volume * textile_r, 2),
                other_waste_ton=round(calibrated_volume * other_r, 2),
                recommended_trucks=calculate_fleet_requirements(calibrated_volume)["recommended_trucks"],
                risk_status=risk, event_info=info, hourly_breakdown=hourly
            ))

    # Unified Deterministic Operational Logistics Plan
    avg_rainfall = float(np.mean(list(weather_forecast.values()))) if weather_forecast else float(req.rainfall_mm)
    has_any_event = any(r.event_info is not None for r in results)
    test_mape = float(ml.model_meta.get("metrics", {}).get("mape", 6.12)) if ml.model_meta else 6.12

    logistics_dict = calculate_full_logistics_plan(
        total_forecast_volume_ton=total_vol,
        forecast_days=req.forecast_days,
        rainfall_mm=avg_rainfall,
        has_event=has_any_event,
        is_rush_hour=False,
        test_mape=test_mape,
        has_live_weather=(len(weather_forecast) > 0),
        has_verified_bps=True
    )

    conf = round(logistics_dict["reliability"]["score_percent"] / 100.0, 2)
    msg = f"CRITICAL at {req.location}!" if max_risk == "CRITICAL" else f"WARNING at {req.location}." if max_risk == "WARNING" else "Normal conditions."

    return APIResponse(
        status="success", message=msg, confidence_score=conf,
        data=PredictionData(
            prediction_results=results,
            logistics_plan=LogisticsPlan(
                forecast_volume_ton=logistics_dict["forecast_volume_ton"],
                trucks_needed=logistics_dict["trucks_needed"],
                manpower=logistics_dict["manpower"],
                estimated_duration_hours=logistics_dict["estimated_duration_hours"],
                efficiency_rate=logistics_dict["efficiency_rate"],
                required_truck_loads=logistics_dict["required_truck_loads"],
                recommended_fleet=FleetBreakdown(**logistics_dict["recommended_fleet"]),
                manpower_breakdown=ManpowerBreakdown(**logistics_dict["manpower_breakdown"]),
                collection_time=CollectionTimeBreakdown(**logistics_dict["collection_time"]),
                operational_factors=logistics_dict["operational_factors"],
                operational_efficiency=OperationalEfficiencyBreakdown(**logistics_dict["operational_efficiency"]),
                reliability=ReliabilityBreakdown(**logistics_dict["reliability"]),
                ui_presentation=UIPresentation(**logistics_dict["ui_presentation"]),
                operational_assumptions=logistics_dict.get("operational_assumptions"),
                calculation_method=logistics_dict.get("calculation_method")
            )
        ),
        generated_at=get_jakarta_now().isoformat()
    )
