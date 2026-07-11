"""StadiumOS AI — FastAPI Backend Server"""
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from .routes import dashboard, navigation, alerts, agents, stadium
from .auth import routes as auth_routes

print(f"LLM Provider: {os.getenv('LLM_PROVIDER', 'deepseek')}")
print(f"DeepSeek configured: {bool(os.getenv('DEEPSEEK_API_KEY'))}")
print(f"Gemini configured: {bool(os.getenv('GEMINI_API_KEY'))}")

ENABLE_DOCS = os.getenv("ENABLE_DOCS", "").lower() in ("1", "true", "yes")

app = FastAPI(
    title="StadiumOS AI",
    description="AI Operating System for FIFA World Cup 2026 Stadium Operations",
    version="0.1.0",
    docs_url="/docs" if ENABLE_DOCS else None,
    redoc_url="/redoc" if ENABLE_DOCS else None,
)

# CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        FRONTEND_URL,
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount route modules
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(navigation.router, prefix="/api/navigation", tags=["Navigation"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(stadium.router, tags=["Stadium"])


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "StadiumOS AI"}
