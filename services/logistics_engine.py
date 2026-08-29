"""
AETERNA AI — Operational Logistics Engine
Centralized, deterministic mathematical service for municipal waste logistics in DKI Jakarta.

Architecture Principle:
    AI Forecast Model (Predicted Volume)
            ↓
    Deterministic Logistics Engine (Physics & Municipal Standards)
            ↓
    Fleet / Crew / Collection Time / Efficiency / Reliability Breakdown
            ↓
    FastAPI Endpoints & Frontend Decision Intelligence Dashboard
"""

import math
from typing import Dict, Any, Optional

# ==========================================
# 1. CENTRALIZED LOGISTICS CONFIGURATION
# ==========================================
# Prototype Operational Assumptions. These values have not been validated against official DLH DKI Jakarta fleet specifications. Use for R&D and decision-support demonstration only.
LOGISTICS_CONFIG: Dict[str, Any] = {
    # Vehicle specifications
    "truck_capacity_ton": 15.0,        # Standard heavy compactor truck gross payload capacity
    "load_factor": 0.95,               # Operational target filling factor (prevent spillage/overload)
    "effective_capacity_per_truck": 15.0 * 0.95,  # 14.25 tons effective capacity per truck-load
    "operational_buffer": 0.05,        # 5% reserve fleet buffer for maintenance, breakdown, and surges

    # Crew staffing requirements per vehicle
    "crew": {
        "drivers_per_truck": 1,        # Certified heavy vehicle driver
        "collectors_per_truck": 2,      # Sanitarian collection crew / loader helpers
        "crew_per_truck": 3            # Total personnel per deployed truck
    },

    # Operational collection throughput baseline
    # Realistic municipal collection throughput in urban Indonesian residential/commercial zones:
    # 1 truck with 3 crew collects approximately 2.0 metric tons of municipal waste per working hour.
    "collection_rate_ton_per_hour": 2.0,

    # Environmental and urban traffic adjustments
    "factors": {
        "baseline_traffic": 1.10,      # Average urban transit congestion delay factor (+10%)
        "rush_hour_traffic": 1.25,     # Peak commercial/business hours delay factor (+25%)
        "normal_weather": 1.00,        # Clear / dry asphalt road condition
        "light_rain": 1.05,            # Precipitation 0.1 - 10.0 mm (+5% caution slowdown)
        "moderate_rain": 1.10,         # Precipitation 10.1 - 25.0 mm (+10% spray/drainage slowdown)
        "heavy_rain": 1.20,            # Precipitation > 25.0 mm (+20% hydroplaning/flooding slowdown)
        "no_event": 1.00,              # Standard daily routine operations
        "event_crowd": 1.10            # Mass public gathering / car free day / festival perimeter (+10%)
    },

    # Multi-factor weights for Operational Efficiency Score (Sum = 1.00)
    "weights_efficiency": {
        "fleet_adequacy": 0.35,        # 35%: Ratio of allocated capacity vs forecast demand
        "weather_condition": 0.20,     # 20%: Weather impact on transit and loading speed
        "traffic_condition": 0.20,     # 20%: Road network throughput & traffic speed
        "event_impact": 0.15,          # 15%: Localized public events congestion
        "capacity_utilization": 0.10   # 10%: Proximity to optimal payload load factor
    },

    # Weights for Forecast Reliability Score (Confidence Score) (Sum = 1.00)
    "weights_reliability": {
        "model_quality": 0.50,         # 50%: Historical out-of-sample MAPE / R2 performance
        "data_completeness": 0.30,     # 30%: Weather API live stream & BPS demographic verification
        "horizon_penalty": 0.20        # 20%: Uncertainty propagation over forecast horizon days
    }
}


