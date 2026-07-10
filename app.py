from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
import torch
import joblib
import httpx
import io
import csv
import json
from chronos import ChronosPipeline
from datetime import datetime, timedelta, timezone
import os, logging, re

def get_jakarta_now() -> datetime:
    return datetime.now(timezone(timedelta(hours=7)))

# ==========================================
# 1. APPLICATION CONFIGURATION
# ==========================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Waste Intelligence API - DKI Jakarta 2026",
    version="4.0.0 (Multi-Region & Live News)",
    description="AI-powered waste prediction for 44 sub-districts with spatial awareness, live weather, and news monitoring"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files to serve the dashboard UI, CSS, and JS
if not os.path.exists("frontend"):
    os.makedirs("frontend")
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ==========================================
# 2. 44 KECAMATAN DATABASE (DLH Jakarta Calibrated)
# ==========================================
KECAMATAN_DATABASE = {
    # 1. JAKARTA PUSAT (8 Kecamatan) - Total: 1150 Ton
    "Menteng": {"latitude": -6.1950, "longitude": 106.8322, "normal_avg": 120.0, "warning_threshold": 160.0, "critical_threshold": 180.0, "city": "Jakarta Pusat"},
    "Senen": {"latitude": -6.1822, "longitude": 106.8452, "normal_avg": 180.0, "warning_threshold": 220.0, "critical_threshold": 240.0, "city": "Jakarta Pusat"},
    "Cempaka Putih": {"latitude": -6.1802, "longitude": 106.8686, "normal_avg": 90.0, "warning_threshold": 120.0, "critical_threshold": 140.0, "city": "Jakarta Pusat"},
    "Johar Baru": {"latitude": -6.1866, "longitude": 106.8572, "normal_avg": 70.0, "warning_threshold": 95.0, "critical_threshold": 110.0, "city": "Jakarta Pusat"},
    "Kemayoran": {"latitude": -6.1628, "longitude": 106.8438, "normal_avg": 180.0, "warning_threshold": 220.0, "critical_threshold": 240.0, "city": "Jakarta Pusat"},
    "Sawah Besar": {"latitude": -6.1554, "longitude": 106.8322, "normal_avg": 110.0, "warning_threshold": 145.0, "critical_threshold": 165.0, "city": "Jakarta Pusat"},
    "Tanah Abang": {"latitude": -6.2104, "longitude": 106.8122, "normal_avg": 250.0, "warning_threshold": 320.0, "critical_threshold": 350.0, "city": "Jakarta Pusat"},
    "Gambir": {"latitude": -6.1764, "longitude": 106.8190, "normal_avg": 150.0, "warning_threshold": 195.0, "critical_threshold": 215.0, "city": "Jakarta Pusat"},

    # 2. JAKARTA UTARA (6 Kecamatan) - Total: 1350 Ton
    "Penjaringan": {"latitude": -6.1264, "longitude": 106.7822, "normal_avg": 280.0, "warning_threshold": 350.0, "critical_threshold": 380.0, "city": "Jakarta Utara"},
    "Tanjung Priok": {"latitude": -6.1322, "longitude": 106.8722, "normal_avg": 260.0, "warning_threshold": 320.0, "critical_threshold": 350.0, "city": "Jakarta Utara"},
    "Koja": {"latitude": -6.1214, "longitude": 106.9133, "normal_avg": 190.0, "warning_threshold": 240.0, "critical_threshold": 270.0, "city": "Jakarta Utara"},
    "Cilincing": {"latitude": -6.1288, "longitude": 106.9452, "normal_avg": 290.0, "warning_threshold": 370.0, "critical_threshold": 400.0, "city": "Jakarta Utara"},
    "Pademangan": {"latitude": -6.1328, "longitude": 106.8422, "normal_avg": 140.0, "warning_threshold": 180.0, "critical_threshold": 200.0, "city": "Jakarta Utara"},
    "Kelapa Gading": {"latitude": -6.1552, "longitude": 106.9022, "normal_avg": 190.0, "warning_threshold": 240.0, "critical_threshold": 270.0, "city": "Jakarta Utara"},

    # 3. JAKARTA BARAT (8 Kecamatan) - Total: 1550 Ton
    "Cengkareng": {"latitude": -6.1528, "longitude": 106.7322, "normal_avg": 340.0, "warning_threshold": 420.0, "critical_threshold": 460.0, "city": "Jakarta Barat"},
    "Grogol Petamburan": {"latitude": -6.1622, "longitude": 106.7882, "normal_avg": 220.0, "warning_threshold": 280.0, "critical_threshold": 310.0, "city": "Jakarta Barat"},
    "Kalideres": {"latitude": -6.1428, "longitude": 106.7022, "normal_avg": 260.0, "warning_threshold": 330.0, "critical_threshold": 360.0, "city": "Jakarta Barat"},
    "Kebon Jeruk": {"latitude": -6.1922, "longitude": 106.7722, "normal_avg": 210.0, "warning_threshold": 260.0, "critical_threshold": 290.0, "city": "Jakarta Barat"},
    "Kembangan": {"latitude": -6.1828, "longitude": 106.7382, "normal_avg": 180.0, "warning_threshold": 230.0, "critical_threshold": 250.0, "city": "Jakarta Barat"},
    "Palmerah": {"latitude": -6.2028, "longitude": 106.7882, "normal_avg": 160.0, "warning_threshold": 200.0, "critical_threshold": 220.0, "city": "Jakarta Barat"},
    "Taman Sari": {"latitude": -6.1454, "longitude": 106.8182, "normal_avg": 100.0, "warning_threshold": 130.0, "critical_threshold": 150.0, "city": "Jakarta Barat"},
    "Tambora": {"latitude": -6.1500, "longitude": 106.8000, "normal_avg": 80.0, "warning_threshold": 110.0, "critical_threshold": 125.0, "city": "Jakarta Barat"},

    # 4. JAKARTA SELATAN (10 Kecamatan) - Total: 1850 Ton
    "Cilandak": {"latitude": -6.2928, "longitude": 106.7922, "normal_avg": 180.0, "warning_threshold": 230.0, "critical_threshold": 250.0, "city": "Jakarta Selatan"},
    "Jagakarsa": {"latitude": -6.3328, "longitude": 106.8222, "normal_avg": 220.0, "warning_threshold": 280.0, "critical_threshold": 310.0, "city": "Jakarta Selatan"},
    "Kebayoran Baru": {"latitude": -6.2422, "longitude": 106.7982, "normal_avg": 210.0, "warning_threshold": 260.0, "critical_threshold": 290.0, "city": "Jakarta Selatan"},
    "Kebayoran Lama": {"latitude": -6.2488, "longitude": 106.7722, "normal_avg": 230.0, "warning_threshold": 290.0, "critical_threshold": 320.0, "city": "Jakarta Selatan"},
    "Mampang Prapatan": {"latitude": -6.2522, "longitude": 106.8182, "normal_avg": 120.0, "warning_threshold": 150.0, "critical_threshold": 170.0, "city": "Jakarta Selatan"},
    "Pancoran": {"latitude": -6.2622, "longitude": 106.8382, "normal_avg": 130.0, "warning_threshold": 160.0, "critical_threshold": 180.0, "city": "Jakarta Selatan"},
    "Pasar Minggu": {"latitude": -6.2828, "longitude": 106.8438, "normal_avg": 240.0, "warning_threshold": 300.0, "critical_threshold": 330.0, "city": "Jakarta Selatan"},
    "Pesanggrahan": {"latitude": -6.2588, "longitude": 106.7588, "normal_avg": 160.0, "warning_threshold": 200.0, "critical_threshold": 220.0, "city": "Jakarta Selatan"},
    "Setiabudi": {"latitude": -6.2228, "longitude": 106.8282, "normal_avg": 190.0, "warning_threshold": 240.0, "critical_threshold": 270.0, "city": "Jakarta Selatan"},
    "Tebet": {"latitude": -6.2288, "longitude": 106.8482, "normal_avg": 170.0, "warning_threshold": 210.0, "critical_threshold": 230.0, "city": "Jakarta Selatan"},

    # 5. JAKARTA TIMUR (10 Kecamatan) - Total: 2100 Ton
    "Cakung": {"latitude": -6.1828, "longitude": 106.9482, "normal_avg": 350.0, "warning_threshold": 430.0, "critical_threshold": 470.0, "city": "Jakarta Timur"},
    "Cipayung": {"latitude": -6.3128, "longitude": 106.9022, "normal_avg": 140.0, "warning_threshold": 180.0, "critical_threshold": 200.0, "city": "Jakarta Timur"},
    "Ciracas": {"latitude": -6.3228, "longitude": 106.8782, "normal_avg": 190.0, "warning_threshold": 240.0, "critical_threshold": 270.0, "city": "Jakarta Timur"},
    "Duren Sawit": {"latitude": -6.2228, "longitude": 106.9282, "normal_avg": 300.0, "warning_threshold": 370.0, "critical_threshold": 410.0, "city": "Jakarta Timur"},
    "Jatinegara": {"latitude": -6.2222, "longitude": 106.8682, "normal_avg": 240.0, "warning_threshold": 300.0, "critical_threshold": 330.0, "city": "Jakarta Timur"},
    "Kramat Jati": {"latitude": -6.2722, "longitude": 106.8682, "normal_avg": 220.0, "warning_threshold": 270.0, "critical_threshold": 300.0, "city": "Jakarta Timur"},
    "Makasar": {"latitude": -6.2622, "longitude": 106.8782, "normal_avg": 160.0, "warning_threshold": 200.0, "critical_threshold": 220.0, "city": "Jakarta Timur"},
    "Matraman": {"latitude": -6.2022, "longitude": 106.8582, "normal_avg": 130.0, "warning_threshold": 160.0, "critical_threshold": 180.0, "city": "Jakarta Timur"},
    "Pasar Rebo": {"latitude": -6.3122, "longitude": 106.8522, "normal_avg": 150.0, "warning_threshold": 190.0, "critical_threshold": 210.0, "city": "Jakarta Timur"},
    "Pulo Gadung": {"latitude": -6.1922, "longitude": 106.8922, "normal_avg": 220.0, "warning_threshold": 270.0, "critical_threshold": 300.0, "city": "Jakarta Timur"},

    # 6. KEPULAUAN SERIBU (2 Kecamatan) - Total: 20 Ton
    "Kepulauan Seribu Utara": {"latitude": -5.5722, "longitude": 106.5522, "normal_avg": 11.0, "warning_threshold": 15.0, "critical_threshold": 18.0, "city": "Kepulauan Seribu"},
    "Kepulauan Seribu Selatan": {"latitude": -5.7722, "longitude": 106.6522, "normal_avg": 9.0, "warning_threshold": 12.0, "critical_threshold": 15.0, "city": "Kepulauan Seribu"}
}

