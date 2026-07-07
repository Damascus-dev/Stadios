"""StadiumOS AI — Navigation Schema Models"""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class NavigationRequest(BaseModel):
    start_location: str = Field(..., description="Starting zone or gate ID")
    destination: str = Field(..., description="Target zone or point of interest")
    accessibility_preference: str | None = Field(
        None, description="wheelchair | visual | hearing | cognitive | None"
    )
    language: str = Field("en", description="ISO 639-1 language code")


class RouteStep(BaseModel):
    instruction: str
    distance_m: float = Field(..., ge=0)
    duration_s: float = Field(..., ge=0)
    congestion_level: str = Field(..., description="low | medium | high")


class StadiumZone(BaseModel):
    zone_id: str
    name: str
    type: str = Field(..., description="gate | stand | concourse | vip | service | field")
    level: int
    accessible: bool = True


class NavigationResponse(BaseModel):
    route_id: str
    steps: list[RouteStep]
    total_distance_m: float
    total_duration_s: float
    eta: datetime
    congestion_aware: bool = True
    accessibility_adapted: bool = False
    alternative_available: bool = False
