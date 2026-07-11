"""StadiumOS AI — Deterministic Route Engine

Three-tier routing:
1. LLM-driven (via orchestrator) — richest, context-aware
2. Deterministic shortest-path — always works, congestion-aware
3. Direct fallback — single-step route

LLMs interpret state, never own it — the route engine is the source of truth.
"""

from __future__ import annotations

import heapq
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from schemas.navigation import NavigationRequest, NavigationResponse, RouteStep


@dataclass
class ZoneNode:
    zone_id: str
    name: str
    level: int
    accessible: bool


ZONE_CATALOG: dict[str, ZoneNode] = {
    "NS-A": ZoneNode("NS-A", "North Stand Gate A", 0, True),
    "NS-B": ZoneNode("NS-B", "North Stand Gate B", 0, True),
    "SS-A": ZoneNode("SS-A", "South Stand Gate C", 0, True),
    "ES-A": ZoneNode("ES-A", "East Stand Lower Tier", 1, True),
    "ES-B": ZoneNode("ES-B", "East Stand Upper Tier", 2, False),
    "WS-VIP": ZoneNode("WS-VIP", "VIP Lounge West", 2, True),
    "CON-N": ZoneNode("CON-N", "North Concourse", 1, True),
    "CON-S": ZoneNode("CON-S", "South Concourse", 1, True),
    "CON-W": ZoneNode("CON-W", "West Concourse", 1, True),
    "MED-1": ZoneNode("MED-1", "Medical Bay 1", 0, True),
    "FZ-W": ZoneNode("FZ-W", "Fan Zone West Plaza", 0, True),
    "FLD": ZoneNode("FLD", "Pitch / Field Level", 0, False),
    "PRESS": ZoneNode("PRESS", "Press Box", 3, True),
    "FC-N": ZoneNode("FC-N", "Food Court North", 1, True),
    "FC-S": ZoneNode("FC-S", "Food Court South", 1, True),
}


EDGES: list[tuple[str, str, int, bool]] = [
    ("NS-A", "CON-N", 50, True),
    ("NS-B", "CON-N", 40, True),
    ("CON-N", "FC-N", 60, True),
    ("CON-N", "ES-A", 80, True),
    ("ES-A", "ES-B", 40, False),
    ("ES-A", "FC-N", 90, True),
    ("SS-A", "CON-S", 50, True),
    ("CON-S", "FC-S", 60, True),
    ("CON-S", "WS-VIP", 70, True),
    ("WS-VIP", "PRESS", 80, True),
    ("CON-W", "FC-N", 100, True),
    ("CON-W", "FC-S", 90, True),
    ("CON-W", "MED-1", 50, True),
    ("MED-1", "NS-A", 60, True),
    ("MED-1", "SS-A", 70, True),
    ("FZ-W", "CON-W", 40, True),
    ("FZ-W", "MED-1", 80, True),
    ("PRESS", "ES-B", 60, True),
    ("FLD", "ES-A", 30, False),
    ("FLD", "WS-VIP", 40, False),
    ("FC-N", "ES-A", 60, True),
    ("FC-S", "WS-VIP", 50, True),
    ("CON-N", "CON-W", 120, True),
    ("CON-S", "CON-W", 100, True),
]

ADJACENCY: dict[str, list[tuple[str, int, bool]]] = {}
for a, b, dist, accessible in EDGES:
    ADJACENCY.setdefault(a, []).append((b, dist, accessible))
    ADJACENCY.setdefault(b, []).append((a, dist, accessible))


def find_shortest_path(
    start: str,
    destination: str,
    accessibility: bool = False,
    congestion_overrides: dict[str, float] | None = None,
) -> list[str]:
    if start not in ZONE_CATALOG or destination not in ZONE_CATALOG:
        return [start, destination]

    INF = float("inf")
    distances: dict[str, float] = {z: INF for z in ZONE_CATALOG}
    previous: dict[str, str | None] = {z: None for z in ZONE_CATALOG}
    distances[start] = 0
    pq = [(0, start)]

    congestion = congestion_overrides or {}

    while pq:
        current_dist, current = heapq.heappop(pq)
        if current == destination:
            break
        if current_dist > distances[current]:
            continue
        for neighbor, base_dist, edge_accessible in ADJACENCY.get(current, []):
            if accessibility and not edge_accessible:
                continue
            if accessibility and not ZONE_CATALOG[neighbor].accessible:
                continue
            zone_congestion = congestion.get(neighbor, 0.0)
            weight = base_dist * (1.0 + zone_congestion * 2.0)
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

    path: list[str] = []
    node: str | None = destination
    while node is not None:
        path.append(node)
        node = previous.get(node)
    path.reverse()

    if len(path) < 2 or path[0] != start:
        return [start, destination]

    return path


CONGESTION_LABELS = {0: "low", 1: "medium", 2: "high"}


def _congestion_level(density_pct: float) -> str:
    if density_pct >= 75:
        return "high"
    if density_pct >= 45:
        return "medium"
    return "low"


def build_deterministic_route(
    req: NavigationRequest,
    sim_state: dict | None = None,
) -> NavigationResponse:
    now = datetime.now(tz=timezone.utc)
    is_accessible = req.accessibility_preference is not None

    congestion_data: dict[str, float] = {}
    if sim_state:
        sim_zones = {z.get("zone_id", ""): z for z in sim_state.get("zones", [])}
        for zid in ZONE_CATALOG:
            s = sim_zones.get(zid)
            if s:
                congestion_data[zid] = s.get("density_pct", 0) / 100.0

    path = find_shortest_path(
        req.start_location,
        req.destination,
        accessibility=is_accessible,
        congestion_overrides=congestion_data,
    )

    steps: list[RouteStep] = []
    total_distance = 0
    total_duration = 0

    for i in range(len(path) - 1):
        cur = path[i]
        nxt = path[i + 1]
        zone_cur = ZONE_CATALOG.get(cur)
        zone_nxt = ZONE_CATALOG.get(nxt)
        dist = 0
        for a, b, d, _ in EDGES:
            if (a == cur and b == nxt) or (a == nxt and b == cur):
                dist = d
                break
        dist = dist or 50

        density_pct = 0
        if sim_state and congestion_data:
            density_pct = congestion_data.get(nxt, 0) * 100

        walking_speed = 0.8 if is_accessible else 1.2
        duration_s = int(dist / walking_speed) + (30 if zone_cur and zone_nxt and zone_cur.level != zone_nxt.level else 0)

        zone_from = zone_cur.name if zone_cur else cur
        zone_to = zone_nxt.name if zone_nxt else nxt
        level_change = ""
        if zone_cur and zone_nxt and zone_cur.level != zone_nxt.level:
            if is_accessible:
                level_change = f" Take elevator to Level {zone_nxt.level}."
            else:
                level_change = f" Take stairs/escalator to Level {zone_nxt.level}."

        steps.append(RouteStep(
            instruction=f"Proceed from {zone_from} to {zone_to}.{level_change}",
            distance_m=float(dist),
            duration_s=float(duration_s),
            congestion_level=_congestion_level(density_pct),
        ))

        total_distance += dist
        total_duration += duration_s

    return NavigationResponse(
        route_id=f"RT-{uuid.uuid4().hex[:8].upper()}",
        steps=steps,
        total_distance_m=float(total_distance),
        total_duration_s=float(total_duration),
        eta=now + timedelta(seconds=total_duration),
        congestion_aware=True,
        accessibility_adapted=is_accessible,
        alternative_available=True,
    )
