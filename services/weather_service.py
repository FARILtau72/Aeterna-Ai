"""
AETERNA AI — Weather Service (Open-Meteo Integration)
"""

import httpx
import logging
from datetime import datetime, timedelta
from typing import Dict

logger = logging.getLogger(__name__)

# In-memory 30-minute weather cache
WEATHER_CACHE: Dict[str, tuple] = {}

async def fetch_rainfall_forecast(lat: float, lon: float, days: int) -> Dict[str, float]:
    """
    Fetch daily rainfall forecast from Open-Meteo API with in-memory caching.
    
    Returns:
        Dict mapping date string (YYYY-MM-DD) to precipitation sum (mm).
    """
    cache_key = f"{lat:.2f}_{lon:.2f}_{days}"
    now = datetime.now()

    if cache_key in WEATHER_CACHE:
        cached_data, timestamp = WEATHER_CACHE[cache_key]
        if now - timestamp < timedelta(minutes=30):
            logger.info(f"⚡ Weather cache hit for {cache_key}")
            return cached_data

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=precipitation_sum&timezone=Asia/Jakarta"
        f"&forecast_days={days}&past_days=2"
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=2.0)
            if response.status_code == 200:
                data = response.json()
                daily = data.get("daily", {})
                times = daily.get("time", [])
                precip = daily.get("precipitation_sum", [])
                result = {times[i]: float(precip[i]) for i in range(len(times)) if i < len(precip)}
                WEATHER_CACHE[cache_key] = (result, now)
                return result
    except Exception as e:
        logger.error(f"Failed to fetch weather from Open-Meteo ({lat}, {lon}): {e}")

    return {}
