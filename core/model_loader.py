"""
AETERNA AI — Model Loader and Global Asset State
"""

import os
import sys
import logging
import joblib
import torch
import pandas as pd
from typing import Dict, Any, Optional
from chronos import ChronosPipeline

logger = logging.getLogger(__name__)

# Global Model & Data References
pipeline: Optional[ChronosPipeline] = None
model_gbr: Optional[Any] = None
model_meta: Dict[str, Any] = {}
df_history: Optional[pd.DataFrame] = None
events_data: Dict[str, Dict[str, Any]] = {}

def get_base_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

async def load_assets():
    """Load machine learning models, training history, and event calendar."""
    global pipeline, model_gbr, model_meta, df_history, events_data
    base_dir = get_base_dir()
    logger.info("⏳ Initializing multi-region AI models...")

    try:
        # 1. Chronos Transformer Pipeline
        pipeline = ChronosPipeline.from_pretrained("amazon/chronos-t5-tiny", device_map="cpu", torch_dtype=torch.float32)
        logger.info("✅ Amazon Chronos-T5 Tiny pipeline loaded")

        # 2. Stacking Regressor Model & Metadata
        model_path = os.path.join(base_dir, "models", "model_sampah_advanced.pkl")
        meta_path = os.path.join(base_dir, "models", "model_metadata.pkl")

        if not os.path.exists(model_path) or not os.path.exists(meta_path):
            logger.info("⚡ Model/Metadata not found. Triggering automated dataset generation and Spatial ML training...")
            scripts_dir = os.path.join(base_dir, "scripts")
            if base_dir not in sys.path:
                sys.path.insert(0, base_dir)
            if scripts_dir not in sys.path:
                sys.path.insert(0, scripts_dir)
            import scripts.build_and_train as builder
            builder.run_pipeline()

        if os.path.exists(model_path):
            model_gbr = joblib.load(model_path)
            logger.info(f"✅ Spatial Stacking Regressor model loaded from {model_path}")
        if os.path.exists(meta_path):
            model_meta = joblib.load(meta_path)
            logger.info(f"✅ Model metadata loaded: Metrics={model_meta.get('metrics', {})}")

        # 3. Synthetic Spatial Training Dataset
        csv_path = os.path.join(base_dir, "data", "synthetic_spatial_training_data_2024_2025.csv")
        if not os.path.exists(csv_path):
            csv_path = os.path.join(base_dir, "data", "dataset_real_kecamatan_2024_2025.csv")
        
        df_history = pd.read_csv(csv_path)
        if "Tanggal" in df_history.columns:
            df_history.rename(columns={"Tanggal": "TANGGAL"}, inplace=True)
        df_history["TANGGAL"] = pd.to_datetime(df_history["TANGGAL"]).dt.strftime("%Y-%m-%d")
        logger.info(f"✅ Synthetic spatial training dataset loaded: {len(df_history)} records")

        # 4. Event Calendar
        event_file = os.path.join(base_dir, "data", "event_jakarta_2026.txt")
        if os.path.exists(event_file):
            df_e = pd.read_csv(event_file)
            df_e.columns = [c.strip().lower() for c in df_e.columns]
            for _, r in df_e.iterrows():
                if str(r.get("ada_event", "1")) == "1":
                    dk = str(r.get("tanggal", "")).strip()
                    if dk:
                        raw_jiwa = float(r.get("jumlah_jiwa", r.get("skala_keramaian", 0)))
                        crowd_jiwa = raw_jiwa * 20000.0 if (0 < raw_jiwa <= 5) else raw_jiwa
                        events_data[dk] = {
                            "event_name": str(r.get("nama_event", "")),
                            "location": str(r.get("lokasi", "")),
                            "crowd_scale": crowd_jiwa,
                            "jumlah_jiwa": crowd_jiwa
                        }
            logger.info(f"✅ Event calendar loaded: {len(events_data)} entries")
    except Exception as e:
        logger.error(f"❌ Startup asset loading failed: {e}", exc_info=True)
        raise
