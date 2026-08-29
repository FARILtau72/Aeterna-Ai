"""
AETERNA AI — DLH DKI Jakarta (Dinas Lingkungan Hidup) Data Adapter

Status: STUB — No public REST API available
Provenance: OBSERVED (when populated with official data)
Source: https://lingkunganhidup.jakarta.go.id/
Authentication: No documented public API found as of 2026-08.

To integrate DLH data:
- Contact DLH DKI Jakarta directly for data sharing agreement
- Potential contact: https://lingkunganhidup.jakarta.go.id/
- Data format to request: daily waste collection records by kecamatan/UPPS

Mode B Status:
Kecamatan-level daily waste volume data from DLH is the
required authoritative target for real-world model validation.
Until this data is obtained, Mode B remains: NOT YET AVAILABLE.
"""

from typing import List
from .base import BaseDataSource, DataRecord, ProvenanceType


class DLHDataSource(BaseDataSource):
    """
    DLH DKI Jakarta Waste Operations Data Connector.

    STUB: No public API available. Requires data sharing agreement with DLH.
    """
    SOURCE_NAME = "DLH DKI Jakarta"
    SOURCE_URL = "https://lingkunganhidup.jakarta.go.id/"
    IS_STUB = True

    LIMITATIONS = (
        "No public REST API. Data sharing agreement with DLH required. "
        "Daily kecamatan-level waste collection records are the "
        "authoritative target needed for Mode B real-world validation."
    )

    def is_available(self) -> bool:
        return False  # No API available

    def fetch(self, **kwargs) -> List[DataRecord]:
        """
        DLH does not provide a public API.
        Returns empty list — do NOT fabricate data.

        To use DLH data:
        1. Establish data sharing agreement with DLH DKI Jakarta
        2. Receive daily waste collection records
        3. Implement a file-based loader in this adapter
        4. This enables Mode B real-world validation
        """
        return []

    def get_status(self):
        status = super().get_status()
        status["mode_b_availability"] = "NOT_AVAILABLE"
        status["note"] = (
            "DLH kecamatan-level daily data is the required authoritative target "
            "for Mode B validation. Currently NOT AVAILABLE. "
            "Contact DLH DKI Jakarta to establish a data-sharing agreement."
        )
        return status