def calculate_fleet_requirements(
    forecast_volume_ton: float,
    truck_capacity_ton: Optional[float] = None,
    load_factor: Optional[float] = None,
    operational_buffer: Optional[float] = None
) -> Dict[str, Any]:
    """
    Calculate transparent recommended fleet sizing based on forecast tonnage.

    Formula:
        truck_loads = forecast_volume_ton / truck_capacity_ton
        effective_capacity = truck_capacity_ton * load_factor
        base_trucks = ceil(forecast_volume_ton / effective_capacity)
        recommended_trucks = ceil(base_trucks * (1 + operational_buffer))
    """
    cap = float(truck_capacity_ton if truck_capacity_ton is not None else LOGISTICS_CONFIG["truck_capacity_ton"])
    lf = float(load_factor if load_factor is not None else LOGISTICS_CONFIG["load_factor"])
    buf = float(operational_buffer if operational_buffer is not None else LOGISTICS_CONFIG["operational_buffer"])

    effective_cap = cap * lf

    if forecast_volume_ton <= 0.0:
        return {
            "truck_capacity_ton": round(cap, 1),
            "load_factor": round(lf, 2),
            "effective_capacity_ton": round(effective_cap, 2),
            "base_trucks": 0,
            "operational_buffer_percent": round(buf * 100, 1),
            "recommended_trucks": 0,
            "required_truck_loads": 0.0
        }

    truck_loads = forecast_volume_ton / cap
    base_trucks = math.ceil(forecast_volume_ton / effective_cap)
    recommended_trucks = math.ceil(base_trucks * (1.0 + buf))

    return {
        "truck_capacity_ton": round(cap, 1),
        "load_factor": round(lf, 2),
        "effective_capacity_ton": round(effective_cap, 2),
        "base_trucks": base_trucks,
        "operational_buffer_percent": round(buf * 100, 1),
        "recommended_trucks": recommended_trucks,
        "required_truck_loads": round(truck_loads, 2)
    }


def calculate_manpower_requirements(
    recommended_trucks: int,
    drivers_per_truck: Optional[int] = None,
    collectors_per_truck: Optional[int] = None
) -> Dict[str, Any]:
    """
    Derive exact staffing headcount from active fleet requirements.

    Formula:
        crew_per_truck = drivers_per_truck + collectors_per_truck (3)
        total_personnel = recommended_trucks * crew_per_truck
    """
    drivers_unit = int(drivers_per_truck if drivers_per_truck is not None else LOGISTICS_CONFIG["crew"]["drivers_per_truck"])
    collectors_unit = int(collectors_per_truck if collectors_per_truck is not None else LOGISTICS_CONFIG["crew"]["collectors_per_truck"])
    crew_unit = drivers_unit + collectors_unit

    if recommended_trucks <= 0:
        return {
            "drivers": 0,
            "collectors": 0,
            "total_personnel": 0,
            "crew_per_truck": crew_unit
        }

    drivers = recommended_trucks * drivers_unit
    collectors = recommended_trucks * collectors_unit
    total_personnel = recommended_trucks * crew_unit

    return {
        "drivers": drivers,
        "collectors": collectors,
        "total_personnel": total_personnel,
        "crew_per_truck": crew_unit
    }


