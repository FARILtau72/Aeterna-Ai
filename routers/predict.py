"""
AETERNA AI — Prediction Router
"""

import io
import csv
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from schemas.prediction import PredictionRequest, APIResponse
from services.forecast_service import generate_prediction_pipeline
import core.model_loader as ml

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Prediction"])

@router.post("/api/v1/predict", response_model=APIResponse)
async def predict_waste_volume(req: PredictionRequest):
    """Predict waste tonnage and compute deterministic logistics simulation."""
    if ml.df_history is None or ml.pipeline is None:
        raise HTTPException(503, "Models not ready.")
    try:
        return await generate_prediction_pipeline(req)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(500, str(e))

@router.post("/api/v1/predict/csv")
async def predict_waste_volume_csv(req: PredictionRequest):
    """Predict waste tonnage and export results as downloadable CSV file."""
    res = await predict_waste_volume(req)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "Date", "Location", "Total Volume (Tons)", 
        "Organic Waste (Tons)", "Plastic Waste (Tons)", 
        "Paper Waste (Tons)", "Metal Waste (Tons)",
        "Glass Waste (Tons)", "Textile Waste (Tons)",
        "Other Waste (Tons)",
        "Risk Status", "Event Info", "Recommended Trucks (15T)"
    ])
    
    for r in res.data.prediction_results:
        writer.writerow([
            r.date, r.location, r.total_volume_ton,
            r.organic_waste_ton, r.plastic_waste_ton,
            r.paper_waste_ton, r.metal_waste_ton,
            r.glass_waste_ton, r.textile_waste_ton,
            r.other_waste_ton,
            r.risk_status, r.event_info or "", r.recommended_trucks
        ])
        
    output.seek(0)
    filename = f"waste_forecast_{req.location.replace(' ', '_')}_{req.forecast_days}d.csv"
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8")), 
        media_type="text/csv", 
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
