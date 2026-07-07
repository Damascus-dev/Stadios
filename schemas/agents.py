"""StadiumOS AI — Agent Schema Models"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class AgentQuery(BaseModel):
    query: str = Field(..., description="Natural language question for the agent")
    agent_type: str = Field(
        ..., description="navigation | operations | accessibility"
    )
    context: dict[str, Any] | None = Field(
        None, description="Optional context from the UI (current zone, user prefs, etc.)"
    )
    language: str = Field("en", description="ISO 639-1 language code")


class AgentResponse(BaseModel):
    agent_type: str
    response_text: str
    structured_data: dict[str, Any] | None = None
    recommendations: list[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0, le=1)
    cached: bool = False