def calculate_collection_time(
    forecast_volume_ton: float,
    recommended_trucks: int,
    collection_rate_per_truck: Optional[float] = None,
    rainfall_mm: float = 0.0,
    has_event: bool = False,
    is_rush_hour: bool = False,
    operational_efficiency: float = 0.85
) -> Dict[str, Any]:
    """
    Calculate estimated collection duration based on fleet throughput, NOT volume / truck capacity.

    Concept:
        Fleet Throughput = Number of Trucks * Collection Rate per Truck (ton/hour)
        Raw Collection Hours = Forecast Volume / Fleet Throughput
        Adjustment Factor = Traffic Factor * Weather Factor * Event Factor
        Adjusted Hours = (Raw Hours * Adjustment Factor) / Operational Efficiency

    Trip Logic:
        If truck_loads > recommended_trucks, multiple trips per truck are required.
        Additional transit turnaround time is incorporated for multi-trip logistics cycles.
    """
    rate = float(collection_rate_per_truck if collection_rate_per_truck is not None else LOGISTICS_CONFIG["collection_rate_ton_per_hour"])
    cap = float(LOGISTICS_CONFIG["truck_capacity_ton"])

    if forecast_volume_ton <= 0.0 or recommended_trucks <= 0:
        return {
            "raw_hours": 0.0,
            "adjusted_hours": 0.0,
            "collection_rate_ton_per_hour_per_truck": round(rate, 1),
            "average_trips_per_truck": 0.0,
            "factors": {
                "traffic_factor": 1.0,
                "weather_factor": 1.0,
                "event_factor": 1.0,
                "operational_efficiency": round(operational_efficiency, 2)
            }
        }

    # 1. Fleet Aggregate Throughput
    fleet_throughput_ton_per_hour = recommended_trucks * rate
    raw_hours = forecast_volume_ton / fleet_throughput_ton_per_hour

    # 2. Environmental Adjustment Factors
    factors_cfg = LOGISTICS_CONFIG["factors"]
    traffic_factor = factors_cfg["rush_hour_traffic"] if is_rush_hour else factors_cfg["baseline_traffic"]

    if rainfall_mm > 25.0:
        weather_factor = factors_cfg["heavy_rain"]
    elif rainfall_mm > 10.0:
        weather_factor = factors_cfg["moderate_rain"]
    elif rainfall_mm > 0.0:
        weather_factor = factors_cfg["light_rain"]
    else:
        weather_factor = factors_cfg["normal_weather"]

    event_factor = factors_cfg["event_crowd"] if has_event else factors_cfg["no_event"]

    # 3. Trip Logic: check if trips per vehicle exceed 1.0
    truck_loads = forecast_volume_ton / cap
    average_trips_per_truck = truck_loads / recommended_trucks

    # If trucks need to perform multiple turnaround trips, add standard 1.25 hours transit turnaround
    additional_trip_hours = 0.0
    if average_trips_per_truck > 1.0:
        additional_trips = average_trips_per_truck - 1.0
        additional_trip_hours = additional_trips * 1.25

    # 4. Composite Adjusted Collection Time
    eff = max(0.10, operational_efficiency)
    adjusted_hours = ((raw_hours + additional_trip_hours) * (traffic_factor * weather_factor * event_factor)) / eff

    return {
        "raw_hours": round(raw_hours, 1),
        "adjusted_hours": round(adjusted_hours, 1),
        "collection_rate_ton_per_hour_per_truck": round(rate, 1),
        "average_trips_per_truck": round(average_trips_per_truck, 2),
        "factors": {
            "traffic_factor": round(traffic_factor, 2),
            "weather_factor": round(weather_factor, 2),
            "event_factor": round(event_factor, 2),
            "operational_efficiency": round(eff, 2)
        }
    }


