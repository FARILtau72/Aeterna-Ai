"""
AETERNA AI — Data Source Connectors

This package provides extensible adapters for authoritative data sources.
Each adapter returns normalized records with provenance metadata.

Available connectors:
- WeatherDataSource (Open-Meteo) — ACTIVE
- BPSDataSource (BPS DKI Jakarta) — STUB (requires API key registration)
- SIPSNDataSource (SIPSN KLHK) — STUB (no public API available)
- DLHDataSource (DLH DKI Jakarta) — STUB (no public API available)
"""

from .base import BaseDataSource, DataRecord, ProvenanceType
from .weather import WeatherDataSource
from .bps import BPSDataSource
from .sipsn import SIPSNDataSource
from .dlh import DLHDataSource

__all__ = [
    "BaseDataSource",
    "DataRecord",
    "ProvenanceType",
    "WeatherDataSource",
    "BPSDataSource",
    "SIPSNDataSource",
    "DLHDataSource",
]
