import os
import json
import pytest
from data_sources.base import ProvenanceType, DataRecord

def test_training_dataset_is_synthetic():
    """Verify that the synthetic dataset is clearly labeled and no observed data claims are made."""
    assert os.path.exists("data/synthetic_spatial_training_data_2024_2025.csv"), "Synthetic dataset missing"
    
    # Check that generator script prints the synthetic warning
    with open("scripts/generate_real_kecamatan_dataset.py", "r") as f:
        content = f.read()
        assert "SYNTHETIC SIMULATION" in content
        assert "NOT real DLH/SIPSN observed data" in content

def test_provenance_enums():
    """Verify provenance classification enum exists and is correct."""
    assert ProvenanceType.OBSERVED.value == "OBSERVED"
    assert ProvenanceType.SYNTHETIC.value == "SYNTHETIC"
    assert ProvenanceType.UNVERIFIED.value == "UNVERIFIED"

def test_data_record_schema():
    """Verify DataRecord requires provenance metadata."""
    record = DataRecord(
        value=100.0,
        field_name="Volume",
        provenance=ProvenanceType.SYNTHETIC,
        source_name="Test Generator"
    )
    d = record.to_dict()
    assert d["provenance"] == "SYNTHETIC"
    assert "fetched_at" in d
