"""StadiumOS AI — Dashboard Schema Models"""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


# ── 1. Stadium Health ────────────────────────────────────────────────
class StadiumHealth(BaseModel):
    overall_score: float = Field(..., ge=0, le=100, description="0‑100 health score")
    status: str = Field(..., description="green | yellow | red")
    capacity_pct: float = Field(..., ge=0, le=100)
    active_zones: int = Field(..., ge=0)


# ── 2. Crowd Heat ────────────────────────────────────────────────────
class CrowdZone(BaseModel):
    zone_id: str
    name: str
    density_pct: float = Field(..., ge=0, le=100)
    trend: str = Field(..., description="rising | stable | falling")
    risk_level: str = Field(..., description="low | medium | high | critical")


class CrowdHeat(BaseModel):
    zones: list[CrowdZone]


# ── 3. Volunteer Status ─────────────────────────────────────────────
class VolunteerAssignment(BaseModel):
    zone_id: str
    zone_name: str
    count: int
    role: str


class VolunteerStatus(BaseModel):
    total: int
    deployed: int
    available: int
    zones: list[VolunteerAssignment]


# ── 4. Incident Count ───────────────────────────────────────────────
class SeverityBreakdown(BaseModel):
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0


class IncidentCount(BaseModel):
    active: int
    resolved: int
    total: int
    by_severity: SeverityBreakdown


# ── 5. Active Alerts ─────────────────────────────────────────────────
class AlertSummary(BaseModel):
    id: str
    type: str
    severity: str
    message: str
    zone: str
    timestamp: datetime


class ActiveAlerts(BaseModel):
    alerts: list[AlertSummary]


# ── 6. AI Recommendation ────────────────────────────────────────────
class AIRecommendation(BaseModel):
    id: str
    type: str
    priority: str = Field(..., description="critical | high | medium | low")
    title: str
    description: str
    agent_source: str = Field(..., description="navigation | operations | accessibility")
    confidence: float = Field(..., ge=0, le=1)


# ── 7. Transportation Status ────────────────────────────────────────
class ExitCongestion(BaseModel):
    exit_id: str
    name: str
    congestion_pct: float = Field(..., ge=0, le=100)


class TransportationStatus(BaseModel):
    shuttle_load_pct: float = Field(..., ge=0, le=100)
    parking_capacity_pct: float = Field(..., ge=0, le=100)
    exit_congestion: list[ExitCongestion]
    prediction: str


# ── 8. Sustainability Metrics ───────────────────────────────────────
class SustainabilityMetrics(BaseModel):
    energy_load_kwh: float
    waste_generation_kg: float
    water_usage_liters: float
    crowd_correlation_factor: float = Field(
        ..., ge=0, le=1,
        description="How strongly crowd density correlates with resource usage",
    )


# ── Aggregated Dashboard Response ────────────────────────────────────
class DashboardResponse(BaseModel):
    stadium_health: StadiumHealth
    crowd_heat: CrowdHeat
    volunteer_status: VolunteerStatus
    incident_count: IncidentCount
    active_alerts: ActiveAlerts
    ai_recommendations: list[AIRecommendation]
    transportation: TransportationStatus
    sustainability: SustainabilityMetrics
    generated_at: datetime
