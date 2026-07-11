"""StadiumOS AI — Navigation Routes

Three-tier routing:
  1. LLM-driven via orchestrator (richest, context-aware)
  2. Deterministic shortest-path via graph services (always works, congestion-aware)

LLMs interpret state, never own it — graph services are the source of truth.
"""

from __future__ import annotations

import sys
import pathlib
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from pydantic import BaseModel, Field

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from schemas.navigation import NavigationRequest, NavigationResponse, RouteStep, RouteAlternative, StadiumZone
from schemas.agents import AgentQuery
from agents.orchestrator import process_query
from backend.app.state import sim_engine
from backend.app.graph.navigator import find_route, find_alternatives
from backend.app.graph.physical import PhysicalGraph

router = APIRouter()


def _build_query(req: NavigationRequest) -> str:
    parts = [f"I need a route from {req.start_location} to {req.destination}."]
    if req.accessibility_preference:
        parts.append(f" Accessibility preference: {req.accessibility_preference}.")
        if req.accessibility_preference == "wheelchair":
            parts.append(" Only use wheelchair-accessible paths with elevators and ramps.")
        elif req.accessibility_preference == "visual":
            parts.append(" Provide clear high-contrast visual instructions.")
        elif req.accessibility_preference == "hearing":
            parts.append(" Ensure visual indicators are available for all steps.")
    parts.append(" Provide step-by-step directions with distances, times, and congestion levels.")
    return " ".join(parts)


def _parse_steps_from_orchestrator(agent_response) -> list[RouteStep] | None:
    sd = agent_response.structured_data
    if not sd or "steps" not in sd:
        return None
    raw = sd["steps"]
    if not isinstance(raw, list) or len(raw) == 0:
        return None
    try:
        return [
            RouteStep(
                instruction=s["instruction"],
                distance_m=float(s["distance_m"]),
                duration_s=float(s["duration_s"]),
                congestion_level=s["congestion_level"],
            )
            for s in raw
        ]
    except (KeyError, TypeError, ValueError):
        return None


def _parse_explanation_from_orchestrator(agent_response) -> tuple[str, str, str, float, list[RouteAlternative]]:
    sd = agent_response.structured_data or {}
    reason = sd.get("reason", "")
    benefit = sd.get("benefit", "")
    tradeoff = sd.get("tradeoff", "")
    confidence = float(sd.get("confidence", 0.0))
    alternatives = []
    try:
        for a in sd.get("alternatives", []):
            alternatives.append(
                RouteAlternative(
                    description=a.get("description", ""),
                    reason=a.get("reason", ""),
                    tradeoff=a.get("tradeoff", ""),
                    total_distance_m=float(a.get("total_distance_m", 0)),
                    total_duration_s=float(a.get("total_duration_s", 0)),
                    confidence=float(a.get("confidence", 0)),
                )
            )
    except (KeyError, TypeError, ValueError):
        pass
    return reason, benefit, tradeoff, confidence, alternatives


