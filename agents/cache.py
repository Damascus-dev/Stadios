"""StadiumOS AI — Cache/Fallback Layer

Pre-computed responses for all 3 demo scenarios (v4 Task 4.3).
The rehearsed demo path never depends on a live Gemini call succeeding.
"""

from schemas.agents import AgentResponse


PRIMARY_SCENARIO_QUERIES: dict[str, AgentResponse] = {
    "what is the current crowd status": AgentResponse(
        agent_type="operations",
        response_text=(
            "Current operations status: North Stand is at critical density (92%). "
            "East Wing Food Court is at 95% and rising. "
            "I recommend rerouting pedestrian flow via the South Corridor to reduce congestion by ~30%."
        ),
        structured_data={
            "predictions": [
                {"zone": "North Stand", "risk_level": "critical", "confidence": 0.94},
                {"zone": "East Wing Food Court", "risk_level": "critical", "confidence": 0.91},
                {"zone": "Main Concourse", "risk_level": "high", "confidence": 0.87},
            ],
            "volunteer_recommendations": [
                {"zone": "Gate A", "count": 5, "reason": "Expected 2nd-half crowd surge"},
                {"zone": "Food Court", "count": 3, "reason": "Critical density — need crowd control"},
            ],
            "transportation_signal": {
                "shuttle_load_pct": 72.0,
                "parking_capacity_pct": 45.0,
                "exit_congestion": "moderate",
                "prediction_text": "Peak shuttle demand expected at T+85min. Pre-positioning 4 additional buses.",
            },
            "sustainability_signal": {
                "energy_load_kwh": 2450.0,
                "waste_generation_kg": 890.0,
                "water_usage_liters": 12400.0,
                "crowd_correlation_factor": 0.87,
                "trend": "elevated",
            },
        },
        recommendations=[
            "Reroute pedestrian flow from East Wing via South Corridor to reduce congestion by ~30%",
            "Deploy 5 additional volunteers to Gate A for expected 2nd-half crowd surge",
            "Activate backup wheelchair ramp at Section 300 — primary ramp queue exceeds 8 min",
        ],
        confidence=0.94,
        cached=True,
    ),
    "reroute traffic": AgentResponse(
        agent_type="navigation",
        response_text=(
            "I've calculated the optimal reroute. From Gate A, take the South Corridor "
            "instead of the Main Concourse to avoid the 95% density at East Wing Food Court. "
            "Total distance: 550m, estimated time: ~11 minutes."
        ),
        structured_data={
            "recommended_route_id": "RT-ALT-7F3",
            "estimated_time_s": 660,
            "congestion_avoided": ["East Wing Food Court", "Main Concourse"],
            "accessibility_options": ["Elevator 2A is on this route"],
        },
        recommendations=[
            "Use South Corridor — congestion is LOW compared to Main Concourse",
            "Elevator 2A is available for wheelchair access",
        ],
        confidence=0.92,
        cached=True,
    ),
}

BACKUP_A_QUERIES: dict[str, AgentResponse] = {
    "i need a wheelchair accessible route": AgentResponse(
        agent_type="accessibility",
        response_text=(
            "I've identified an accessible route for you. "
            "Use Elevator C1 (east side) to Level 2, then follow the wide corridor "
            "past the Sensory Room to Section 214. "
            "All ramps and elevators on this route are confirmed operational. "
            "Elevator 3B on the West Concourse is currently out of service — avoid that area."
        ),
        structured_data={
            "accessibility_type": "wheelchair",
            "adapted_instructions": [
                "Proceed to Elevator C1 on the east side of the Main Concourse",
                "Take Elevator C1 to Level 2",
                "Exit and follow the wide corridor toward the Sensory Room",
                "Continue past the Sensory Room to Section 214",
            ],
            "language": "en",
            "emergency_mode": False,
            "alternative_formats": {"text": True, "audio_description": False},
        },
        recommendations=[
            "Use Elevator C1 — it's the only fully accessible elevator near your location",
            "Avoid West Concourse — Elevator 3B is out of service",
            "Accessible restrooms are available at Section 214 on Level 2",
        ],
        confidence=0.95,
        cached=True,
    ),
}

BACKUP_B_QUERIES: dict[str, AgentResponse] = {
    "transportation status": AgentResponse(
        agent_type="operations",
        response_text=(
            "Transportation status: All gates are experiencing heavy exit congestion. "
            "Gate A is at 95% density, Gate D is at 97%. "
            "Shuttle load is at 98% capacity. "
            "I recommend activating the overflow shuttle staging area and redirecting fans to Gates B and C."
        ),
        structured_data={
            "transportation_signal": {
                "shuttle_load_pct": 98.0,
                "parking_capacity_pct": 95.0,
                "exit_congestion": "severe",
                "prediction_text": "Exit bottleneck at Gate D — shuttle queue exceeding 45 minutes",
            },
            "recommendations": [
                "Activate overflow shuttle staging at Lot E",
                "Redirect exiting fans to Gates B and C to balance load",
                "Pre-stage 12 additional shuttle buses at North Exit",
            ],
        },
        recommendations=[
            "Activate overflow shuttle staging at Lot E immediately",
            "Redirect exiting fans to Gates B and C",
            "Pre-stage 12 additional shuttle buses at North Exit",
        ],
        confidence=0.91,
        cached=True,
    ),
}


CACHE: dict[str, dict[str, AgentResponse]] = {
    "primary": PRIMARY_SCENARIO_QUERIES,
    "backup_a": BACKUP_A_QUERIES,
    "backup_b": BACKUP_B_QUERIES,
}


def get_all_cache_entries() -> list[AgentResponse]:
    entries: list[AgentResponse] = []
    for scenario in CACHE.values():
        entries.extend(scenario.values())
    return entries


def find_cache_entry(query: str) -> AgentResponse | None:
    q = query.lower().strip()
    for scenario in CACHE.values():
        for cached_query, response in scenario.items():
            if cached_query in q or q in cached_query:
                return response
    return None
