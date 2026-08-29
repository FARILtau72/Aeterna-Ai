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