def calculate_operational_efficiency_score(
    recommended_trucks: int,
    forecast_volume_ton: float,
    rainfall_mm: float = 0.0,
    has_event: bool = False,
    is_rush_hour: bool = False
) -> Dict[str, Any]:
    """
    Calculate dynamic Operational Efficiency Score based on weighted real-world operational factors.

    Weights:
        Fleet Adequacy (35%)
        Weather Condition (20%)
        Traffic Condition (20%)
        Event Impact (15%)
        Capacity Utilization (10%)
    """
    weights = LOGISTICS_CONFIG["weights_efficiency"]
    cap = LOGISTICS_CONFIG["truck_capacity_ton"]
    effective_cap = LOGISTICS_CONFIG["effective_capacity_per_truck"]

    if forecast_volume_ton <= 0.0:
        return {
            "score_percent": 100.0,
            "status": "Optimal",
            "display": "100% — Optimal",
            "breakdown": {
                "fleet_adequacy": 100.0,
                "weather_condition": 100.0,
                "traffic_condition": 100.0,
                "event_impact": 100.0,
                "capacity_utilization": 100.0
            }
        }

    # 1. Fleet Adequacy Score (0-100)
    total_effective_allocated = recommended_trucks * effective_cap
    coverage_ratio = total_effective_allocated / forecast_volume_ton if forecast_volume_ton > 0 else 1.0
    if coverage_ratio >= 1.0:
        fleet_score = 100.0
    else:
        fleet_score = max(20.0, coverage_ratio * 100.0)

    # 2. Weather Condition Score (0-100)
    if rainfall_mm > 25.0:
        weather_score = 50.0   # Heavy rain / flood alert
    elif rainfall_mm > 10.0:
        weather_score = 75.0   # Moderate rain
    elif rainfall_mm > 0.0:
        weather_score = 90.0   # Light drizzle
    else:
        weather_score = 100.0  # Clear dry skies

    # 3. Traffic Condition Score (0-100)
    traffic_score = 70.0 if is_rush_hour else 90.0

    # 4. Event Impact Score (0-100)
    event_score = 75.0 if has_event else 100.0

    # 5. Capacity Utilization Score (0-100)
    if recommended_trucks > 0:
        utilization = (forecast_volume_ton / (recommended_trucks * cap)) * 100.0
        if 85.0 <= utilization <= 100.0:
            utilization_score = 100.0
        elif 70.0 <= utilization < 85.0:
            utilization_score = 88.0
        else:
            utilization_score = 75.0
    else:
        utilization_score = 50.0

    # Composite weighted efficiency score
    total_score = (
        fleet_score * weights["fleet_adequacy"] +
        weather_score * weights["weather_condition"] +
        traffic_score * weights["traffic_condition"] +
        event_score * weights["event_impact"] +
        utilization_score * weights["capacity_utilization"]
    )
    total_score = round(min(100.0, max(0.0, total_score)), 1)

    # Operational status classification
    if total_score >= 85.0:
        status = "Optimal"
    elif total_score >= 70.0:
        status = "Good"
    elif total_score >= 55.0:
        status = "Moderate"
    else:
        status = "High Operational Risk"

    return {
        "score_percent": total_score,
        "status": status,
        "display": f"{int(total_score)}% — {status}",
        "breakdown": {
            "fleet_adequacy": round(fleet_score, 1),
            "weather_condition": round(weather_score, 1),
            "traffic_condition": round(traffic_score, 1),
            "event_impact": round(event_score, 1),
            "capacity_utilization": round(utilization_score, 1)
        }
    }


def calculate_forecast_reliability_score(
    test_mape: float = 6.12,
    has_live_weather: bool = True,
    has_verified_bps: bool = True,
    forecast_days: int = 7
) -> Dict[str, Any]:
    """
    Calculate Forecast Reliability Score based on empirical model quality, data verification, and horizon decay.

    Formula:
        Reliability = Model Quality (50%) + Data Completeness (30%) + Horizon Score (20%)
    """
    weights = LOGISTICS_CONFIG["weights_reliability"]

    # 1. Model Quality Score based on out-of-sample MAPE
    # Model quality score based on out-of-sample MAPE from synthetic benchmark evaluation.
    # Note: test_mape=6.12 is a hardcoded fallback from a previous evaluation.
    model_quality = max(0.60, min(0.98, 1.0 - (test_mape / 100.0)))

    # 2. Data Completeness & Verification Score
    completeness = 1.0
    if not has_live_weather:
        completeness -= 0.15
    if not has_verified_bps:
        completeness -= 0.15
    completeness = max(0.70, completeness)

    # 3. Forecast Horizon Uncertainty Score
    if forecast_days <= 1:
        horizon_score = 1.00
    elif forecast_days <= 3:
        horizon_score = 0.96
    elif forecast_days <= 7:
        horizon_score = 0.92
    elif forecast_days <= 14:
        horizon_score = 0.85
    else:
        horizon_score = 0.78

    composite = (
        model_quality * weights["model_quality"] +
        completeness * weights["data_completeness"] +
        horizon_score * weights["horizon_penalty"]
    )
    reliability_pct = round(composite * 100.0, 1)

    return {
        "score_percent": reliability_pct,
        "display": f"{reliability_pct}%",
        "label": "Forecast Reliability Score",
        "breakdown": {
            "model_quality_score": round(model_quality * 100, 1),
            "data_completeness_score": round(completeness * 100, 1),
            "horizon_score": round(horizon_score * 100, 1)
        }
    }