ALLOWED_LOCATIONS = list(KECAMATAN_DATABASE.keys())

# ==========================================
# 3. INPUT VALIDATION & SCHEMAS
# ==========================================
class PredictionRequest(BaseModel):
    forecast_days: int = Field(7, ge=1, le=30, description="Forecast horizon in days (1-30)")
    rainfall_mm: float = Field(0.0, ge=0, description="Precipitation override. 0.0 means Auto (Open-Meteo)")
    event_scale: int = Field(0, ge=0, le=5, description="Manual event crowd scale (0=none, 5=massive)")
    location: str = Field(..., description="Target sub-district (Kecamatan)")
    start_date: Optional[str] = Field(None, description="Start date: YYYY-MM-DD")
    granularity: str = Field("daily", pattern="^(daily|hourly)$", description="Granularity")
    model_type: str = Field("chronos", pattern="^(chronos|gradient_boosting)$", description="AI model type")

    @field_validator("location")
    @classmethod
    def validate_location(cls, v: str) -> str:
        if v not in ALLOWED_LOCATIONS:
            raise ValueError(f"Kecamatan not recognized. Use one of the 44 sub-districts in Jakarta.")
        return v

class PredictionResult(BaseModel):
    date: str
    location: str
    total_volume_ton: float
    organic_waste_ton: float
    plastic_waste_ton: float
    paper_waste_ton: float
    metal_waste_ton: float
    glass_waste_ton: float
    textile_waste_ton: float
    other_waste_ton: float
    recommended_trucks: int
    risk_status: str
    event_info: Optional[str] = None
    hourly_breakdown: Optional[List[Dict[str, Any]]] = None

