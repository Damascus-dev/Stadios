"""StadiumOS AI — Agent Routes (mock data)"""

from __future__ import annotations

import sys, pathlib
from typing import Literal

from fastapi import APIRouter, HTTPException

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from schemas.agents import AgentQuery, AgentResponse

router = APIRouter()

# ── Mock responses per agent type ────────────────────────────────────

_AGENT_RESPONSES: dict[str, AgentResponse] = {
    "navigation": AgentResponse(
        agent_type="navigation",
        response_text=(
            "Based on current crowd density data, the fastest route from North Stand Gate A "
            "to your seat in Section E-08 is via the North Concourse bypass. This avoids the "
            "congested main corridor (88 % density) and saves approximately 3 minutes. "
            "I've also flagged an accessible alternative using Elevator C1 if needed."
        ),
        structured_data={
            "recommended_route_id": "RT-7A3F1B2C",
            "estimated_time_s": 370,
            "congestion_avoided": ["CON-N main corridor"],
            "accessibility_options": ["Elevator C1 → Level 1"],
        },
        recommendations=[
            "Take the North Concourse bypass to avoid 88 % congestion.",
            "Follow digital signage screens NS-07 through NS-12 for real-time updates.",
            "If you need wheelchair access, Elevator C1 is available on the east side.",
        ],
        confidence=0.92,
        cached=False,
    ),
    "operations": AgentResponse(
        agent_type="operations",
        response_text=(
            "Current operations status: North Stand Gate A is at critical density (92 %). "
            "I recommend opening auxiliary Gate A2 immediately and redeploying 6 volunteers "
            "from the under-utilised South Concourse. Shuttle bus pre-staging for the "
            "post-match surge should begin within the next 15 minutes. Energy consumption "
            "is 4,851 kWh — 7 % above baseline — due to all floodlights being at full power."
        ),
        structured_data={
            "gate_a_density_pct": 92.1,
            "recommended_volunteer_redeployment": 6,
            "shuttle_prestage_eta_min": 15,
            "energy_kwh": 4850.7,
            "energy_vs_baseline_pct": 7.0,
            "transportation": {
                "shuttle_load_pct": 68.5,
                "parking_remaining_pct": 8.8,
            },
            "sustainability": {
                "energy_load_kwh": 4850.7,
                "waste_kg": 1237.4,
                "water_liters": 18420.0,
            },
        },
        recommendations=[
            "Open auxiliary Gate A2 to relieve North Stand pressure.",
            "Redeploy 6 volunteers from South Concourse to North Stand.",
            "Pre-stage 12 shuttle buses at North Exit for post-match surge.",
            "Dim South Concourse lighting to 60 % — estimated savings 12 kWh/hr.",
            "Alert parking team: Lot A is 91 % full — begin overflow signage.",
        ],
        confidence=0.89,
        cached=False,
    ),
    "accessibility": AgentResponse(
        agent_type="accessibility",
        response_text=(
            "Accessibility status update: Elevator B3 on the West Concourse is currently "
            "offline (door sensor fault, ETA 15 min). I've identified a portable ramp in "
            "Logistics Room W-04 that can be deployed at Section W-12 to maintain wheelchair "
            "access to Level 2. Audio descriptions for the match are available on Channel 4 "
            "of the stadium radio system. There are 23 sensory-quiet pods available across "
            "the stadium — 8 in the North Concourse and 15 in the South Concourse."
        ),
        structured_data={
            "elevator_b3_status": "offline",
            "elevator_b3_eta_min": 15,
            "portable_ramp_location": "Logistics Room W-04",
            "ramp_deploy_target": "Section W-12",
            "audio_description_channel": 4,
            "sensory_pods": {"total": 23, "north": 8, "south": 15},
            "wheelchair_accessible_restrooms": 12,
            "sign_language_interpreters_on_duty": 4,
        },
        recommendations=[
            "Deploy portable ramp from W-04 to Section W-12 immediately.",
            "Announce Elevator B3 outage on accessibility PA channel.",
            "Direct wheelchair users to Elevator C1 (east side) as alternative.",
            "Ensure sensory-quiet pods in North Concourse are staffed.",
            "Verify hearing-loop system is active in Sections N-10 through N-14.",
        ],
        confidence=0.95,
        cached=False,
    ),
}


# ── Route ────────────────────────────────────────────────────────────
@router.post("/{agent_type}", response_model=AgentResponse)
async def query_agent(agent_type: str, body: AgentQuery):
    """Send a natural-language query to one of the three AI agents and get a structured response."""
    if agent_type not in _AGENT_RESPONSES:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown agent type '{agent_type}'. Valid types: navigation, operations, accessibility",
        )
    return _AGENT_RESPONSES[agent_type]