def calculate_full_logistics_plan(
    total_forecast_volume_ton: float,
    forecast_days: int = 7,
    rainfall_mm: float = 0.0,
    has_event: bool = False,
    is_rush_hour: bool = False,
    test_mape: float = 6.12,
    has_live_weather: bool = True,
    has_verified_bps: bool = True
) -> Dict[str, Any]:
    """
    Generate the complete, unified Operational Logistics Plan for Aeterna AI.
    Integrates Fleet, Manpower, Throughput Collection Time, Dynamic Efficiency, and Reliability.
    """
    volume = round(float(total_forecast_volume_ton), 2)

    # 1. Fleet Requirements
    fleet = calculate_fleet_requirements(volume)
    rec_trucks = fleet["recommended_trucks"]

    # 2. Manpower Requirements
    manpower = calculate_manpower_requirements(rec_trucks)

    # 3. Dynamic Operational Efficiency
    efficiency = calculate_operational_efficiency_score(
        recommended_trucks=rec_trucks,
        forecast_volume_ton=volume,
        rainfall_mm=rainfall_mm,
        has_event=has_event,
        is_rush_hour=is_rush_hour
    )

    # 4. Collection Time based on Fleet Throughput
    collection = calculate_collection_time(
        forecast_volume_ton=volume,
        recommended_trucks=rec_trucks,
        rainfall_mm=rainfall_mm,
        has_event=has_event,
        is_rush_hour=is_rush_hour,
        operational_efficiency=efficiency["score_percent"] / 100.0
    )

    # 5. Forecast Reliability Score
    reliability = calculate_forecast_reliability_score(
        test_mape=test_mape,
        has_live_weather=has_live_weather,
        has_verified_bps=has_verified_bps,
        forecast_days=forecast_days
    )

    # Format human-friendly labels avoiding false precision
    loads_int = math.ceil(fleet["required_truck_loads"])

    return {
        "forecast_volume_ton": volume,
        # Backward-compatible fields
        "trucks_needed": rec_trucks,
        "manpower": manpower["total_personnel"],
        "estimated_duration_hours": collection["adjusted_hours"],
        "efficiency_rate": efficiency["display"],
        "required_truck_loads": fleet["required_truck_loads"],
        # Deep structured explainable modules
        "recommended_fleet": fleet,
        "manpower_breakdown": manpower,
        "collection_time": collection,
        "operational_factors": collection["factors"],
        "operational_efficiency": efficiency,
        "reliability": reliability,
        "ui_presentation": {
            "recommended_fleet_display": f"{rec_trucks} Trucks",
            "fleet_subtitle": f"{int(fleet['truck_capacity_ton'])} ton capacity / truck",
            "crew_display": f"{manpower['total_personnel']} Personnel",
            "crew_subtitle": f"{manpower['drivers']} drivers + {manpower['collectors']} collectors",
            "collection_time_display": f"{collection['adjusted_hours']} Hours",
            "collection_time_subtitle": "Adjusted for traffic, weather & events",
            "truck_loads_display": f"~{loads_int} Loads",
            "efficiency_display": efficiency["display"],
            "reliability_display": reliability["display"]
        },
        "calculation_method": "DETERMINISTIC_SIMULATION",
        "operational_assumptions": {
            "note": "Prototype Operational Assumptions — not validated against DLH specifications",
            "truck_capacity_ton": LOGISTICS_CONFIG["truck_capacity_ton"],
            "load_factor": LOGISTICS_CONFIG["load_factor"],
            "operational_buffer": LOGISTICS_CONFIG["operational_buffer"],
            "crew_per_truck": LOGISTICS_CONFIG["crew"]["crew_per_truck"],
            "collection_rate_ton_per_hour": LOGISTICS_CONFIG["collection_rate_ton_per_hour"]
        }
    }