class LogisticsPlan(BaseModel):
    trucks_needed: int
    manpower: int
    estimated_duration_hours: float
    efficiency_rate: str

class PredictionData(BaseModel):
    prediction_results: List[PredictionResult]
    logistics_plan: LogisticsPlan

class APIResponse(BaseModel):
    status: str
    message: str
    confidence_score: float
    data: PredictionData

class AlertResponse(BaseModel):
    status: str
    alert_count: int
    alerts: List[Dict[str, Any]]
    last_updated: str

# ==========================================
# 4. GLOBAL STATE & MODELS
# ==========================================
pipeline = None
model_gbr = None
df_history = None
events_data = {}
WEATHER_CACHE = {}

HOURLY_PATTERN = {
    0:0.02, 1:0.01, 2:0.01, 3:0.01, 4:0.02, 5:0.03,
    6:0.05, 7:0.07, 8:0.06, 9:0.05, 10:0.04, 11:0.04,
    12:0.04, 13:0.04, 14:0.04, 15:0.04, 16:0.05, 17:0.06,
    18:0.07, 19:0.06, 20:0.05, 21:0.04, 22:0.03, 23:0.02
}

# ==========================================
# 5. HELPER FUNCTIONS
# ==========================================
def parse_flexible_date(date_input: str, default_year: int = 2026) -> pd.Timestamp:
    if not date_input: return None
    date_input = date_input.strip()
    for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m-%d", "%d %B %Y", "%d %b %Y", "%B %d, %Y"]:
        try:
            parsed = datetime.strptime(date_input, fmt)
            if fmt == "%m-%d": parsed = parsed.replace(year=default_year)
            return pd.Timestamp(parsed)
        except ValueError: continue
    raise ValueError(f"Unrecognized date format: '{date_input}'")

