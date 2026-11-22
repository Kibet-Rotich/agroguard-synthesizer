import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api import router

app = FastAPI(title="AgroGuard Synthesizer API", version="1.0")
templates = Jinja2Templates(directory="templates")

# Register the synthesizer routes
app.include_router(router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    """Serves the minimalistic vanilla JS frontend."""
    return templates.TemplateResponse("index.html", {"request": request})