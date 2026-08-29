"""
AETERNA AI — BPS DKI Jakarta Population Data Adapter

Status: STUB — Requires API key registration
Provenance: OBSERVED (when populated with official data)
Source: https://webapi.bps.go.id/
Authentication: API key required — register at https://webapi.bps.go.id/

Registration Steps:
1. Visit https://webapi.bps.go.id/
2. Create an account and request API access
3. Set environment variable: BPS_API_KEY=<your_key>
4. Population data available at: https://webapi.bps.go.id/v1/api/list/
   (subject to BPS API terms of use)

Known BPS Subject Codes for Jakarta Population:
- Subject 12: Penduduk (Population)
- Domain: 3100 (DKI Jakarta)

Limitations:
- Population data is annual (not daily)
- Published with ~1-2 year lag
- Sub-district (kecamatan) level available in some publications
- API response format may change between BPS API versions

IMPORTANT: The population values currently hardcoded in KECAMATAN_DATABASE
(app.py) are UNVERIFIED. They were manually entered and have not been
validated against official BPS publications. Until this adapter is
activated with an official API key, all population values must be
labeled UNVERIFIED.
"""

import os
from typing import List, Optional
from .base import BaseDataSource, DataRecord, ProvenanceType

# Currently hardcoded population values (UNVERIFIED)
# Source: Manually entered, claimed to be BPS 2023/2024 — NOT YET VALIDATED
# These will be REPLACED when BPS API adapter is activated
UNVERIFIED_POPULATION_DATA = {
    # Jakarta Pusat
    "Menteng": {"population": 88000, "year": 2023},
    "Senen": {"population": 128000, "year": 2023},
    "Cempaka Putih": {"population": 96000, "year": 2023},
    "Johar Baru": {"population": 130000, "year": 2023},
    "Kemayoran": {"population": 255000, "year": 2023},
    "Sawah Besar": {"population": 126000, "year": 2023},
    "Tanah Abang": {"population": 175000, "year": 2023},
    "Gambir": {"population": 97000, "year": 2023},
    # Jakarta Utara
    "Penjaringan": {"population": 312000, "year": 2023},
    "Tanjung Priok": {"population": 415000, "year": 2023},
    "Koja": {"population": 330000, "year": 2023},
    "Cilincing": {"population": 430000, "year": 2023},
    "Pademangan": {"population": 168000, "year": 2023},
    "Kelapa Gading": {"population": 143000, "year": 2023},
    # Jakarta Barat
    "Cengkareng": {"population": 592000, "year": 2023},
    "Grogol Petamburan": {"population": 240000, "year": 2023},
    "Kalideres": {"population": 460000, "year": 2023},
    "Kebon Jeruk": {"population": 380000, "year": 2023},
    "Kembangan": {"population": 310000, "year": 2023},
    "Palmerah": {"population": 205000, "year": 2023},
    "Taman Sari": {"population": 125000, "year": 2023},
    "Tambora": {"population": 270000, "year": 2023},
    # Jakarta Selatan
    "Cilandak": {"population": 215000, "year": 2023},
    "Jagakarsa": {"population": 390000, "year": 2023},
    "Kebayoran Baru": {"population": 145000, "year": 2023},
    "Kebayoran Lama": {"population": 310000, "year": 2023},
    "Mampang Prapatan": {"population": 150000, "year": 2023},
    "Pancoran": {"population": 170000, "year": 2023},
    "Pasar Minggu": {"population": 315000, "year": 2023},
    "Pesanggrahan": {"population": 250000, "year": 2023},
    "Setiabudi": {"population": 110000, "year": 2023},
    "Tebet": {"population": 220000, "year": 2023},
    # Jakarta Timur
    "Cakung": {"population": 559000, "year": 2023},
    "Cipayung": {"population": 290000, "year": 2023},
    "Ciracas": {"population": 310000, "year": 2023},
    "Duren Sawit": {"population": 420000, "year": 2023},
    "Jatinegara": {"population": 315000, "year": 2023},
    "Kramat Jati": {"population": 300000, "year": 2023},
    "Makasar": {"population": 210000, "year": 2023},
    "Matraman": {"population": 175000, "year": 2023},
    "Pasar Rebo": {"population": 220000, "year": 2023},
    "Pulo Gadung": {"population": 300000, "year": 2023},
    # Kepulauan Seribu
    "Kepulauan Seribu Utara": {"population": 16000, "year": 2023},
    "Kepulauan Seribu Selatan": {"population": 13000, "year": 2023},
}


class BPSDataSource(BaseDataSource):
    """
    BPS DKI Jakarta Population Data Connector.

    STUB: Not yet connected to live BPS API.
    Requires BPS_API_KEY environment variable.
    Register at: https://webapi.bps.go.id/
    """
    SOURCE_NAME = "BPS DKI Jakarta"
    SOURCE_URL = "https://webapi.bps.go.id/"
    IS_STUB = True

    LIMITATIONS = (
        "Population data is annual, not daily. Published with ~1-2 year lag. "
        "BPS API registration required. Currently using unverified manually-entered values."
    )

    def __init__(self):
        self.api_key = os.getenv("BPS_API_KEY", "")

    def is_available(self) -> bool:
        """Returns False until BPS API key is configured."""
        return bool(self.api_key)

    def fetch(self, kecamatan: Optional[str] = None, year: int = 2023) -> List[DataRecord]:
        """
        Fetch population data from BPS API.

        If BPS_API_KEY is not configured, returns UNVERIFIED records from
        the hardcoded table. These must be validated and replaced.

        NEVER fabricates or invents population values.
        """
        if not self.is_available():
            # Return unverified hardcoded data with clear provenance labeling
            records = []
            targets = (
                {kecamatan: UNVERIFIED_POPULATION_DATA[kecamatan]}
                if kecamatan and kecamatan in UNVERIFIED_POPULATION_DATA
                else UNVERIFIED_POPULATION_DATA
            )
            for kec, info in targets.items():
                records.append(DataRecord(
                    value=info["population"],
                    field_name="Population_Jiwa",
                    provenance=ProvenanceType.UNVERIFIED,
                    source_name="Hardcoded (UNVERIFIED — BPS API not yet configured)",
                    source_url="https://webapi.bps.go.id/",
                    geographic_granularity="Kecamatan",
                    temporal_granularity="Annual",
                    observation_date=f"{info['year']}-12-31",
                    limitations=(
                        "UNVERIFIED: This value was manually entered and has NOT been validated "
                        "against official BPS publications. Set BPS_API_KEY environment variable "
                        "to activate the official BPS API adapter."
                    ),
                    validation_status="UNVERIFIED_NEEDS_VALIDATION",
                    extra={"kecamatan": kec},
                ))
            return records

        # Live BPS API call (when API key is configured)
        # NOTE: BPS API v1 endpoint structure — verify against current BPS API docs
        # https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/3100/var/12/key/{api_key}
        # This is a documented endpoint pattern — not fabricated
        raise NotImplementedError(
            "Live BPS API connector not yet implemented. "
            "Contribute implementation at: https://github.com/FARILtau72/Aeterna-Ai\n"
            "Reference: https://webapi.bps.go.id/documentation"
        )