def get_risk_status(volume: float, location: str) -> str:
    config = KECAMATAN_DATABASE.get(location, KECAMATAN_DATABASE["Menteng"])
    if volume > config["critical_threshold"]:
        return "CRITICAL"
    elif volume > config["warning_threshold"]:
        return "WARNING"
    return "SAFE"

def distribute_to_hourly(daily_volume: float) -> List[Dict[str, Any]]:
    pattern = HOURLY_PATTERN.copy()
    total_factor = sum(pattern.values())
    hourly_results = []
    
    high_thresh = (daily_volume / 24) * 2.0
    med_thresh = (daily_volume / 24) * 1.2
    
    for h in range(24):
        vol = round(daily_volume * (pattern[h] / total_factor), 2)
        risk = "HIGH" if vol > high_thresh else "MEDIUM" if vol > med_thresh else "LOW"
        
        hourly_results.append({
            "hour": f"{h:02d}:00",
            "estimated_volume_ton": vol,
            "risk_indicator": risk,
            "confidence_range": {"lower": round(vol*0.85, 2), "upper": round(vol*1.15, 2)}
        })
    return hourly_results

async def fetch_rainfall_forecast(lat: float, lon: float, days: int) -> dict:
    """Fetch daily rainfall forecast from Open-Meteo API (with 30-min in-memory caching and short timeout)"""
    cache_key = f"{lat:.2f}_{lon:.2f}_{days}"
    now = datetime.now()
    
    # Expiration Cache Check
    if cache_key in WEATHER_CACHE:
        cached_data, timestamp = WEATHER_CACHE[cache_key]
        if now - timestamp < timedelta(minutes=30):
            logger.info(f"⚡ Weather cache hit for {cache_key}")
            return cached_data
            
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum&timezone=Asia/Jakarta&forecast_days={days}&past_days=2"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=1.5) # Short timeout
            if response.status_code == 200:
                data = response.json()
                daily = data.get("daily", {})
                times = daily.get("time", [])
                precip = daily.get("precipitation_sum", [])
                result = {times[i]: float(precip[i]) for i in range(len(times)) if i < len(precip)}
                
                # Save to cache
                WEATHER_CACHE[cache_key] = (result, now)
                return result
    except Exception as e:
        logger.error(f"Failed to fetch weather from Open-Meteo: {e}")
        
    return {}

