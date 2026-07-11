"""StadiumOS AI — Operational Graph Service

Reads live simulation state and produces congestion/delay weights.
This layer updates continuously as the simulation advances.
"""

from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from backend.app.state import sim_engine


class OperationalGraph:
    _instance: OperationalGraph | None = None

    @classmethod
    def get(cls) -> OperationalGraph:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _get_state(self) -> dict:
        return sim_engine.get_state_dict()

    def get_overall_congestion(self) -> float:
        state = self._get_state()
        total_attendance = state.get("total_attendance", 0) or 0
        capacity = state.get("stadium_capacity", 82500) or 82500
        return total_attendance / capacity

    def get_weight_multiplier(self, node_id: str) -> float:
        congestion = self.get_overall_congestion()
        return 1.0 + congestion * 2.0

    def is_closed(self, node_id: str) -> bool:
        state = self._get_state()
        for alert in state.get("incidents", []):
            if isinstance(alert, dict):
                zone = alert.get("zone", "")
                if zone and zone.lower() in node_id.lower():
                    return True
        return False
