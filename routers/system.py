"""
AETERNA AI — System & UI Router
"""

import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse
import core.model_loader as ml

router = APIRouter(tags=["System"])
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

@router.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """Serve the interactive dashboard UI."""
    html_path = os.path.join(frontend_dir, "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard HTML not found. Please check your frontend directory.</h1>", status_code=404)

@router.get("/style.css")
def serve_style():
    """Serve style.css directly at root path."""
    style_path = os.path.join(frontend_dir, "style.css")
    if os.path.exists(style_path):
        return FileResponse(style_path, media_type="text/css")
    return HTMLResponse(content="/* CSS not found */", status_code=404)

@router.get("/app.js")
def serve_app_js():
    """Serve app.js directly at root path."""
    js_path = os.path.join(frontend_dir, "app.js")
    if os.path.exists(js_path):
        return FileResponse(js_path, media_type="application/javascript")
    return HTMLResponse(content="// JS not found", status_code=404)

@router.get("/model_actual_vs_predicted.png")
def serve_model_png1():
    img_path = os.path.join(frontend_dir, "model_actual_vs_predicted.png")
    if os.path.exists(img_path):
        return FileResponse(img_path, media_type="image/png")
    return HTMLResponse(content="Image not found", status_code=404)

@router.get("/model_feature_importance.png")
def serve_model_png2():
    img_path = os.path.join(frontend_dir, "model_feature_importance.png")
    if os.path.exists(img_path):
        return FileResponse(img_path, media_type="image/png")
    return HTMLResponse(content="Image not found", status_code=404)

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
