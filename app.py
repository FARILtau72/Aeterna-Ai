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
import asyncio

# ==========================================
# 1. KONFIGURASI & METADATA API
# ==========================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Waste Intelligence API - Jakarta Pusat 2025",
    description="""
    API Prediksi Volume Sampah Berbasis AI untuk tantangan CASE 2.
    Sistem menggunakan Model Transformer (Amazon Chronos) untuk memprediksi tumpukan sampah 
    berdasarkan anomali cuaca (BMKG) dan izin keramaian (Event Data).
    
    Fitur Utama:
    - Prediksi Volume Total (Ton)
    - Dekomposisi Sampah (Organik vs Plastik) berdasarkan SIPSN KLHK 2025
    - Rekomendasi Jumlah Armada Truk
    - Status Risiko Operasional (Safe, Warning, Critical)
    - Integrasi Jadwal Event Otomatis
    """,
    version="1.1.0",
    contact={
        "name": "Faril Putra Pratama - SMK Taruna Bangsa",
        "url": "https://github.com/vibe-coder",
    }
)

# Menambahkan dukungan CORS agar Frontend bisa mengakses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 2. MODEL & DATA LOADING (STARTUP)
# ==========================================
pipeline = None
df_history = None
events_data = {}

@app.on_event("startup")
def load_assets():
    global pipeline, df_history, events_data
    logger.info("⏳ Menyiapkan AI Engine (Chronos-T5)...")
    try:
        pipeline = ChronosPipeline.from_pretrained(
            "amazon/chronos-t5-tiny",
            device_map="cpu", 
            torch_dtype=torch.float32,
        )
        
        dataset_path = 'dataset_vibe_coder_2025.csv'
        if os.path.exists(dataset_path):
            df_history = pd.read_csv(dataset_path)
            logger.info("✅ Dataset & Model AI berhasil dimuat.")
        else:
            logger.warning(f"⚠️ Warning: {dataset_path} tidak ditemukan!")
            
        # Memuat jadwal event jika ada
        event_path = 'event_jakarta_2025.txt'
        if os.path.exists(event_path):
            df_events = pd.read_csv(event_path)
            for _, row in df_events.iterrows():
                if str(row['Ada_Event']) == '1':
                    events_data[str(row['Tanggal'])] = {
                        'Nama_Event': row['Nama_Event'],
                        'Lokasi': row['Lokasi_Utama']
                    }
            logger.info(f"✅ Jadwal {len(events_data)} event otomatis berhasil dimuat.")
        else:
            logger.warning(f"⚠️ Warning: {event_path} tidak ditemukan!")
            
    except Exception as e:
        logger.error(f"❌ Gagal memuat asset: {e}")

# ==========================================
# 3. SCHEMA VALIDATION (DATA MODELS)
# ==========================================
class PredictionRequest(BaseModel):
    hari_ke_depan: int = Field(7, ge=1, le=30, description="Durasi prediksi (1-30 hari)")
    prediksi_hujan_bmkg: float = Field(0.0, ge=0, description="Estimasi curah hujan (mm)")
    skala_keramaian: int = Field(0, ge=0, le=3, description="Skala event manual (0=Normal, 1=Kecil, 2=Menengah, 3=Besar) jika jadwal otomatis tidak ada.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "hari_ke_depan": 7,
                    "prediksi_hujan_bmkg": 25.5,
                    "skala_keramaian": 0
                }
            ]
        }
    }

class PredictionResult(BaseModel):
    tanggal: str
    total_volume_ton: float
    sisa_makanan_ton: float
    plastik_ton: float
    rekomendasi_truk: int
    status_risiko: str
    info_event: Optional[str] = Field(None, description="Informasi jika ada event besar di hari ini")

# ==========================================
# 4. ENDPOINT LOGIC (BUSINESS LAYER)
# ==========================================
@app.get("/", tags=["Sistem"])
def status_check():
    return {
        "status": "Online", 
        "model": "Chronos-T5 Tiny", 
        "region": "Jakarta Pusat",
        "events_loaded": len(events_data)
    }

def perform_inference(context_tensor, steps):
    """Fungsi sync untuk inference model yang akan dijalankan di threadpool"""
    forecast = pipeline.predict(context_tensor.unsqueeze(0), steps)
    return np.quantile(forecast[0].numpy(), 0.5, axis=0)

@app.post("/api/v1/predict", response_model=List[PredictionResult], tags=["Prediksi Sampah"])
async def get_waste_forecast(request: PredictionRequest):
    if df_history is None or pipeline is None:
        raise HTTPException(status_code=503, detail="Model atau Dataset belum siap.")

    try:
        # 1. Konteks Data Historis
        context = torch.tensor(df_history['Volume_Total_Ton'].values)
        
        # 2. Forecasting Probabilistik (Asynchronous / Non-blocking)
        logger.info(f"⏳ Memprediksi {request.hari_ke_depan} hari ke depan...")
        median_forecast = await run_in_threadpool(perform_inference, context, request.hari_ke_depan)

        # 3. Integrasi Faktor Luar (Case 2: Cuaca & Event Otomatis)
        results = []
        last_date = pd.to_datetime(df_history['TANGGAL'].iloc[-1])

        for i, val in enumerate(median_forecast):
            current_date = last_date + timedelta(days=i+1)
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Logika tambahan berat sampah basah karena hujan
            rain_impact = (request.prediksi_hujan_bmkg * 2) if request.prediksi_hujan_bmkg > 20 else 0
            
            # Logika otomatis vs manual untuk Event
            event_info = events_data.get(date_str)
            if event_info:
                # Jika ada di jadwal kalender otomatis (misal Konser Maroon 5), asumsikan lonjakan super besar
                event_impact = 350 # Ton ekstra
                info_text = f"{event_info['Nama_Event']} di {event_info['Lokasi']}"
            else:
                # Fallback ke skala input manual
                event_impact = request.skala_keramaian * 150
                info_text = None
            
            total_vol = float(val + rain_impact + event_impact)

            # Dekomposisi berdasarkan Data SIPSN KLHK 2025 Jakarta Pusat
            food_waste = total_vol * 0.4987
            plastic_waste = total_vol * 0.2295

            # Rekomendasi Armada (Kapasitas Truk Standar: 10 Ton)
            num_trucks = int(np.ceil(total_vol / 10))

            # Penentuan Status Risiko
            if total_vol > 1300:
                risk = "CRITICAL ⚠️"
            elif total_vol > 1100:
                risk = "WARNING ⚡"
            else:
                risk = "SAFE ✅"

            results.append(
                PredictionResult(
                    tanggal=date_str,
                    total_volume_ton=round(total_vol, 2),
                    sisa_makanan_ton=round(food_waste, 2),
                    plastik_ton=round(plastic_waste, 2),
                    rekomendasi_truk=num_trucks,
                    status_risiko=risk,
                    info_event=info_text
                )
            )

        logger.info("✅ Prediksi berhasil digenerate.")
        return results

    except Exception as e:
        logger.error(f"❌ Gagal memproses prediksi: {e}")
        raise HTTPException(status_code=500, detail=str(e))