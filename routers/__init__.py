from .predict import router as predict_router
from .autopilot import router as autopilot_router
from .alerts import router as alerts_router
from .news import router as news_router
from .kecamatan import router as kecamatan_router
from .seo import router as seo_router
from .system import router as system_router

__all__ = [
    "predict_router",
    "autopilot_router",
    "alerts_router",
    "news_router",
    "kecamatan_router",
    "seo_router",
    "system_router"
]
