"""StadiumOS AI — Extended Dijkstra Navigator

Route finding on the composed multi-layer graph.
Supports congestion-aware routing.
"""

from __future__ import annotations

import heapq
import uuid

from .composer import compose_graph


class RouteResult:
    def __init__(
        self,
        route_id: str,
        path: list[str],
        total_distance: float,
        total_duration: float,
    ):
        self.route_id = route_id
        self.path = path
        self.total_distance = total_distance
        self.total_duration = total_duration


def _dijkstra(
    start_id: str,
    end_id: str,
    graph,
    avoid_nodes: set[str] | None = None,
) -> tuple[dict[str, float], dict[str, str | None]] | None:
    avoid = avoid_nodes or set()
    if start_id in avoid or end_id in avoid:
        return None

    distances: dict[str, float] = {start_id: 0}
    previous: dict[str, str | None] = {start_id: None}
    pq: list[tuple[float, str]] = [(0, start_id)]

    while pq:
        current_dist, current = heapq.heappop(pq)
        if current == end_id:
            break
        if current_dist > distances.get(current, float("inf")):
            continue

        for edge in graph.neighbors(current):
            neighbor = edge.end_id if edge.start_id == current else edge.start_id
            if neighbor in avoid:
                continue
            new_dist = current_dist + edge.weight
            if new_dist < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

    if end_id not in previous:
        return None
    return distances, previous


def _reconstruct_path(
    previous: dict[str, str | None],
    end_id: str,
) -> list[str]:
    path: list[str] = []
    node = end_id
    while node is not None:
        path.append(node)
        node = previous.get(node)
    path.reverse()
    return path


def _compute_total_distance(graph, path: list[str]) -> float:
    total = 0.0
    for i in range(len(path) - 1):
        for edge in graph.neighbors(path[i]):
            if edge.end_id == path[i + 1]:
                total += edge.base_distance
                break
    return total


def find_route(start_id: str, end_id: str) -> RouteResult | None:
    graph = compose_graph()
    if start_id not in graph.all_nodes():
        return None
    if end_id not in graph.all_nodes():
        return None

    result = _dijkstra(start_id, end_id, graph)
    if result is None:
        return None

    distances, previous = result
    path = _reconstruct_path(previous, end_id)
    total_dist = _compute_total_distance(graph, path)

    return RouteResult(
        route_id=f"route-{uuid.uuid4().hex[:8]}",
        path=path,
        total_distance=total_dist,
        total_duration=distances.get(end_id, total_dist / 1.4),
    )


def find_alternatives(start_id: str, end_id: str, max_alts: int = 2) -> list[RouteResult]:
    graph = compose_graph()
    if start_id not in graph.all_nodes() or end_id not in graph.all_nodes():
        return []

    primary = _dijkstra(start_id, end_id, graph)
    if primary is None:
        return []
    _, primary_prev = primary
    primary_path = _reconstruct_path(primary_prev, end_id)
    if len(primary_path) < 4:
        return []

    alternatives: list[RouteResult] = []
    seen_paths: set[str] = set()

    for i in range(1, len(primary_path) - 1, max(1, (len(primary_path) - 2) // (max_alts + 1))):
        avoid = {primary_path[i]}
        result = _dijkstra(start_id, end_id, graph, avoid_nodes=avoid)
        if result is None:
            continue
        distances, previous = result
        alt_path = _reconstruct_path(previous, end_id)
        path_key = ",".join(alt_path)
        if path_key in seen_paths:
            continue
        seen_paths.add(path_key)
        total_dist = _compute_total_distance(graph, alt_path)
        alternatives.append(RouteResult(
            route_id=f"route-{uuid.uuid4().hex[:8]}",
            path=alt_path,
            total_distance=total_dist,
            total_duration=distances.get(end_id, total_dist / 1.4),
        ))
        if len(alternatives) >= max_alts:
            break

    return alternatives
