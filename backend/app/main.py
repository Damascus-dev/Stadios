"""StadiumOS AI — FastAPI Backend Server"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import dashboard, navigation, alerts, agents

app = FastAPI(
    title="StadiumOS AI",
    description="AI Operating System for FIFA World Cup 2026 Stadium Operations",
    version="0.1.0",
)

# CORS for frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount route modules
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(navigation.router, prefix="/api/navigation", tags=["Navigation"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "StadiumOS AI"}
