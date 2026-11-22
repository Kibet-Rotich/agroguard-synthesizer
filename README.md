# AgroGuard Data Synthesizer

A high-performance orchestration layer utilizing FastAPI to asynchronously merge and synthesize computer vision agronomic data with real-time meteorological forecasts from the Weather-AI API.

## Architecture
- **Framework:** FastAPI (Python)
- **Concurrency:** Non-blocking `httpx` async clients utilized via `asyncio.gather()`.
- **Caching:** TTL memory cache implemented on meteorological routes to preserve API quotas.
- **Data Integration:** Computes a composite vulnerability score by cross-referencing OpenCV canopy health metrics with localized weather patterns.

## Local Setup

1. Initialize the environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt```

2. Add your Weather-AI key:
```bash
export WEATHER_AI_API_KEY=your-key   # see .env.example
```

3. Run the server:
```bash
uvicorn main:app --reload
```

Open http://localhost:8000 for the upload page, or `POST /api/synthesize` with `lat`, `lon`, optional `land_acres` and an `image` file (multipart form).