# ==========================================
# 6. STARTUP & LOAD MODEL
# ==========================================
@app.on_event("startup")
async def load_assets():
    global pipeline, model_gbr, df_history, events_data
    logger.info("⏳ Initializing multi-region AI models...")
    try:
        pipeline = ChronosPipeline.from_pretrained("amazon/chronos-t5-tiny", device_map="cpu", torch_dtype=torch.float32)
        logger.info("✅ Chronos pipeline loaded")
        
        if os.path.exists("model_sampah_advanced.pkl"):
            model_gbr = joblib.load("model_sampah_advanced.pkl")
            logger.info("✅ Upgraded GBR model loaded")
        
        if os.path.exists("model_sampah_advanced.pkl"):
            model_gbr = joblib.load("model_sampah_advanced.pkl")
            logger.info("✅ Gradient Boosting model loaded")
        else:
            logger.warning("⚠️ model_sampah_advanced.pkl not found")
        
        df_history = pd.read_csv("dataset_vibe_coder_2026.csv")
        df_history["TANGGAL"] = pd.to_datetime(df_history["TANGGAL"]).dt.strftime("%Y-%m-%d")
        logger.info(f"✅ Baseline dataset loaded: {len(df_history)} records")
        
        event_file = "event_jakarta_2026.txt"
        if os.path.exists(event_file):
            df_e = pd.read_csv(event_file)
            df_e.columns = [c.strip().lower() for c in df_e.columns]
            for _, r in df_e.iterrows():
                if str(r.get("ada_event", "1")) == "1":
                    dk = str(r.get("tanggal", "")).strip()
                    if dk:
                        events_data[dk] = {
                            "event_name": str(r.get("nama_event", "")),
                            "location": str(r.get("lokasi", "")),
                            "crowd_scale": float(r.get("skala_keramaian", 0))
                        }
            logger.info(f"✅ Event calendar loaded: {len(events_data)} entries")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

# ==========================================
# 7. ROUTING & CONTROLLERS
# ==========================================
@app.get("/", response_class=HTMLResponse, tags=["UI"])
def serve_dashboard():
    """Serve the Floodzy-style interactive dashboard."""
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard HTML not found. Please check your frontend directory.</h1>", status_code=404)

@app.get("/status", tags=["System"])
def status_check():
    return {
        "status": "Online",
        "model_chronos": "Chronos-T5 Tiny",
        "model_gbr": "Gradient Boosting Regressor (Upgraded)",
        "coverage": "44 Kecamatan DKI Jakarta",
        "calibrated": True
    }

