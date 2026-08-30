import pytest
from app import APIResponse, PredictionData, LogisticsPlan

def test_api_response_provenance_fields():
    """Verify that the APIResponse schema includes scientific provenance fields."""
    schema = APIResponse.model_json_schema()
    props = schema["properties"]
    
    assert "data_status" in props
    assert "forecast_type" in props
    assert "model_version" in props
    assert "training_data_type" in props
    assert "disclaimer" in props

def test_logistics_plan_schema():
    """Verify LogisticsPlan includes operational assumptions."""
    schema = LogisticsPlan.model_json_schema()
    props = schema["properties"]
    
    assert "operational_assumptions" in props
    assert "calculation_method" in props

def test_kecamatan_registry_json_integrity():
    """Verify that config/kecamatan_registry.json contains exactly 44 sub-districts with valid metadata."""
    from core.config import KECAMATAN_DATABASE, ALLOWED_LOCATIONS
    assert len(KECAMATAN_DATABASE) == 44, f"Expected 44 kecamatan, got {len(KECAMATAN_DATABASE)}"
    assert len(ALLOWED_LOCATIONS) == 44
    assert "Menteng" in KECAMATAN_DATABASE
    assert "Cakung" in KECAMATAN_DATABASE
    assert "Penjaringan" in KECAMATAN_DATABASE
    assert "Cengkareng" in KECAMATAN_DATABASE
    
    for loc, info in KECAMATAN_DATABASE.items():
        assert "latitude" in info
        assert "longitude" in info
        assert "population_jiwa" in info
        assert "normal_avg" in info
        assert "city" in info
        assert "zone" in info
