"""
AETERNA AI — Application Settings and Global Constants
"""

import os
from typing import Dict

APP_TITLE = "AETERNA AI — Waste Forecasting & Decision Intelligence"
APP_DESCRIPTION = "Spatial-Temporal AI Waste Forecasting & Deterministic Operational Simulation for 44 Kecamatans in DKI Jakarta"
APP_VERSION = "4.1.0"

HOURLY_PATTERN: Dict[int, float] = {
    0: 0.02, 1: 0.01, 2: 0.01, 3: 0.01, 4: 0.02, 5: 0.03,
    6: 0.05, 7: 0.07, 8: 0.06, 9: 0.05, 10: 0.04, 11: 0.04,
    12: 0.04, 13: 0.04, 14: 0.04, 15: 0.04, 16: 0.05, 17: 0.06,
    18: 0.07, 19: 0.06, 20: 0.05, 21: 0.04, 22: 0.03, 23: 0.02
}

COMPOSITION_RATIOS = {
    "organic": 0.502,
    "plastic": 0.228,
    "paper": 0.115,
    "metal": 0.021,
    "glass": 0.032,
    "textile": 0.042,
    "other": 0.060
}

ZONE_MAPPING = {
    "Pusat Komersial": 1,
    "Permukiman Padat": 2,
    "Permukiman Menengah": 3,
    "Pariwisata & Olahraga": 4,
    "Pesisir & Pelabuhan": 5,
    "Industri & Pergudangan": 6,
    "Kepulauan": 7
}