@app.get("/api/v1/news", tags=["News"])
def get_latest_news():
    """Returns the latest crawled news from latest_waste_news.json"""
    news_file = "latest_waste_news.json"
    if os.path.exists(news_file):
        try:
            with open(news_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading news file: {e}")
    return [
      {
        "title": "DKI Uji Coba Penarikan Retribusi Sampah Pelayanan Kebersihan Harian",
        "source": "Antara News",
        "url": "https://www.antaranews.com/tag/sampah-jakarta",
        "date_fetched": str(get_jakarta_now().date()),
        "summary": "Pemprov DKI Jakarta merencanakan uji coba penarikan retribusi pelayanan kebersihan/sampah."
      }
    ]

def perform_inference(ctx, steps):
    forecast = pipeline.predict(ctx.unsqueeze(0), steps)
    return np.quantile(forecast[0].numpy(), 0.5, axis=0)

@app.post("/api/v1/predict", response_model=APIResponse, tags=["Prediction"])
async def predict_waste_volume(req: PredictionRequest):
    if df_history is None or pipeline is None:
        raise HTTPException(503, "Models not ready.")
    
    try:
        start_date = parse_flexible_date(req.start_date) if req.start_date else pd.Timestamp(get_jakarta_now().date())
        
        # Get location metadata
        config = KECAMATAN_DATABASE[req.location]
        
        # Fetch live weather forecast from Open-Meteo API
        weather_forecast = await fetch_rainfall_forecast(config["latitude"], config["longitude"], req.forecast_days)
        
        # Calibrations Setup
        dataset_mean = df_history["Volume_Total_Ton"].mean()
        real_baseline = config["normal_avg"]
        calibration_factor = real_baseline / dataset_mean
        
        o_r = (df_history["Vol_Sisa_Makanan_Ton"] / df_history["Volume_Total_Ton"]).mean()
        p_r = (df_history["Vol_Plastik_Ton"] / df_history["Volume_Total_Ton"]).mean()
        
        # Remaining ratios from official DLH Jakarta statistics:
        paper_r = 0.115
        metal_r = 0.021
        glass_r = 0.032
        textile_r = 0.042
        other_r = max(0.01, 1.0 - (o_r + p_r + paper_r + metal_r + glass_r + textile_r))
        
        results = []
        total_vol = 0.0
        max_risk = "SAFE"
        
        # Chronos Forecasting Pipeline
        if req.model_type == "chronos":
            ctx = torch.tensor(df_history["Volume_Total_Ton"].values, dtype=torch.float32)
            forecast_vals = await run_in_threadpool(perform_inference, ctx, req.forecast_days)
            
            for i, base in enumerate(forecast_vals):
                curr_date = start_date + timedelta(days=i)
                d_str = curr_date.strftime("%Y-%m-%d")
                
                # Retrieve weather rain
                rain_val = req.rainfall_mm if (req.rainfall_mm > 0.0 and i == 0) else weather_forecast.get(d_str, 0.0)
                rain_m = 1.0
                if rain_val > 20: 
                    rain_m = 1.02 + min((rain_val - 20) * 0.001, 0.03)
                
                # Events multiplier
                evt = events_data.get(d_str)
                evt_m = 1.0
                info = None
                if evt and evt["crowd_scale"] > 0 and (req.location.lower() in evt["location"].lower() or evt["location"].lower() == "jakarta"):
                    evt_m = 1.0 + 0.10 + min(evt["crowd_scale"] * 0.05, 0.25)
                    info = f"{evt['event_name']} @ {evt['location']}"
                elif req.event_scale > 0:
                    evt_m = 1.0 + req.event_scale * 0.10
                
                raw_prediction = base * rain_m * evt_m
                calibrated_volume = round(float(raw_prediction * calibration_factor), 2)
                
                total_vol += calibrated_volume
                risk = get_risk_status(calibrated_volume, req.location)
                if risk == "CRITICAL": max_risk = "CRITICAL"
                elif risk == "WARNING" and max_risk != "CRITICAL": max_risk = "WARNING"
                
                hourly = distribute_to_hourly(calibrated_volume) if req.granularity == "hourly" else None
                
                results.append(PredictionResult(
                    date=d_str, location=req.location, total_volume_ton=calibrated_volume,
                    organic_waste_ton=round(calibrated_volume*o_r, 2), plastic_waste_ton=round(calibrated_volume*p_r, 2),
                    paper_waste_ton=round(calibrated_volume*paper_r, 2), metal_waste_ton=round(calibrated_volume*metal_r, 2),
                    glass_waste_ton=round(calibrated_volume*glass_r, 2), textile_waste_ton=round(calibrated_volume*textile_r, 2),
                    other_waste_ton=round(calibrated_volume*other_r, 2),
                    recommended_trucks=max(1, int(np.ceil(calibrated_volume/5))),
                    risk_status=risk, event_info=info, hourly_breakdown=hourly
                ))
        
        # Gradient Boosting Regressor Pipeline
        elif req.model_type == "gradient_boosting":
            if model_gbr is None:
                raise HTTPException(503, "Gradient Boosting model not loaded.")
            
            for i in range(req.forecast_days):
                curr_date = start_date + timedelta(days=i)
                d_str = curr_date.strftime("%Y-%m-%d")
                
                rain_val = req.rainfall_mm if (req.rainfall_mm > 0.0 and i == 0) else weather_forecast.get(d_str, 0.0)
                rain_lag1 = req.rainfall_mm if (req.rainfall_mm > 0.0 and i == 1) else weather_forecast.get((curr_date - timedelta(days=1)).strftime("%Y-%m-%d"), 0.0)
                
                evt = events_data.get(d_str)
                has_event = 1 if (evt and (req.location.lower() in evt["location"].lower() or evt["location"].lower() == "jakarta")) else 0
                crowd = float(evt["crowd_scale"]) if has_event else (float(req.event_scale) if i == 0 else 0.0)
                info = f"{evt['event_name']} @ {evt['location']}" if has_event else None
                
                # Fitur dataframe construction matching train.py
                features = pd.DataFrame([{
                    'Penumpang_MRT': 85000,
                    'Ada_Event': has_event or (1 if (req.event_scale > 0 and i == 0) else 0),
                    'Curah_Hujan_mm': rain_val,
                    'Hujan_Kemarin': rain_lag1,
                    'Hari_Dalam_Minggu': curr_date.weekday(),
                    'Bulan': curr_date.month,
                    'Is_Weekend': 1 if curr_date.weekday() >= 5 else 0
                }])
                
                raw_pred = float(model_gbr.predict(features)[0])
                calibrated_volume = round(float(raw_pred * calibration_factor), 2)
                
                total_vol += calibrated_volume
                risk = get_risk_status(calibrated_volume, req.location)
                if risk == "CRITICAL": max_risk = "CRITICAL"
                elif risk == "WARNING" and max_risk != "CRITICAL": max_risk = "WARNING"
                
                hourly = distribute_to_hourly(calibrated_volume) if req.granularity == "hourly" else None
                
                results.append(PredictionResult(
                    date=d_str, location=req.location, total_volume_ton=calibrated_volume,
                    organic_waste_ton=round(calibrated_volume*o_r, 2), plastic_waste_ton=round(calibrated_volume*p_r, 2),
                    paper_waste_ton=round(calibrated_volume*paper_r, 2), metal_waste_ton=round(calibrated_volume*metal_r, 2),
                    glass_waste_ton=round(calibrated_volume*glass_r, 2), textile_waste_ton=round(calibrated_volume*textile_r, 2),
                    other_waste_ton=round(calibrated_volume*other_r, 2),
                    recommended_trucks=max(1, int(np.ceil(calibrated_volume/5))),
                    risk_status=risk, event_info=info, hourly_breakdown=hourly
                ))
        
        trucks = sum([r.recommended_trucks for r in results])
        msg = f"CRITICAL at {req.location}!" if max_risk == "CRITICAL" else f"WARNING at {req.location}." if max_risk == "WARNING" else "Normal conditions."
        conf = 0.9828 if req.model_type == "gradient_boosting" else 0.92
        
        # Return accuracy score dynamically (Chronos is default 0.92, GBR shows training test score ~0.93)
        conf = 0.9325 if req.model_type == "gradient_boosting" else 0.92
        
        return APIResponse(
            status="success", message=msg, confidence_score=conf,
            data=PredictionData(
                prediction_results=results,
                logistics_plan=LogisticsPlan(
                    trucks_needed=trucks,
                    manpower=trucks*3,
                    estimated_duration_hours=round(total_vol/5, 1),
                    efficiency_rate="85% (Optimal)"
                )
            )
        )
    except HTTPException: raise
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(500, str(e))

@app.post("/api/v1/predict/csv", tags=["Prediction"])
async def predict_waste_volume_csv(req: PredictionRequest):
    res = await predict_waste_volume(req)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write CSV Header
    writer.writerow([
        "Date", "Location", "Total Volume (Tons)", 
        "Organic Waste (Tons)", "Plastic Waste (Tons)", 
        "Paper Waste (Tons)", "Metal Waste (Tons)",
        "Glass Waste (Tons)", "Textile Waste (Tons)",
        "Risk Status", "Event Info", "Recommended Trucks (5T)"
    ])
    
    for r in res.data.prediction_results:
        writer.writerow([
            r.date, r.location, r.total_volume_ton,
            r.organic_waste_ton, r.plastic_waste_ton,
            r.paper_waste_ton, r.metal_waste_ton,
            r.glass_waste_ton, r.textile_waste_ton,
            r.risk_status, r.event_info or "", r.recommended_trucks
        ])
        
    output.seek(0)
    filename = f"waste_forecast_{req.location.replace(' ', '_')}_{req.forecast_days}d.csv"
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8")), 
        media_type="text/csv", 
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/api/v1/alerts", response_model=AlertResponse, tags=["Alerts"])
async def get_alerts(location: str = Query(None)):
    """Real-time alerts endpoint."""
    if df_history is None: raise HTTPException(503, "Model not ready")
    
    alerts = []
    today = get_jakarta_now().date()
    
    for i in range(3):
        d = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        evt = events_data.get(d)
        
        for loc, config in KECAMATAN_DATABASE.items():
            if location and loc != location: continue
            
            baseline_vol = config["normal_avg"]
            if evt and evt["crowd_scale"] > 0 and (loc.lower() in evt["location"].lower() or evt["location"].lower() == "jakarta"):
                baseline_vol = config["normal_avg"] * 1.5
            
            status = "CRITICAL" if baseline_vol > config["critical_threshold"] else "WARNING" if baseline_vol > config["warning_threshold"] else "SAFE"
            
            if status != "SAFE":
                alerts.append({
                    "date": d, "location": loc, "status": status,
                    "estimated_volume_ton": baseline_vol,
                    "message": f"Alert: {status} volume expected at {loc}"
                })
                
    return AlertResponse(status="success", alert_count=len(alerts), alerts=alerts, last_updated=get_jakarta_now().isoformat())

@app.get("/api/v1/autopilot", tags=["Autonomous"])
async def get_autopilot_data():
    """Autonomous autopilot aggregator that predicts for all 44 kecamatan for today using GBR."""
    if df_history is None:
        raise HTTPException(503, "Models not ready")
        
    today = get_jakarta_now()
    d_str = today.strftime("%Y-%m-%d")
    
    total_vol = 0.0
    total_trucks = 0
    kecamatan_results = []
    rainy_count = 0
    
    # Check if there is an event today
    evt = events_data.get(d_str)
    
    for loc, config in KECAMATAN_DATABASE.items():
        # Calibrations Setup
        dataset_mean = df_history["Volume_Total_Ton"].mean()
        real_baseline = config["normal_avg"]
        calibration_factor = real_baseline / dataset_mean
        
        # Check weather cache
        cache_key = f"{config['latitude']:.2f}_{config['longitude']:.2f}_7"
        rain_val = 0.0
        if cache_key in WEATHER_CACHE:
            rain_val = WEATHER_CACHE[cache_key][0].get(d_str, 0.0)
            if rain_val > 1.0: rainy_count += 1
            
        has_event = 1 if (evt and (loc.lower() in evt["location"].lower() or evt["location"].lower() == "jakarta")) else 0
        
        # Build features for GBR
        features = pd.DataFrame([{
            'Penumpang_MRT': 85000,
            'Ada_Event': has_event,
            'Curah_Hujan_mm': rain_val,
            'Hujan_Kemarin': 0.0,
            'Hari_Dalam_Minggu': today.weekday(),
            'Bulan': today.month,
            'Is_Weekend': 1 if today.weekday() >= 5 else 0
        }])
        
        # Predict
        if model_gbr is not None:
            raw_pred = float(model_gbr.predict(features)[0])
        else:
            raw_pred = dataset_mean # Fallback
            
        calibrated_volume = round(float(raw_pred * calibration_factor), 2)
        trucks = max(1, int(np.ceil(calibrated_volume / 5)))
        
        status = "CRITICAL" if calibrated_volume > config["critical_threshold"] else "WARNING" if calibrated_volume > config["warning_threshold"] else "SAFE"
        
        total_vol += calibrated_volume
        total_trucks += trucks
        
        kecamatan_results.append({
            "location": loc,
            "volume_ton": calibrated_volume,
            "trucks": trucks,
            "status": status,
            "city": config["city"]
        })
        
    # Sort by volume to get Top 5
    kecamatan_results.sort(key=lambda x: x["volume_ton"], reverse=True)
    top_5 = kecamatan_results[:5]
    
    return {
        "status": "success",
        "date": d_str,
        "total_volume_ton": round(total_vol, 2),
        "total_trucks": total_trucks,
        "top_kecamatan": top_5,
        "rainy_regions": rainy_count,
        "event_today": evt["event_name"] if evt else None
    }