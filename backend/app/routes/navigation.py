"""StadiumOS AI — Navigation Routes (mock data)"""

from __future__ import annotations

import sys, pathlib, uuid
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from schemas.navigation import NavigationRequest, NavigationResponse, RouteStep, StadiumZone

router = APIRouter()

# ── Static zone catalog ──────────────────────────────────────────────
ZONES: list[StadiumZone] = [
    StadiumZone(zone_id="NS-A", name="North Stand Gate A", type="gate", level=0, accessible=True),
    StadiumZone(zone_id="NS-B", name="North Stand Gate B", type="gate", level=0, accessible=True),
    StadiumZone(zone_id="SS-A", name="South Stand Gate C", type="gate", level=0, accessible=True),
    StadiumZone(zone_id="ES-A", name="East Stand Lower Tier", type="stand", level=1, accessible=True),
    StadiumZone(zone_id="ES-B", name="East Stand Upper Tier", type="stand", level=2, accessible=False),
    StadiumZone(zone_id="WS-VIP", name="VIP Lounge West", type="vip", level=2, accessible=True),
    StadiumZone(zone_id="CON-N", name="North Concourse", type="concourse", level=1, accessible=True),
    StadiumZone(zone_id="CON-S", name="South Concourse", type="concourse", level=1, accessible=True),
    StadiumZone(zone_id="CON-W", name="West Concourse", type="concourse", level=1, accessible=True),
    StadiumZone(zone_id="MED-1", name="Medical Bay 1", type="service", level=0, accessible=True),
    StadiumZone(zone_id="FZ-W", name="Fan Zone West Plaza", type="gate", level=0, accessible=True),
    StadiumZone(zone_id="FLD", name="Pitch / Field Level", type="field", level=0, accessible=False),
    StadiumZone(zone_id="PRESS", name="Press Box", type="vip", level=3, accessible=True),
    StadiumZone(zone_id="FC-N", name="Food Court North", type="concourse", level=1, accessible=True),
    StadiumZone(zone_id="FC-S", name="Food Court South", type="concourse", level=1, accessible=True),
]


def _mock_route(req: NavigationRequest) -> NavigationResponse:
    now = datetime.now(tz=timezone.utc)
    is_accessible = req.accessibility_preference is not None

    steps = [
        RouteStep(
            instruction=f"Exit {req.start_location} and proceed east along the main concourse.",
            distance_m=120,
            duration_s=90,
            congestion_level="medium",
        ),
        RouteStep(
            instruction="Turn right at the digital wayfinding screen and follow signs for the North Concourse.",
            distance_m=85,
            duration_s=65,
            congestion_level="low",
        ),
        RouteStep(
            instruction="Take the escalator to Level 1." if not is_accessible else "Take Elevator C1 to Level 1 (wheelchair accessible).",
            distance_m=15,
            duration_s=40 if not is_accessible else 55,
            congestion_level="low",
        ),
        RouteStep(
            instruction="Continue straight through Section N-12, past Food Court North.",
            distance_m=200,
            duration_s=150,
            congestion_level="high",
        ),
        RouteStep(
            instruction=f"Arrive at {req.destination}. Your seat is in Row 14, Section N-12.",
            distance_m=30,
            duration_s=25,
            congestion_level="low",
        ),
    ]

    total_dist = sum(s.distance_m for s in steps)
    total_dur = sum(s.duration_s for s in steps)

    return NavigationResponse(
        route_id=f"RT-{uuid.uuid4().hex[:8].upper()}",
        steps=steps,
        total_distance_m=total_dist,
        total_duration_s=total_dur,
        eta=now + timedelta(seconds=total_dur),
        congestion_aware=True,
        accessibility_adapted=is_accessible,
        alternative_available=True,
    )


# ── Routes ───────────────────────────────────────────────────────────
@router.post("/route", response_model=NavigationResponse)
async def create_route(req: NavigationRequest):
    """Generate a mock navigation route between two stadium locations."""
    return _mock_route(req)


@router.get("/zones", response_model=list[StadiumZone])
async def list_zones():
    """Return all navigable stadium zones."""
    return ZONES
