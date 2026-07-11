"""StadiumOS AI — Graph Composer

Combines Physical + Operational + Semantic layers into a single weighted
navigation graph at runtime (<100ms target).

Every navigation request builds a fresh composed graph.
"""

from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from .physical import PhysicalGraph
from .operational import OperationalGraph
from .semantic import SemanticGraph


class ComposedEdge:
    def __init__(self, start_id: str, end_id: str, base_distance: float, weight: float):
        self.start_id = start_id
        self.end_id = end_id
        self.base_distance = base_distance
        self.weight = weight


class ComposedGraph:
    def __init__(self, physical: PhysicalGraph, operational: OperationalGraph, semantic: SemanticGraph):
        self._adj: dict[str, list[ComposedEdge]] = {}
        self._build(physical, operational)

    def _build(self, physical: PhysicalGraph, operational: OperationalGraph):
        for node_id in physical.graph.nodes:
            self._adj.setdefault(node_id, [])

        for edge in physical.graph.edges:
            w = edge.distance_m * operational.get_weight_multiplier(edge.start_id)
            self._adj.setdefault(edge.start_id, []).append(
                ComposedEdge(edge.start_id, edge.end_id, edge.distance_m, w)
            )
            self._adj.setdefault(edge.end_id, []).append(
                ComposedEdge(edge.end_id, edge.start_id, edge.distance_m, w)
            )

    def neighbors(self, node_id: str) -> list[ComposedEdge]:
        return self._adj.get(node_id, [])

    def all_nodes(self) -> set[str]:
        return set(self._adj.keys())


def compose_graph() -> ComposedGraph:
    physical = PhysicalGraph.get()
    operational = OperationalGraph.get()
    return ComposedGraph(physical, operational, SemanticGraph.get())
