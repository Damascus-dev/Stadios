"""StadiumOS AI — Alerts Schema Models"""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class Alert(BaseModel):
    id: str
    type: str = Field(..., description="crowd | medical | security | weather | infrastructure")
    severity: str = Field(..., description="critical | high | medium | low")
    title: str
    message: str
    zone: str
    timestamp: datetime
    acknowledged: bool = False
    recommended_action: str


class AlertsResponse(BaseModel):
    alerts: list[Alert]
    total: int
    unacknowledged_count: int
