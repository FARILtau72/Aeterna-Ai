"""
AETERNA AI — Open-Meteo Weather Data Source

Status: ACTIVE
Provenance: EXTERNAL_REALTIME
Source: https://open-meteo.com/
API: https://api.open-meteo.com/v1/forecast
Authentication: None required (free tier)

Limitations:
- Forecast accuracy degrades beyond 7 days
- Free tier, no uptime SLA
- Point-coordinate based (not kecamatan-polygon averaged)
"""

import httpx
from typing import List, Optional
from .base import BaseDataSource, DataRecord, ProvenanceType


class WeatherDataSource(BaseDataSource):
    SOURCE_NAME = "Open-Meteo"
    SOURCE_URL = "https://api.open-meteo.com/v1/forecast"
    IS_STUB = False  # Live connector

    LIMITATIONS = (
        "Free tier, no SLA. Forecast accuracy degrades beyond 7 days. "
        "Point-coordinate estimate, not spatial average over kecamatan boundary."
    )

    def is_available(self) -> bool:
        """Check if Open-Meteo API is reachable."""
        try:
            r = httpx.get(
                "https://api.open-meteo.com/v1/forecast",
                params={"latitude": -6.2, "longitude": 106.8, "daily": "precipitation_sum",
                        "timezone": "Asia/Jakarta", "forecast_days": 1},
                timeout=3.0
            )
            return r.status_code == 200
        except Exception:
            return False

    def fetch(
        self,
        latitude: float,
        longitude: float,
        forecast_days: int = 7,
        past_days: int = 2
    ) -> List[DataRecord]:
        """
        Fetch daily precipitation forecast from Open-Meteo.

        Returns one DataRecord per forecast day with:
        - field_name: "Rainfall_mm"
        - provenance: EXTERNAL_REALTIME
        - source_name: "Open-Meteo"
        """
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&daily=precipitation_sum&timezone=Asia/Jakarta"
            f"&forecast_days={forecast_days}&past_days={past_days}"
        )
        try:
            r = httpx.get(url, timeout=3.0)
            if r.status_code != 200:
                return []
            data = r.json().get("daily", {})
            times = data.get("time", [])
            precip = data.get("precipitation_sum", [])
            records = []
            for i, (t, p) in enumerate(zip(times, precip)):
                records.append(DataRecord(
                    value=float(p) if p is not None else 0.0,
                    field_name="Rainfall_mm",
                    provenance=ProvenanceType.EXTERNAL_REALTIME,
                    source_name=self.SOURCE_NAME,
                    source_url=self.SOURCE_URL,
                    geographic_granularity=f"Point ({latitude:.4f}, {longitude:.4f})",
                    temporal_granularity="Daily",
                    observation_date=t,
                    limitations=self.LIMITATIONS,
                    validation_status="LIVE_API",
                ))
            return records
        except Exception:
            return []