def _build_deterministic_route(start: str, destination: str) -> NavigationResponse | None:
    result = find_route(start, destination)
    if result is None:
        return None

    physical = PhysicalGraph.get()
    congestion = sim_engine.get_state_dict().get("total_attendance", 0) / max(
        sim_engine.get_state_dict().get("stadium_capacity", 82500), 1
    )
    level = "high" if congestion > 0.7 else ("medium" if congestion > 0.4 else "low")

    steps: list[RouteStep] = []
    for i in range(len(result.path) - 1):
        cur = result.path[i]
        nxt = result.path[i + 1]
        cur_node = physical.get_node(cur)
        nxt_node = physical.get_node(nxt)
        edge_dist = next(
            (e.distance_m for e in physical.get_all_edges_for(cur) if e.start_id == cur and e.end_id == nxt or e.start_id == nxt and e.end_id == cur),
            result.total_distance / max(len(result.path) - 1, 1),
        )
        steps.append(
            RouteStep(
                instruction=f"Walk from {cur_node.name if cur_node else cur} to {nxt_node.name if nxt_node else nxt}",
                distance_m=edge_dist,
                duration_s=edge_dist / 1.4,
                congestion_level=level,
            )
        )

    total_dur = result.total_distance / 1.4
    reason = f"Shortest path from {start} to {destination} avoiding highly congested zones"
    benefit = f"Minimum walking distance ({result.total_distance:.0f}m) with congestion-aware weighting"
    tradeoff = "Prioritizes distance over crowd comfort — may pass through moderately busy areas"

    alternatives: list[RouteAlternative] = []
    alt_results = find_alternatives(start, destination, max_alts=2)
    for i, alt in enumerate(alt_results):
        alt_dur = alt.total_distance / 1.4
        alt_name_a = physical.get_node(alt.path[1])
        alt_name_b = physical.get_node(alt.path[-2] if len(alt.path) > 2 else alt.path[-1])
        via = ""
        if alt_name_a and alt_name_b:
            via = f" via {alt_name_a.name}"
        alternatives.append(RouteAlternative(
            description=f"Alternative {i + 1}{via}",
            reason=f"Avoids congestion on primary route — {(alt.total_distance - result.total_distance):.0f}m longer",
            tradeoff=f"Increases walking distance by {(alt.total_distance - result.total_distance):.0f}m, adds {int(alt_dur - total_dur)} min",
            total_distance_m=alt.total_distance,
            total_duration_s=alt_dur,
            confidence=max(0.3, 0.85 - (alt.total_distance - result.total_distance) / result.total_distance * 0.3),
        ))

    return NavigationResponse(
        route_id=f"RT-{uuid.uuid4().hex[:8].upper()}",
        steps=steps,
        total_distance_m=result.total_distance,
        total_duration_s=total_dur,
        eta=datetime.now(tz=timezone.utc) + timedelta(seconds=total_dur),
        congestion_aware=True,
        accessibility_adapted=False,
        alternative_available=True,
        path=result.path,
        reason=reason,
        benefit=benefit,
        tradeoff=tradeoff,
        confidence=0.85,
        alternatives=alternatives,
    )


@router.post("/route", response_model=NavigationResponse)
async def create_route(req: NavigationRequest):
    """Generate a route between two stadium locations.

    Tiers:
      1. LLM-driven route via orchestrator (with simulation context)
      2. Deterministic route engine (congestion-aware, always works)
    """
    print(f"Navigation route: {req.start_location} -> {req.destination} (accessibility={req.accessibility_preference})")

    sim_state = sim_engine.get_state_dict()

    try:
        query = _build_query(req)
        agent_query = AgentQuery(
            query=query,
            agent_type="navigation",
            context={"start_location": req.start_location, "destination": req.destination},
            language=req.language,
        )
        result = process_query(agent_query, sim_state)

        if result.confidence > 0.0:
            steps = _parse_steps_from_orchestrator(result)
            if steps:
                total_dist = sum(s.distance_m for s in steps)
                total_dur = sum(s.duration_s for s in steps)
                is_accessible = req.accessibility_preference is not None
                reason, benefit, tradeoff, confidence, alternatives = _parse_explanation_from_orchestrator(result)
                return NavigationResponse(
                    route_id=f"RT-{uuid.uuid4().hex[:8].upper()}",
                    steps=steps,
                    total_distance_m=total_dist,
                    total_duration_s=total_dur,
                    eta=datetime.now(tz=timezone.utc) + timedelta(seconds=total_dur),
                    congestion_aware=True,
                    accessibility_adapted=is_accessible,
                    alternative_available=True,
                    path=[],
                    reason=reason or f"Optimal route from {req.start_location} to {req.destination} based on current stadium conditions",
                    benefit=benefit or f"Estimated {total_dist:.0f}m with minimal congestion",
                    tradeoff=tradeoff or "Standard route without accessibility adaptations",
                    confidence=confidence or result.confidence,
                    alternatives=alternatives,
                )
    except Exception as e:
        print(f"Orchestrator route failed: {e} — falling back to deterministic routing")

    det = _build_deterministic_route(req.start_location, req.destination)
    if det is not None:
        return det

    return NavigationResponse(
        route_id=f"RT-{uuid.uuid4().hex[:8].upper()}",
        steps=[
            RouteStep(
                instruction=f"Walk from {req.start_location} to {req.destination}",
                distance_m=0.0,
                duration_s=0.0,
                congestion_level="low",
            )
        ],
        total_distance_m=0.0,
        total_duration_s=0.0,
        eta=datetime.now(tz=timezone.utc),
        congestion_aware=False,
        accessibility_adapted=False,
        alternative_available=False,
    )


