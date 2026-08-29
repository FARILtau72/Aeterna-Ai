"""
AETERNA AI — SIPSN (Sistem Informasi Pengelolaan Sampah Nasional) Data Adapter

Status: STUB — No public REST API available
Provenance: OBSERVED (when populated with official data)
Source: https://sipsn.menlhk.go.id/
Authentication: Web interface only — no documented public API found as of 2026-08.

Available data (web interface only):
- Annual/periodic total waste tonnage by city/province
- Composition statistics by city
- No kecamatan-level daily data available

IMPORTANT — Disaggregation Rule:
If city-level SIPSN data is obtained (e.g., total DKI Jakarta annual waste),
it MUST NOT be disaggregated to kecamatan level and labeled as OBSERVED.
Spatial disaggregation would produce DERIVED or ESTIMATED data only.
"""

from typing import List
from .base import BaseDataSource, DataRecord, ProvenanceType


class SIPSNDataSource(BaseDataSource):
    """
    SIPSN Waste Data Connector.

    STUB: No public API available. Data must be manually obtained from the web interface.
    """
    SOURCE_NAME = "SIPSN KLHK"
    SOURCE_URL = "https://sipsn.menlhk.go.id/"
    IS_STUB = True

    LIMITATIONS = (
        "No public REST API available. Annual city-level data only. "
        "Kecamatan-level daily data NOT available via SIPSN. "
        "City-level data MUST NOT be disaggregated to kecamatan and labeled OBSERVED."
    )

    def is_available(self) -> bool:
        return False  # No API available

    def fetch(self, **kwargs) -> List[DataRecord]:
        """
        SIPSN does not provide a public API.
        Returns empty list — do NOT fabricate data.

        To use SIPSN data:
        1. Download data from https://sipsn.menlhk.go.id/
        2. Process manually
        3. Load via a static file loader, not this adapter
        4. Label as OBSERVED at city level only
        """
        return []

    def get_status(self):
        status = super().get_status()
        status["mode_b_availability"] = "NOT_AVAILABLE"
        status["note"] = (
            "SIPSN provides annual city-level aggregate data via web interface only. "
            "Kecamatan-level daily observations: NOT AVAILABLE. "
            "Mode B validation at kecamatan level is NOT YET POSSIBLE."
        )
        return status
