import os
import httpx
from cachetools import TTLCache

WEATHER_AI_API_KEY = os.getenv("WEATHER_AI_API_KEY")
BASE_URL = "https://api.weather-ai.co"

# LRU Cache: Stores up to 100 coordinates for 1 hour
weather_cache = TTLCache(maxsize=100, ttl=3600)

async def fetch_weather_data(lat: float, lon: float) -> dict:
    """Fetches 7-day weather forecast and AI insights from Weather-AI."""
    cache_key = f"{lat},{lon}"
    if cache_key in weather_cache:
        return weather_cache[cache_key]

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/v1/weather",
            params={"lat": lat, "lon": lon, "days": 7, "ai": "true"},
            headers={"Authorization": f"Bearer wai_{WEATHER_AI_API_KEY}"},
            timeout=10.0
        )
        response.raise_for_status()
        data = response.json()
        weather_cache[cache_key] = data
        return data

async def analyze_farm_image(image_bytes: bytes, filename: str, content_type: str, acres: float = None) -> dict:
    """Transmits drone/satellite imagery to Weather-AI CV engine."""
    async with httpx.AsyncClient() as client:
        files = {"image": (filename, image_bytes, content_type)}
        data = {}
        if acres:
            data["landAcres"] = str(acres)

        response = await client.post(
            f"{BASE_URL}/v1/trees/analyze",
            headers={"Authorization": f"Bearer wai_{WEATHER_AI_API_KEY}"},
            files=files,
            data=data,
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()