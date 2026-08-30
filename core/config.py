"""
AETERNA AI — Core Kecamatan Registry Loader
"""

import json
import os
from typing import Dict, Any, List

_REGISTRY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "kecamatan_registry.json")

def load_kecamatan_registry() -> Dict[str, Dict[str, Any]]:
    if not os.path.exists(_REGISTRY_PATH):
        raise FileNotFoundError(f"Kecamatan registry JSON not found at: {_REGISTRY_PATH}")
    with open(_REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

KECAMATAN_DATABASE: Dict[str, Dict[str, Any]] = load_kecamatan_registry()
ALLOWED_LOCATIONS: List[str] = list(KECAMATAN_DATABASE.keys())

def get_kecamatan_info(location: str) -> Dict[str, Any]:
    return KECAMATAN_DATABASE.get(location, KECAMATAN_DATABASE["Menteng"])
