"""StadiumOS AI — Dashboard Route (mock data)"""

from __future__ import annotations

import sys, pathlib
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter

# Allow importing schemas from project root
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from schemas.dashboard import (
    DashboardResponse,
    StadiumHealth,
    CrowdZone,
    CrowdHeat,
    VolunteerAssignment,
    VolunteerStatus,
    SeverityBreakdown,
    IncidentCount,
    AlertSummary,
    ActiveAlerts,
    AIRecommendation,
    ExitCongestion,
    TransportationStatus,
    SustainabilityMetrics,
)

router = APIRouter()

# ── Helpers ──────────────────────────────────────────────────────────
_NOW = datetime(2026, 7, 7, 19, 45, 0, tzinfo=timezone.utc)  # Match‑day evening


def _mock_dashboard() -> DashboardResponse:
    return DashboardResponse(
        stadium_health=StadiumHealth(
            overall_score=87.3,
            status="green",
            capacity_pct=78.5,
            active_zones=14,
        ),
        crowd_heat=CrowdHeat(
            zones=[
                CrowdZone(zone_id="NS-A", name="North Stand Gate A", density_pct=92.1, trend="rising", risk_level="high"),
                CrowdZone(zone_id="NS-B", name="North Stand Gate B", density_pct=74.3, trend="stable", risk_level="medium"),
                CrowdZone(zone_id="SS-A", name="South Stand Gate C", density_pct=61.8, trend="falling", risk_level="low"),
                CrowdZone(zone_id="ES-A", name="East Stand Lower Tier", density_pct=85.4, trend="rising", risk_level="high"),
                CrowdZone(zone_id="WS-VIP", name="VIP Lounge West", density_pct=45.2, trend="stable", risk_level="low"),
                CrowdZone(zone_id="CON-N", name="North Concourse", density_pct=88.7, trend="rising", risk_level="high"),
                CrowdZone(zone_id="CON-S", name="South Concourse", density_pct=52.3, trend="stable", risk_level="low"),
                CrowdZone(zone_id="FZ-W", name="Fan Zone West Plaza", density_pct=71.6, trend="rising", risk_level="medium"),
            ]
        ),
        volunteer_status=VolunteerStatus(
            total=420,
            deployed=387,
            available=33,
            zones=[
                VolunteerAssignment(zone_id="NS-A", zone_name="North Stand Gate A", count=42, role="crowd-management"),
                VolunteerAssignment(zone_id="SS-A", zone_name="South Stand Gate C", count=38, role="crowd-management"),
                VolunteerAssignment(zone_id="CON-N", zone_name="North Concourse", count=55, role="wayfinding"),
                VolunteerAssignment(zone_id="WS-VIP", zone_name="VIP Lounge West", count=18, role="hospitality"),
                VolunteerAssignment(zone_id="MED-1", zone_name="Medical Bay 1", count=12, role="first-aid"),
                VolunteerAssignment(zone_id="FZ-W", zone_name="Fan Zone West Plaza", count=30, role="wayfinding"),
            ],
        ),
        incident_count=IncidentCount(
            active=7,
            resolved=23,
            total=30,
            by_severity=SeverityBreakdown(critical=1, high=2, medium=3, low=1),
        ),
        active_alerts=ActiveAlerts(
            alerts=[
                AlertSummary(
                    id="ALT-001",
                    type="crowd",
                    severity="critical",
                    message="North Stand Gate A approaching maximum safe density — 92 % occupied",
                    zone="NS-A",
                    timestamp=_NOW - timedelta(minutes=4),
                ),
                AlertSummary(
                    id="ALT-002",
                    type="medical",
                    severity="high",
                    message="Heat-related incident reported at East Stand Lower Tier — medical team dispatched",
                    zone="ES-A",
                    timestamp=_NOW - timedelta(minutes=11),
                ),
                AlertSummary(
                    id="ALT-003",
                    type="infrastructure",
                    severity="medium",
                    message="Elevator B3 offline on West Concourse — technician en route, ETA 15 min",
                    zone="CON-W",
                    timestamp=_NOW - timedelta(minutes=22),
                ),
            ]
        ),
        ai_recommendations=[
            AIRecommendation(
                id="REC-001",
                type="crowd-flow",
                priority="critical",
                title="Redirect North Stand Ingress",
                description="Gate A is at 92 % density. Open auxiliary Gate A2 and redirect 30 % of incoming fans via the North Concourse bypass to Gate B. Estimated relief in 8 minutes.",
                agent_source="operations",
                confidence=0.94,
            ),
            AIRecommendation(
                id="REC-002",
                type="accessibility",
                priority="high",
                title="Deploy Temporary Ramp at West Concourse",
                description="Elevator B3 is offline. Place a portable ramp at Section W-12 so wheelchair users can reach Level 2 VIP seating. Three portable ramps are stored in Logistics Room W-04.",
                agent_source="accessibility",
                confidence=0.91,
            ),
            AIRecommendation(
                id="REC-003",
                type="navigation",
                priority="medium",
                title="Update Digital Signage — Gate B Promotion",
                description="Gate B is at 74 % — 18 pp below Gate A. Push multilingual wayfinding messages on screens NS-07 through NS-12 to redistribute foot traffic.",
                agent_source="navigation",
                confidence=0.87,
            ),
            AIRecommendation(
                id="REC-004",
                type="sustainability",
                priority="medium",
                title="Dim Non-Essential Lighting in South Concourse",
                description="South Concourse is at only 52 % density. Reduce lighting to 60 % in Sections S-08 through S-14 to save an estimated 12 kWh per hour while maintaining safety standards.",
                agent_source="operations",
                confidence=0.82,
            ),
        ],
        transportation=TransportationStatus(
            shuttle_load_pct=68.5,
            parking_capacity_pct=91.2,
            exit_congestion=[
                ExitCongestion(exit_id="EXIT-N1", name="North Exit — Metro Link", congestion_pct=82.0),
                ExitCongestion(exit_id="EXIT-S1", name="South Exit — Bus Terminal", congestion_pct=45.3),
                ExitCongestion(exit_id="EXIT-E1", name="East Exit — Parking Lot A", congestion_pct=73.1),
                ExitCongestion(exit_id="EXIT-W1", name="West Exit — Ride-Share Zone", congestion_pct=56.8),
            ],
            prediction="Post-match surge expected in 45 min. Recommend pre-staging 12 additional shuttle buses at North Exit.",
        ),
        sustainability=SustainabilityMetrics(
            energy_load_kwh=4850.7,
            waste_generation_kg=1237.4,
            water_usage_liters=18420.0,
            crowd_correlation_factor=0.78,
        ),
        generated_at=_NOW,
    )


# ── Route ────────────────────────────────────────────────────────────
@router.get("/", response_model=DashboardResponse)
async def get_dashboard():
    """Return a full dashboard snapshot with all eight widget payloads."""
    return _mock_dashboard()
