"""
Unit Tests for AETERNA AI Operational Logistics Engine
Validates transparent fleet sizing, crew allocation, throughput-based collection duration,
operational efficiency, and zero/large volume edge cases.
"""

import pytest
import math
from services.logistics_engine import (
    LOGISTICS_CONFIG,
    calculate_fleet_requirements,
    calculate_manpower_requirements,
    calculate_collection_time,
    calculate_operational_efficiency_score,
    calculate_forecast_reliability_score,
    calculate_full_logistics_plan
)


def test_1_fleet_calculation():
    """
    Test 1: Fleet Calculation for forecast = 1135.63 ton.
    Verifies dimensional correctness and transparent formula:
    effective_capacity = 15.0 * 0.95 = 14.25 ton
    base_trucks = ceil(1135.63 / 14.25) = 80
    recommended_trucks = ceil(80 * 1.05) = 84
    required_truck_loads = 1135.63 / 15.0 = 75.71
    """
    forecast = 1135.63
    fleet = calculate_fleet_requirements(forecast)

    assert fleet["truck_capacity_ton"] == 15.0
    assert fleet["load_factor"] == 0.95
    assert fleet["effective_capacity_ton"] == 14.25
    assert fleet["base_trucks"] == 80
    assert fleet["operational_buffer_percent"] == 5.0
    assert fleet["recommended_trucks"] == 84
    assert fleet["required_truck_loads"] == 75.71


def test_2_manpower_calculation():
    """
    Test 2: Manpower staffing derived directly from recommended fleet.
    Standard crew: 1 driver + 2 collectors = 3 personnel per truck.
    """
    # Test with 80 base trucks
    manpower_80 = calculate_manpower_requirements(80)
    assert manpower_80["drivers"] == 80
    assert manpower_80["collectors"] == 160
    assert manpower_80["total_personnel"] == 240
    assert manpower_80["crew_per_truck"] == 3

    # Test with 84 recommended trucks
    manpower_84 = calculate_manpower_requirements(84)
    assert manpower_84["drivers"] == 84
    assert manpower_84["collectors"] == 168
    assert manpower_84["total_personnel"] == 252
    assert manpower_84["total_personnel"] == 84 * 3


def test_3_collection_time_uses_throughput_not_volume_div_capacity():
    """
    Test 3: Collection time MUST use fleet throughput, NOT volume / truck_capacity.
    Volume / 15 gives 75.7 (which is truck loads, NOT hours).
    Throughput = recommended_trucks * collection_rate_ton_per_hour (2.0 T/h).
    """
    forecast = 1135.63
    truck_capacity = 15.0
    faulty_time = forecast / truck_capacity  # 75.70866...

    rec_trucks = 84
    collection = calculate_collection_time(
        forecast_volume_ton=forecast,
        recommended_trucks=rec_trucks,
        collection_rate_per_truck=2.0,
        rainfall_mm=0.0,
        has_event=False,
        operational_efficiency=0.98
    )

    # Collection time must NOT equal faulty volume / capacity
    assert collection["adjusted_hours"] != round(faulty_time, 1)
    assert collection["raw_hours"] != round(faulty_time, 1)

    # Dimensional verification:
    # fleet_throughput = 84 * 2.0 = 168.0 ton/hour
    # raw_hours = 1135.63 / 168.0 = 6.7597... ~ 6.8 hours
    assert collection["raw_hours"] == 6.8
    # adjusted_hours = (6.7597 * 1.1) / 0.98 = 7.587... ~ 7.6 hours
    assert collection["adjusted_hours"] == 7.6


def test_4_zero_forecast_handling():
    """
    Test 4: Zero forecast volume edge case.
    If forecast_volume = 0, trucks = 0, crew = 0, collection time = 0.
    """
    plan = calculate_full_logistics_plan(0.0)

    assert plan["forecast_volume_ton"] == 0.0
    assert plan["trucks_needed"] == 0
    assert plan["manpower"] == 0
    assert plan["estimated_duration_hours"] == 0.0
    assert plan["required_truck_loads"] == 0.0

    fleet = plan["recommended_fleet"]
    assert fleet["base_trucks"] == 0
    assert fleet["recommended_trucks"] == 0
    assert fleet["required_truck_loads"] == 0.0

    crew = plan["manpower_breakdown"]
    assert crew["drivers"] == 0
    assert crew["collectors"] == 0
    assert crew["total_personnel"] == 0


def test_5_large_volume_scaling():
    """
    Test 5: Large volume handling without hardcoded limits.
    For citywide 10,000 tons surge, all formulas scale consistently.
    """
    large_volume = 10000.0
    plan = calculate_full_logistics_plan(large_volume)

    # Effective capacity = 14.25
    expected_base_trucks = math.ceil(10000.0 / 14.25)  # 702
    expected_rec_trucks = math.ceil(expected_base_trucks * 1.05)  # 738
    expected_personnel = expected_rec_trucks * 3  # 2214

    assert plan["recommended_fleet"]["base_trucks"] == expected_base_trucks
    assert plan["recommended_fleet"]["recommended_trucks"] == expected_rec_trucks
    assert plan["manpower"] == expected_personnel
    assert plan["required_truck_loads"] == round(10000.0 / 15.0, 2)
    assert plan["estimated_duration_hours"] > 0.0
    assert plan["operational_efficiency"]["score_percent"] > 0.0


def test_6_operational_factors_adjustment():
    """
    Test 6: Real-world adjustments (rain, traffic, events) affect collection duration.
    Heavy rain (>25mm) and event crowd increase estimated duration.
    """
    base_plan = calculate_collection_time(
        forecast_volume_ton=1000.0,
        recommended_trucks=50,
        rainfall_mm=0.0,
        has_event=False,
        operational_efficiency=0.85
    )

    rain_event_plan = calculate_collection_time(
        forecast_volume_ton=1000.0,
        recommended_trucks=50,
        rainfall_mm=30.0,  # Heavy rain (factor 1.20)
        has_event=True,    # Event crowd (factor 1.10)
        operational_efficiency=0.85
    )

    assert rain_event_plan["adjusted_hours"] > base_plan["adjusted_hours"]
    assert rain_event_plan["factors"]["weather_factor"] == 1.20
    assert rain_event_plan["factors"]["event_factor"] == 1.10
