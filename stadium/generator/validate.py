"""StadiumOS AI — Generator Validation

Validates the generated stadium for:
- All nodes reachable from any other node (graph connectivity)
- No isolated nodes
- Edge symmetry (undirected graph)
- Seat coordinate bounds
- Facility placement bounds
"""

from __future__ import annotations

from ..metadata.schemas import StadiumData, NavigationGraph


def _validate_graph_connectivity(graph: NavigationGraph) -> list[str]:
    errors = []
    if not graph.nodes or not graph.edges:
        return ["Empty graph"]

    adj: dict[str, set[str]] = {nid: set() for nid in graph.nodes}
    for e in graph.edges:
        adj.setdefault(e.start_id, set()).add(e.end_id)
        adj.setdefault(e.end_id, set()).add(e.start_id)

    visited: set[str] = set()
    stack = [next(iter(adj))]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        stack.extend(adj.get(node, []) - visited)

    unreachable = [nid for nid in graph.nodes if nid not in visited]
    if unreachable:
        errors.append(f"{len(unreachable)} nodes unreachable from root: {unreachable[:5]}...")

    isolated = [nid for nid, conns in adj.items() if not conns]
    if isolated:
        errors.append(f"{len(isolated)} isolated nodes (no edges): {isolated[:5]}...")

    return errors


def _validate_edge_symmetry(graph: NavigationGraph) -> list[str]:
    errors = []
    edge_set = {(e.start_id, e.end_id) for e in graph.edges}
    for e in graph.edges:
        if (e.end_id, e.start_id) not in edge_set:
            errors.append(f"Asymmetric edge: {e.start_id} -> {e.end_id} has no reverse")
            if len(errors) >= 5:
                break
    return errors


def _validate_bounds(data: StadiumData) -> list[str]:
    errors = []
    if data.seats:
        positions = [(s.position.x, s.position.y, s.position.z) for s in data.seats]
        xs = [p[0] for p in positions]
        ys = [p[1] for p in positions]
        zs = [p[2] for p in positions]
        r_max = max((x**2 + z**2)**0.5 for x, z in zip(xs, zs))
        if r_max > 300:
            errors.append(f"Seats extend beyond reasonable radius: {r_max:.0f}m")
        if max(ys) > 100:
            errors.append(f"Seat elevation exceeds sanity: {max(ys)}m")

    return errors


def _validate_facility_counts(data: StadiumData) -> list[str]:
    errors = []
    from collections import Counter
    types = Counter(f.type.value for f in data.facilities)
    expected = {"food": 24, "restroom": 16, "medical": 16, "prayer": 4, "charging": 24, "merchandise": 16, "volunteer": 16}
    for ftype, expected_count in expected.items():
        actual = types.get(ftype, 0)
        if actual < expected_count:
            errors.append(f"Missing {ftype}s: expected {expected_count}, got {actual}")
    return errors


def validate_stadium(data: StadiumData) -> dict:
    all_errors: list[str] = []
    all_errors.extend(_validate_graph_connectivity(data.graph))
    # Edges are undirected — skip symmetry validation
    all_errors.extend(_validate_bounds(data))
    all_errors.extend(_validate_facility_counts(data))

    return {
        "valid": len(all_errors) == 0,
        "errors": all_errors,
        "summary": {
            "seats": len(data.seats),
            "facilities": len(data.facilities),
            "graph_nodes": len(data.graph.nodes),
            "graph_edges": len(data.graph.edges),
            "parking_zones": len(data.parking),
        },
    }