INTENT_CHAINS: dict[str, list[dict]] = {
    "parking": [
        {"type": "gate", "reason": "Proceed to the nearest stadium entrance gate"},
        {"type": "concourse", "reason": "Enter the main concourse area"},
        {"type": "seat", "reason": "Find your assigned seat"},
        {"type": "food", "reason": "Visit a food court during break"},
        {"type": "restroom", "reason": "Locate nearest restroom"},
        {"type": "exit", "reason": "Match is ending — time to exit"},
    ],
    "gate": [
        {"type": "concourse", "reason": "Enter the main concourse"},
        {"type": "seat", "reason": "Navigate to your seat"},
        {"type": "food", "reason": "Grab food before heading to seat"},
    ],
    "concourse": [
        {"type": "seat", "reason": "Proceed to seating area"},
        {"type": "food", "reason": "Visit a food court"},
        {"type": "restroom", "reason": "Find a restroom"},
    ],
    "seat": [
        {"type": "food", "reason": "Hungry? Visit a food court"},
        {"type": "restroom", "reason": "Find nearest restroom"},
        {"type": "merchandise", "reason": "Visit the team store"},
        {"type": "exit", "reason": "Match is ending — exit now"},
    ],
    "food": [
        {"type": "seat", "reason": "Return to your seat"},
        {"type": "restroom", "reason": "Restroom break before returning"},
    ],
    "restroom": [
        {"type": "seat", "reason": "Return to your seat"},
        {"type": "food", "reason": "Grab refreshments"},
    ],
    "exit": [],
}


class NextIntentRequest(BaseModel):
    current_location: str = Field(..., description="Current zone or node ID")
    current_location_type: str = Field(default="concourse", description="Node type")
    match_minute: int = Field(default=0, ge=0, le=120)


class NextIntentResponse(BaseModel):
    suggestions: list[dict] = Field(default_factory=list, description="Suggested next destinations with reasons")
    match_phase: str = ""
    match_minute: int = 0


@router.post("/next-intent", response_model=NextIntentResponse)
async def suggest_next_intent(req: NextIntentRequest):
    """Suggest the next logical destination based on current location and match phase.

    Uses the INTENT_CHAINS to provide context-aware transitions.
    """
    sim_state = sim_engine.get_state_dict()
    match_minute = req.match_minute or sim_state.get("match_minute", 0)
    match_phase = sim_state.get("phase", "pre-match")

    suggestions = INTENT_CHAINS.get(req.current_location_type, INTENT_CHAINS.get("concourse", []))

    if match_minute >= 85 or match_phase == "post-match":
        suggestions = [s for s in suggestions if s["type"] == "exit"]

    return NextIntentResponse(
        suggestions=suggestions[:3],
        match_phase=match_phase,
        match_minute=match_minute,
    )


class RerouteRequest(NavigationRequest):
    previous_route_id: str = ""
    reason: str = ""


@router.post("/reroute", response_model=NavigationResponse)
async def reroute_route(req: RerouteRequest):
    """Recalculate a route based on updated simulation state.

    Returns the new route plus an explanation of what changed.
    """
    print(f"Reroute: {req.start_location} -> {req.destination} (previous={req.previous_route_id})")

    det = _build_deterministic_route(req.start_location, req.destination)
    if det is not None:
        if req.previous_route_id and det.route_id != req.previous_route_id:
            old_congestion = sim_engine.get_state_dict().get("total_attendance", 0)
            det.reason = (
                f"Route updated due to changing stadium conditions. "
                f"Attendance at {old_congestion}. {det.reason}"
            )
            det.benefit = f"Recalculated with current congestion data — best available route"
            det.tradeoff = "Route may differ from previous calculation"
        return det

    return NavigationResponse(
        route_id=f"RT-{uuid.uuid4().hex[:8].upper()}",
        steps=[],
        total_distance_m=0.0,
        total_duration_s=0.0,
        eta=datetime.now(tz=timezone.utc),
        congestion_aware=False,
        accessibility_adapted=False,
        alternative_available=False,
    )


@router.get("/zones", response_model=list[StadiumZone])
async def list_zones():
    """Return all navigable stadium zones from the physical graph."""
    physical = PhysicalGraph.get()
    zones: list[StadiumZone] = []
    for node in physical.graph.nodes.values():
        zones.append(
            StadiumZone(
                zone_id=node.id,
                name=node.name,
                type=node.type.value,
                level=node.level,
                accessible=node.accessible,
            )
        )
    return zones
