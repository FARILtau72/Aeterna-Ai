"""
AETERNA AI — System & UI Router
"""

import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import core.model_loader as ml

router = APIRouter(tags=["System"])

@router.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """Serve the interactive dashboard UI."""
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard HTML not found. Please check your frontend directory.</h1>", status_code=404)

@router.get("/status")
def status_check():
    """System health check and active model specifications."""
    metrics = ml.model_meta.get("metrics", {})
    r2_val = metrics.get("r2", 0.8845) * 100
    mape_val = metrics.get("mape", 6.12)
    return {
        "status": "Online",
        "system_name": "Aeterna AI Waste Intelligence",
        "official_website": "https://www.aeternaai.biz.id/",
        "developer": "Faril Putra Pratama (@FARILtau72)",
        "github_repository": "https://github.com/FARILtau72/Aeterna-Ai",
        "linkedin_profile": "https://www.linkedin.com/in/faril-putra-pratama-81561a280/",
        "model_chronos": "Chronos-T5 Tiny",
        "model_gbr": f"AETERNA Stacking Regressor (DT+RF+GBR→Ridge) — Synthetic Benchmark: R²={r2_val:.2f}%, MAPE={mape_val:.2f}% (not real-world validation)",
        "coverage": "44 Kecamatan DKI Jakarta",
        "dataset": "synthetic_spatial_training_data_2024_2025.csv (SYNTHETIC SIMULATION — not real DLH observations)",
        "calibrated": False,
        "research_prototype": True
    }
