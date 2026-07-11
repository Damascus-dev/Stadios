"""StadiumOS AI — Deterministic Operations Engine

Three-tier operations pipeline:
1. LLM-driven (via orchestrator) — richest, context-aware predictions
2. Deterministic analysis — always works, simulation-backed
3. Direct fallback — minimal valid response

LLMs interpret state, never own it — this engine is the source of truth.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

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


def _zone_trend(prev_density: float, curr_density: float) -> str:
    if curr_density > prev_density + 2:
        return "rising"
    if curr_density < prev_density - 2:
        return "falling"
    return "stable"


def _health_status(score: float) -> str:
    if score >= 85:
        return "green"
    if score >= 65:
        return "yellow"
    return "red"


def _density_risk(density_pct: float) -> str:
    if density_pct >= 90:
        return "critical"
    if density_pct >= 75:
        return "high"
    if density_pct >= 50:
        return "medium"
    return "low"


def _severity_from_risk(risk: str) -> str:
    return {"critical": "critical", "high": "high", "medium": "medium", "low": "low"}.get(risk, "low")


def build_dashboard(sim_state: dict[str, Any] | None) -> DashboardResponse:
    now = datetime.now(tz=timezone.utc)
    zones: list[dict] = (sim_state or {}).get("zones", [])
    incidents: list[dict] = (sim_state or {}).get("incidents", [])

    total_attendance = (sim_state or {}).get("total_attendance", 0)
    stadium_capacity = (sim_state or {}).get("stadium_capacity", 82500)
    health_score = (sim_state or {}).get("stadium_health_score", 85.0)
    match_minute = (sim_state or {}).get("match_minute", 0)

    # 1. Stadium Health
    capacity_pct = round(total_attendance / stadium_capacity * 100, 1) if stadium_capacity else 0
    stadium_health = StadiumHealth(
        overall_score=health_score,
        status=_health_status(health_score),
        capacity_pct=capacity_pct,
        active_zones=len([z for z in zones if z.get("density_pct", 0) > 0]),
    )

    # 2. Crowd Heat — map all sim zones
    crowd_zones: list[CrowdZone] = []
    for z in zones:
        crowd_zones.append(CrowdZone(
            zone_id=z.get("zone_id", ""),
            name=z.get("name", ""),
            density_pct=z.get("density_pct", 0),
            trend=z.get("trend", "stable"),
            risk_level=z.get("risk_level", "low"),
        ))
    crowd_heat = CrowdHeat(zones=crowd_zones)

    # 3. Volunteer Status — generated from zone risk levels
    volunteer_assignments: list[VolunteerAssignment] = []
    total_vols = 420
    deployed = 0
    for z in zones:
        risk = z.get("risk_level", "low")
        zone_id = z.get("zone_id", "")
        zone_name = z.get("name", "")
        base_count = {"critical": 55, "high": 42, "medium": 30, "low": 15}.get(risk, 20)
        density = z.get("density_pct", 0)
        extra = int(density / 100 * 10) if risk in ("critical", "high") else 0
        count = base_count + extra
        role = "crowd-management" if risk in ("critical", "high") else "wayfinding"
        if zone_id in ("medical_station",):
            role = "first-aid"
        elif zone_id in ("vip_lounge",):
            role = "hospitality"
        volunteer_assignments.append(VolunteerAssignment(
            zone_id=zone_id,
            zone_name=zone_name,
            count=count,
            role=role,
        ))
        deployed += count
    volunteer_status = VolunteerStatus(
        total=total_vols,
        deployed=min(deployed, total_vols),
        available=max(0, total_vols - deployed),
        zones=volunteer_assignments,
    )

    # 4. Incident Count
    active_incidents = [i for i in incidents if i.get("active")]
    resolved_incidents = [i for i in incidents if not i.get("active")]
    sev = SeverityBreakdown()
    for inc in active_incidents:
        s = inc.get("severity", "low")
        if s == "critical":
            sev.critical += 1
        elif s == "high":
            sev.high += 1
        elif s == "medium":
            sev.medium += 1
        else:
            sev.low += 1
    incident_count = IncidentCount(
        active=len(active_incidents),
        resolved=len(resolved_incidents),
        total=len(incidents),
        by_severity=sev,
    )

    # 5. Active Alerts — from active incidents
    alert_list: list[AlertSummary] = []
    for inc in active_incidents:
        alert_list.append(AlertSummary(
            id=inc.get("incident_id", f"ALT-{uuid.uuid4().hex[:6].upper()}"),
            type=inc.get("type", "crowd"),
            severity=inc.get("severity", "medium"),
            message=inc.get("description", ""),
            zone=inc.get("zone_id", ""),
            timestamp=datetime.fromtimestamp(inc.get("timestamp", now.timestamp()), tz=timezone.utc),
        ))
    # Add predictive alerts for high/critical zones without incidents
    alert_ids = {a.zone for a in alert_list}
    for z in zones:
        if z.get("zone_id") in alert_ids:
            continue
        risk = z.get("risk_level", "low")
        if risk in ("critical", "high"):
            alert_list.append(AlertSummary(
                id=f"PRD-{uuid.uuid4().hex[:6].upper()}",
                type="crowd",
                severity=_severity_from_risk(risk),
                message=f"{z.get('name', 'Zone')} at {z.get('density_pct', 0)}% density — {risk} risk level",
                zone=z.get("zone_id", ""),
                timestamp=now,
            ))
    active_alerts = ActiveAlerts(alerts=alert_list)

    # 6. AI Recommendations
    recommendations: list[AIRecommendation] = []
    for z in zones:
        risk = z.get("risk_level", "low")
        zone_name = z.get("name", "")
        zone_id = z.get("zone_id", "")
        density = z.get("density_pct", 0)
        if risk == "critical":
            recommendations.append(AIRecommendation(
                id=f"REC-{uuid.uuid4().hex[:6].upper()}",
                type="crowd-flow",
                priority="critical",
                title=f"Immediate intervention needed at {zone_name}",
                description=f"{zone_name} at {density}% — critical density. Redirect incoming flow and deploy additional crowd management. Activate auxiliary routes.",
                agent_source="operations",
                confidence=0.92,
            ))
        elif risk == "high":
            recommendations.append(AIRecommendation(
                id=f"REC-{uuid.uuid4().hex[:6].upper()}",
                type="crowd-flow",
                priority="high",
                title=f"Monitor {zone_name} closely",
                description=f"{zone_name} at {density}% — high density. Pre-position volunteer team and prepare rerouting contingency.",
                agent_source="operations",
                confidence=0.85,
            ))
    # Add transportation recommendation if shuttle/parking high
    shuttle = (sim_state or {}).get("shuttle_load_pct", 0)
    parking = (sim_state or {}).get("parking_capacity_pct", 0)
    if shuttle > 85 or parking > 85:
        recommendations.append(AIRecommendation(
            id=f"REC-{uuid.uuid4().hex[:6].upper()}",
            type="transportation",
            priority="high" if max(shuttle, parking) > 90 else "medium",
            title="Transportation bottleneck developing",
            description=f"Shuttle load at {shuttle}%, parking at {parking}%. Pre-stage additional shuttles and activate overflow lots.",
            agent_source="operations",
            confidence=0.88,
        ))
    # Sustainability recommendation
    energy = (sim_state or {}).get("energy_load_kwh", 0)
    if energy > 4000:
        recommendations.append(AIRecommendation(
            id=f"REC-{uuid.uuid4().hex[:6].upper()}",
            type="sustainability",
            priority="medium",
            title="Reduce non-essential energy consumption",
            description=f"Energy load at {energy} kWh. Dim non-essential lighting in low-density zones to reduce load by ~15%.",
            agent_source="operations",
            confidence=0.82,
        ))

    # 7. Transportation Status
    exit_zones = [z for z in zones if "gate" in z.get("zone_id", "").lower()]
    exit_congestion_list: list[ExitCongestion] = [
        ExitCongestion(
            exit_id=z.get("zone_id", ""),
            name=z.get("name", ""),
            congestion_pct=z.get("density_pct", 0),
        )
        for z in exit_zones
    ] if exit_zones else [
        ExitCongestion(exit_id="EXIT-N1", name="North Exit — Metro Link", congestion_pct=min(shuttle + 10, 100)),
        ExitCongestion(exit_id="EXIT-S1", name="South Exit — Bus Terminal", congestion_pct=min(parking + 5, 100)),
        ExitCongestion(exit_id="EXIT-E1", name="East Exit — Parking Lot A", congestion_pct=min(shuttle, 100)),
        ExitCongestion(exit_id="EXIT-W1", name="West Exit — Ride-Share Zone", congestion_pct=min(parking, 100)),
    ]
    transportation = TransportationStatus(
        shuttle_load_pct=shuttle,
        parking_capacity_pct=parking,
        exit_congestion=exit_congestion_list,
        prediction=(
            "Post-match surge expected within 30 min. Recommend pre-staging additional shuttle buses."
            if match_minute > 80
            else "Transportation flow stable. Monitoring exit gates for post-match surge."
        ),
    )

    # 8. Sustainability Metrics
    sustainability = SustainabilityMetrics(
        energy_load_kwh=(sim_state or {}).get("energy_load_kwh", 0),
        waste_generation_kg=(sim_state or {}).get("waste_generation_kg", 0),
        water_usage_liters=(sim_state or {}).get("water_usage_liters", 0),
        crowd_correlation_factor=0.78,
    )

    return DashboardResponse(
        stadium_health=stadium_health,
        crowd_heat=crowd_heat,
        volunteer_status=volunteer_status,
        incident_count=incident_count,
        active_alerts=active_alerts,
        ai_recommendations=recommendations,
        transportation=transportation,
        sustainability=sustainability,
        generated_at=now,
    )
