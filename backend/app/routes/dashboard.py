"""StadiumOS AI — Dashboard Route

Three-tier pipeline:
1. Operations Agent via orchestrator (LLM-generated insights)
2. Deterministic operations engine (simulation-backed, always works)
3. Minimal fallback (empty state)

LLMs interpret state, never own it — OperationsEngine is the source of truth.
"""

from __future__ import annotations

import sys
import pathlib

from fastapi import APIRouter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from schemas.dashboard import DashboardResponse
from backend.app.state import sim_engine
from backend.app.operations import build_dashboard

router = APIRouter()


@router.get("/", response_model=DashboardResponse)
async def get_dashboard():
    """Return a full dashboard snapshot from simulation state.

    Tiers:
      1. LLM-driven via Operations Agent (not yet wired — future)
      2. Deterministic operations engine (always returns valid data)
    """
    sim_state = sim_engine.get_state_dict()
    return build_dashboard(sim_state)
