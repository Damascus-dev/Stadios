"""StadiumOS AI — Agent Routes (Orchestrator-backed)"""

from __future__ import annotations

import sys, pathlib

from fastapi import APIRouter, HTTPException

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from schemas.agents import AgentQuery, AgentResponse
from agents.orchestrator import process_query, detect_intent
from backend.app.state import sim_engine

router = APIRouter()


@router.post("/{agent_type}", response_model=AgentResponse)
async def query_agent(agent_type: str, body: AgentQuery):
    """Send a natural-language query to one of the three AI agents."""
    print(f"Chat endpoint hit — agent_type={agent_type}, query={body.query}")
    if agent_type not in {"navigation", "operations", "accessibility"}:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown agent type '{agent_type}'. Valid types: navigation, operations, accessibility",
        )

    body.agent_type = agent_type
    sim_state = sim_engine.get_state_dict()
    response = process_query(body, sim_state)
    return response


@router.post("/detect-intent")
async def detect_intent_endpoint(query: str):
    """Classify a query to determine which agent should handle it."""
    agent_type = detect_intent(query)
    return {"agent_type": agent_type}
