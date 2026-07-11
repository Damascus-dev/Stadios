"""StadiumOS AI — Physical Graph Service

Immutable graph loaded from the procedural generator output.
Defines the stadium's static infrastructure: nodes, edges, distances, accessibility.
This graph NEVER changes during runtime.
"""

from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from stadium.generator import generate_stadium
from stadium.metadata.schemas import NavigationNode, NavigationEdge, NavigationGraph, NodeType


class PhysicalGraph:
    _instance: PhysicalGraph | None = None

    def __init__(self):
        data = generate_stadium()
        self._graph: NavigationGraph = data.graph
        self._by_level: dict[int, list[NavigationNode]] = {}
        self._by_type: dict[str, list[NavigationNode]] = {}
        self._by_quadrant: dict[str, list[NavigationNode]] = {}

        for n in self._graph.nodes.values():
            self._by_level.setdefault(n.level, []).append(n)
            self._by_type.setdefault(n.type.value, []).append(n)
            self._by_quadrant.setdefault(n.quadrant, []).append(n)

    @classmethod
    def get(cls) -> PhysicalGraph:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def graph(self) -> NavigationGraph:
        return self._graph

    def get_node(self, node_id: str) -> NavigationNode | None:
        return self._graph.nodes.get(node_id)

    def get_nodes_by_type(self, ntype: str) -> list[NavigationNode]:
        return self._by_type.get(ntype, [])

    def get_nodes_by_level(self, level: int) -> list[NavigationNode]:
        return self._by_level.get(level, [])

    def get_nodes_by_quadrant(self, quadrant: str) -> list[NavigationNode]:
        return self._by_quadrant.get(quadrant, [])

    def get_edges_from(self, node_id: str) -> list[NavigationEdge]:
        return [e for e in self._graph.edges if e.start_id == node_id]

    def get_edges_to(self, node_id: str) -> list[NavigationEdge]:
        return [e for e in self._graph.edges if e.end_id == node_id]

    def get_all_edges_for(self, node_id: str) -> list[NavigationEdge]:
        return self.get_edges_from(node_id) + self.get_edges_to(node_id)
