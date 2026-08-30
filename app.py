"""
AETERNA AI — Waste Forecasting & Decision Intelligence Platform DKI Jakarta

FastAPI Application Entry Point
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config.settings import APP_TITLE, APP_DESCRIPTION, APP_VERSION
from core.config import KECAMATAN_DATABASE, ALLOWED_LOCATIONS
from core.timezone import get_jakarta_now
from core.model_loader import load_assets
from routers import (
    predict_router,
    autopilot_router,
    alerts_router,
    news_router,
    kecamatan_router,
    seo_router,
    system_router
)

# Re-export schemas for 100% backward compatibility with test suites and external callers
from schemas import (
    PredictionRequest,
    PredictionResult,
    PredictionData,
    APIResponse,
    LogisticsPlan,
    FleetBreakdown,
    ManpowerBreakdown,
    CollectionTimeBreakdown,
    OperationalEfficiencyBreakdown,
    ReliabilityBreakdown,
    UIPresentation,
    AlertResponse,
    NewsItem
)

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# FastAPI Lifespan Handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await load_assets()
    yield
    # Shutdown

# Initialize FastAPI App
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Assets
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include Routers
app.include_router(system_router)
app.include_router(predict_router)
app.include_router(autopilot_router)
app.include_router(alerts_router)
app.include_router(news_router)
app.include_router(kecamatan_router)
app.include_router(seo_router)
