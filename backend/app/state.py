"""StadiumOS AI — Shared Application State

Single SimulationEngine instance shared across all route handlers.
"""

from __future__ import annotations

import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from simulation.engine import SimulationEngine

sim_engine = SimulationEngine()
