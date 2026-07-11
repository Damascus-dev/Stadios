"""StadiumOS AI — Semantic Graph Service

Facility index for type-based queries.
Answers "what is this place?" instead of "where is it?"
"""

from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from stadium.metadata.schemas import FacilityType

from .physical import PhysicalGraph


class SemanticGraph:
    _instance: SemanticGraph | None = None

    def __init__(self):
        self._physical = PhysicalGraph.get()

    @classmethod
    def get(cls) -> SemanticGraph:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def find_nearest(self, facility_type: str, from_node_id: str) -> str | None:
        nodes = self._physical.get_nodes_by_type(facility_type)
        if not nodes:
            return None
        from_node = self._physical.get_node(from_node_id)
        if not from_node:
            return nodes[0].id

        best = None
        best_dist = float("inf")
        for n in nodes:
            d = self._node_distance(from_node, n)
            if d < best_dist:
                best_dist = d
                best = n.id
        return best

    def find_all(self, facility_type: str) -> list[dict]:
        nodes = self._physical.get_nodes_by_type(facility_type)
        return [
            {
                "id": n.id,
                "type": n.type.value,
                "name": n.name,
                "level": n.level,
                "quadrant": n.quadrant,
            }
            for n in nodes
        ]

    def _node_distance(self, a, b) -> float:
        dx = a.position.x - b.position.x
        dy = a.position.y - b.position.y
        dz = a.position.z - b.position.z
        return (dx*dx + dy*dy + dz*dz) ** 0.5
