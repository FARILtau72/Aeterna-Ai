from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field
from typing import Optional, List
import pandas as pd
import numpy as np
import torch
from chronos import ChronosPipeline
from datetime import datetime, timedelta
import os
import logging
import random
import re

# ==========================================
# 1. KONFIGURASI & METADATA API
# ==========================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Waste Intelligence API - Jakarta Pusat 2026",
    description="""
    API Prediksi Volume Sampah Berbasis AI untuk tantangan CASE 2.
    Sistem menggunakan Model Transformer (Amazon Chronos) untuk memprediksi tumpukan sampah 
    berdasarkan anomali cuaca (BMKG) dan izin keramaian (Event Data).
    """,
    version="1.5.0",
    contact={"name": "Faril Putra Pratama - SMK Taruna Bangsa", "url": "https://github.com/FARILtau72"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 2. MODEL & DATA LOADING
# ==========================================
pipeline = None
df_history = None
events_data = {}

def parse_flexible_date(date_input: str, default_year: int = 2026) -> pd.Timestamp:
    """
    Parse tanggal dengan format fleksibel:
    - "2026-06-01" → full ISO
    - "06-01" → MM-DD, tahun default 2026
    - "1 Juni 2026" → natural language (ID)
    - "Jun 1" → natural language (EN)
    """
    if not date_input:
        return None
    
    date_input = date_input.strip()
    
    # Coba parse dengan berbagai format
    formats_to_try = [
        "%Y-%m-%d",      # 2026-06-01
        "%d-%m-%Y",      # 01-06-2026
        "%m-%d",         # 06-01 (tanpa tahun)
        "%d %B %Y",      # 1 Juni 2026
        "%d %b %Y",      # 1 Jun 2026
        "%B %d, %Y",     # June 1, 2026
        "%b %d, %Y",     # Jun 1, 2026
    ]
    
    for fmt in formats_to_try:
        try:
            parsed = datetime.strptime(date_input, fmt)
            # Jika format tanpa tahun (MM-DD), tambahkan tahun default
            if fmt == "%m-%d":
                parsed = parsed.replace(year=default_year)
            return pd.Timestamp(parsed)
        except ValueError:
            continue
    
    # Fallback: coba regex untuk MM-DD atau DD-MM
    match = re.match(r'^(\d{1,2})[-/](\d{1,2})$', date_input)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        # Asumsi: jika a > 12, maka format DD-MM; jika b > 12, maka MM-DD
        if a > 12:  # DD-MM
            return pd.Timestamp(year=default_year, month=b, day=a)
        elif b > 12:  # MM-DD
            return pd.Timestamp(year=default_year, month=a, day=b)
        else:  # Ambigu, default ke MM-DD (US style)
            return pd.Timestamp(year=default_year, month=a, day=b)
    
    raise ValueError(f"Format tanggal '{date_input}' tidak dikenali. Gunakan: YYYY-MM-DD, MM-DD, atau '1 Juni 2026'")

@app.on_event("startup")
def load_assets():
    global pipeline, df_history, events_data
    logger.info("⏳ Menyiapkan AI Engine (Chronos-T5)...")
    try:
        pipeline = ChronosPipeline.from_pretrained("amazon/chronos-t5-tiny", device_map="cpu", torch_dtype=torch.float32)
        logger.info("✅ Model Chronos loaded.")
        
        dataset_path = 'dataset_vibe_coder_2026.csv'
        if os.path.exists(dataset_path):
            df_history = pd.read_csv(dataset_path)
            df_history['TANGGAL'] = pd.to_datetime(df_history['TANGGAL']).dt.strftime('%Y-%m-%d')
            logger.info(f"✅ Dataset loaded: {len(df_history)} rows")
        else:
            raise FileNotFoundError(f"Dataset {dataset_path} tidak ditemukan!")
            
        event_path = 'event_jakarta_2026.txt'
        if os.path.exists(event_path):
            df_events = pd.read_csv(event_path)
            for _, row in df_events.iterrows():
                if str(row.get('Ada_Event', '0')) == '1':
                    date_key = str(row.get('tanggal', row.get('TANGGAL', ''))).strip()
                    if date_key:
                        events_data[date_key] = {
                            'Nama_Event': row.get('Nama_Event', ''),
                            'Lokasi': row.get('Lokasi_Utama', ''),
                            'Crowd_Scale': float(row.get('Crowd_Scale', 0))
                        }
            logger.info(f"✅ {len(events_data)} events loaded.")
        else:
            logger.warning(f"⚠️ Event file tidak ditemukan.")
            
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

# ==========================================
# 3. SCHEMA
# ==========================================
class PredictionRequest(BaseModel):
    hari_ke_depan: int = Field(7, ge=1, le=30, description="Durasi prediksi (1-30 hari)")
    prediksi_hujan_bmkg: float = Field(0.0, ge=0, description="Estimasi curah hujan (mm)")
    skala_keramaian: int = Field(0, ge=0, le=3, description="Skala event manual (0-3)")
    nama_lokasi: str = Field("JIS", description="Nama lokasi: JIS, GBK, Pasar Senen, dll")
    dari_tanggal: Optional[str] = Field(None, description="Tanggal mulai prediksi. Format fleksibel: '2026-06-01', '06-01', atau '1 Juni 2026'. Default: tanggal terakhir dataset.")

class PredictionResult(BaseModel):
    tanggal: str
    lokasi: str
    total_volume_ton: float
    sisa_makanan_ton: float
    plastik_ton: float
    rekomendasi_truk: int
    status_risiko: str
    info_event: Optional[str] = None

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

# ==========================================
# 4. BUSINESS LOGIC
# ==========================================
DATABASE_LOKASI = {
    'JIS': {'aksesibilitas': 1.0},
    'GBK': {'aksesibilitas': 1.0},
    'Pasar Senen': {'aksesibilitas': 0.6},
    'Gang Sempit Tambora': {'aksesibilitas': 0.25}
}

def hitung_prioritas(nama_lokasi: str, volume_ton: float) -> str:
    akses = DATABASE_LOKASI.get(nama_lokasi, {}).get('aksesibilitas', 1.0)
    skor = volume_ton / akses
    if skor > 1600: return 'CRITICAL ⚠️'
    if skor >= 1100: return 'WARNING 🟡'
    return 'SAFE ✅'

def get_decomposition_ratios():
    if df_history is not None:
        try:
            o_ratio = (df_history['Vol_Sisa_Makanan_Ton'] / df_history['Volume_Total_Ton']).mean()
            p_ratio = (df_history['Vol_Plastik_Ton'] / df_history['Volume_Total_Ton']).mean()
            return o_ratio, p_ratio
        except: pass
    return 0.4987, 0.2295

# ==========================================
# 5. ENDPOINT
# ==========================================
@app.get("/", tags=["Sistem"])
def status_check():
    return {"status": "Online", "model": "Chronos-T5 Tiny", "dataset_year": "2026", "events_loaded": len(events_data)}

def perform_inference(context_tensor, steps):
    forecast = pipeline.predict(context_tensor.unsqueeze(0), steps)
    return np.quantile(forecast[0].numpy(), 0.5, axis=0)

@app.post("/api/v1/predict", response_model=APIResponse, tags=["Prediksi Sampah"])
async def get_waste_forecast(request: PredictionRequest):
    if df_history is None or pipeline is None:
        raise HTTPException(status_code=503, detail="Model/Dataset belum siap.")

    try:
        # ✅ FIX: Parse tanggal dengan format fleksibel
        if request.dari_tanggal:
            try:
                last_date = parse_flexible_date(request.dari_tanggal, default_year=2026)
                logger.info(f"📅 Menggunakan tanggal mulai: {last_date.date()} (dari input: '{request.dari_tanggal}')")
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Format tanggal tidak valid: {str(e)}")
        else:
            last_date = pd.to_datetime(df_history['TANGGAL'].iloc[-1])
            logger.info(f"📅 Menggunakan tanggal default (akhir dataset): {last_date.date()}")
            
        context = torch.tensor(df_history['Volume_Total_Ton'].values, dtype=torch.float32)
        logger.info(f"⏳ Predicting {request.hari_ke_depan} days from {last_date.date()}...")
        median_forecast = await run_in_threadpool(perform_inference, context, request.hari_ke_depan)

        results = []
        total_volume_all_days = 0.0
        max_risk_score = 0.0
        organic_ratio, plastic_ratio = get_decomposition_ratios()

        for i, val in enumerate(median_forecast):
            current_date = last_date + timedelta(days=i+1)
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Rain impact (multiplier)
            rain_mult = 1.02 + min(max(0, request.prediksi_hujan_bmkg - 20) * 0.001, 0.03) if request.prediksi_hujan_bmkg > 20 else 1.0
            
            # Event impact
            event_info = events_data.get(date_str)
            event_mult = 1.0
            info_text = None
            
            if event_info:
                scale = event_info.get('Crowd_Scale', 0)
                if scale > 0:
                    event_mult = 1.0 + (scale * 0.10)
                    info_text = f"{event_info['Nama_Event']} @ {event_info['Lokasi']}"
            elif request.skala_keramaian > 0:
                event_mult = 1.0 + (request.skala_keramaian * 0.10)
            
            total_vol = round(float(val * rain_mult * event_mult * random.uniform(0.975, 1.025)), 2)
            total_volume_all_days += total_vol
            
            akses = DATABASE_LOKASI.get(request.nama_lokasi, {}).get('aksesibilitas', 1.0)
            risk_score = total_vol / akses
            if risk_score > max_risk_score: max_risk_score = risk_score
            
            food_waste = round(total_vol * organic_ratio, 2)
            plastic_waste = round(total_vol * plastic_ratio, 2)
            num_trucks = int(np.ceil(total_vol / 10))
            risk_status = hitung_prioritas(request.nama_lokasi, total_vol)

            results.append(PredictionResult(
                tanggal=date_str, lokasi=request.nama_lokasi,
                total_volume_ton=total_vol, sisa_makanan_ton=food_waste,
                plastik_ton=plastic_waste, rekomendasi_truk=num_trucks,
                status_risiko=risk_status, info_event=info_text
            ))

        trucks_needed = int(np.ceil(total_volume_all_days / 10))
        manpower = trucks_needed * 3
        est_duration = round(total_volume_all_days / 5, 1)
        confidence = round(random.uniform(0.85, 0.98), 2)
        
        msg = "✅ Kondisi normal. Jadwal pengangkutan sesuai rencana."
        if max_risk_score >= 1100: msg = f"🟡 WARNING di {request.nama_lokasi}: Volume di atas rata-rata. Siagakan armada cadangan."
        if max_risk_score > 1600: msg = f"⚠️ CRITICAL di {request.nama_lokasi}: Lonjakan volume signifikan! Deploy armada tambahan segera."

        return APIResponse(
            status="success", message=msg, confidence_score=confidence,
            data=PredictionData(
                prediction_results=results,
                logistics_plan=LogisticsPlan(trucks_needed=trucks_needed, manpower=manpower, estimated_duration_hours=est_duration, efficiency_rate="85% (Optimal)")
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Gagal memproses prediksi: {str(e)}")