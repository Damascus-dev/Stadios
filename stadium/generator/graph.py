"""StadiumOS AI — Navigation Graph Builder

Builds a NavigationGraph from generated geometry:
- Every facility connects to its level's concourse hub
- Concourse hubs connect vertically (elevators/escalators)
- Facilities within the same level connect to nearby facilities
- All edges are bidirectional
"""

from __future__ import annotations

import math

from ..metadata.schemas import NavigationGraph, NavigationNode, NavigationEdge, NodeType, Position


def _dist(a: tuple, b: tuple) -> float:
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)


def _add_edge(edges: list[NavigationEdge], a_id: str, b_id: str, d: float, speed: float, accessible: bool):
    edges.append(NavigationEdge(
        start_id=a_id, end_id=b_id,
        distance_m=d, travel_time_s=d / speed,
        accessible=accessible,
    ))


def build_navigation_graph(
    nodes: dict[str, dict],
    edges: list,
    stadium_cfg: dict,
) -> NavigationGraph:
    graph_nodes: dict[str, NavigationNode] = {}
    graph_edges: list[NavigationEdge] = []

    for nid, nd in nodes.items():
        p = nd["position"]
        try:
            ntype = NodeType(nd["type"])
        except ValueError:
            ntype = NodeType.CONCOURSE
        graph_nodes[nid] = NavigationNode(
            id=nid,
            type=ntype,
            name=nd["name"],
            position=Position(x=p[0], y=p[1], z=p[2]),
            level=nd["level"],
            quadrant=nd.get("quadrant", ""),
            accessible=nd.get("accessible", True),
        )

    node_list = list(graph_nodes.values())
    by_level: dict[int, list[NavigationNode]] = {}
    for n in node_list:
        by_level.setdefault(n.level, []).append(n)

    # Connect each facility to its level's concourse hub
    for level, lvl_nodes in by_level.items():
        concourse = [n for n in lvl_nodes if n.type == NodeType.CONCOURSE]
        if not concourse:
            continue
        hub = concourse[0]
        for n in lvl_nodes:
            if n.id == hub.id:
                continue
            d = _dist((n.position.x, n.position.y, n.position.z),
                      (hub.position.x, hub.position.y, hub.position.z))
            _add_edge(graph_edges, n.id, hub.id, d, 1.4, n.accessible and hub.accessible)

    # Connect facilities to nearby same-level facilities
    for level, lvl_nodes in by_level.items():
        facilities = [n for n in lvl_nodes if n.type != NodeType.CONCOURSE]
        for i in range(len(facilities)):
            for j in range(i + 1, len(facilities)):
                a, b = facilities[i], facilities[j]
                d = _dist((a.position.x, a.position.y, a.position.z),
                          (b.position.x, b.position.y, b.position.z))
                if d < 20:
                    _add_edge(graph_edges, a.id, b.id, d, 1.4, a.accessible and b.accessible)

    # Vertical connections between concourse hubs
    sorted_levels = sorted(by_level.keys())
    for i in range(len(sorted_levels) - 1):
        lvl_a = sorted_levels[i]
        lvl_b = sorted_levels[i + 1]
        hubs_a = [n for n in by_level[lvl_a] if n.type == NodeType.CONCOURSE]
        hubs_b = [n for n in by_level[lvl_b] if n.type == NodeType.CONCOURSE]
        if hubs_a and hubs_b:
            ha, hb = hubs_a[0], hubs_b[0]
            d = abs(ha.position.y - hb.position.y)
            _add_edge(graph_edges, ha.id, hb.id, d, 0.8, True)

    return NavigationGraph(nodes=graph_nodes, edges=graph_edges)
