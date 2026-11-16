import asyncio
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from .services import fetch_weather_data, analyze_farm_image

router = APIRouter()

@router.post("/synthesize")
async def generate_risk_report(
    lat: float = Form(...),
    lon: float = Form(...),
    land_acres: float = Form(None),
    image: UploadFile = File(...)
):
    try:
        image_bytes = await image.read()
        
        # Dispatch non-blocking concurrent requests
        weather_task = fetch_weather_data(lat, lon)
        trees_task = analyze_farm_image(image_bytes, image.filename, image.content_type, land_acres)
        
        weather_data, trees_data = await asyncio.gather(weather_task, trees_task)
        
        # Synthesis Engine: Calculate Vulnerability Score
        health = trees_data.get("tree_health", {})
        needs_care = health.get("needs_care", 0)
        needs_repl = health.get("needs_replacement", 0)
        total_trees = trees_data.get("total_tree_count", 1)
        
        # Base risk derived from CV canopy analysis
        base_risk = ((needs_care + needs_repl) / total_trees) * 100
        
        # Cross-reference with weather forecast
        weather_summary = str(weather_data).lower()
        if "rain" in weather_summary or "storm" in weather_summary:
            vulnerability_score = min(base_risk * 1.3, 100.0) # Penalty for poor health during storms
        elif "drought" in weather_summary or "heat" in weather_summary:
            vulnerability_score = min(base_risk * 1.5, 100.0)
        else:
            vulnerability_score = base_risk

        # Categorize risk
        if vulnerability_score > 70:
            risk_level = "CRITICAL"
        elif vulnerability_score > 35:
            risk_level = "ELEVATED"
        else:
            risk_level = "NOMINAL"
            
        return {
            "synthesis": {
                "vulnerability_score": round(vulnerability_score, 2),
                "risk_level": risk_level,
                "flags": [
                    f"Identified {needs_care + needs_repl} compromised trees.",
                    "Risk score adjusted via 7-day meteorological cross-reference."
                ]
            },
            "raw_data": {
                "cv_analysis": trees_data,
                "meteorology": weather_data
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))