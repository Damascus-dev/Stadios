"""StadiumOS AI — AI Orchestrator

Core pipeline: intent detection -> prompt construction -> LLM call -> schema validation -> formatted response.
Provider-agnostic — routes all inference through the provider abstraction layer.
"""

import logging
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from agents.cache import find_cache_entry as find_cached_response
from agents.intent_classifier import classify as classify_intent
from agents.providers import get_provider
from schemas.agents import AgentQuery, AgentResponse

PROMPTS_DIR = pathlib.Path(__file__).resolve().parent.parent / "prompts"

PROMPT_FILES: dict[str, str] = {
    "navigation": "navigation_explain_v1.md",
    "operations": "operations_v1.md",
    "accessibility": "accessibility_v1.md",
    "formatter": "formatter_v1.md",
}

AGENT_SYSTEM_PROMPTS: dict[str, str] = {}


def _load_prompts():
    for agent_type, filename in PROMPT_FILES.items():
        filepath = PROMPTS_DIR / filename
        if filepath.exists():
            AGENT_SYSTEM_PROMPTS[agent_type] = filepath.read_text(encoding="utf-8")
        else:
            logging.warning("Prompt file not found: %s", filepath)


_load_prompts()


def build_context(sim_state: dict | None) -> str:
    if sim_state is None:
        return "No simulation data available."

    zones = sim_state.get("zones", [])
    incidents = sim_state.get("incidents", [])
    active_incidents = [i for i in incidents if i.get("active")]

    context_parts = [
        f"Stadium: MetLife Stadium, Capacity: {sim_state.get('stadium_capacity', 'N/A')}",
        f"Match Phase: {sim_state.get('phase', 'N/A')}, Minute: {sim_state.get('match_minute', 'N/A')}",
        f"Total Attendance: {sim_state.get('total_attendance', 'N/A')}",
        f"Stadium Health Score: {sim_state.get('stadium_health_score', 'N/A')}",
        "",
        "Zone Density Report:",
    ]

    for zone in zones:
        context_parts.append(
            f"  - {zone.get('name', zone.get('zone_id', 'Unknown'))}: "
            f"{zone.get('density_pct', 0)}% density, "
            f"risk: {zone.get('risk_level', 'unknown')}, "
            f"trend: {zone.get('trend', 'stable')}"
        )

    if active_incidents:
        context_parts.append("")
        context_parts.append("Active Incidents:")
        for inc in active_incidents:
            context_parts.append(
                f"  - [{inc.get('severity', 'info')}] {inc.get('description', 'No description')}"
            )

    context_parts.append("")
    context_parts.append(f"Transportation — Shuttle Load: {sim_state.get('shuttle_load_pct', 0)}%, "
                         f"Parking: {sim_state.get('parking_capacity_pct', 0)}%")
    context_parts.append(f"Sustainability — Energy: {sim_state.get('energy_load_kwh', 0)} kWh, "
                         f"Waste: {sim_state.get('waste_generation_kg', 0)} kg, "
                         f"Water: {sim_state.get('water_usage_liters', 0)} L")

    return "\n".join(context_parts)


def _build_response_schema(agent_type: str) -> dict:
    base = {
        "type": "object",
        "properties": {
            "response_text": {"type": "string"},
            "structured_data": {"type": "object"},
            "recommendations": {
                "type": "array",
                "items": {"type": "string"},
            },
            "confidence": {"type": "number"},
        },
        "required": ["response_text", "confidence"],
    }

    if agent_type == "navigation":
        base["properties"]["structured_data"] = {
            "type": "object",
            "properties": {
                "recommended_route_id": {"type": "string"},
                "estimated_time_s": {"type": "number"},
                "congestion_avoided": {"type": "array", "items": {"type": "string"}},
                "accessibility_options": {"type": "array", "items": {"type": "string"}},
                "reason": {"type": "string"},
                "benefit": {"type": "string"},
                "tradeoff": {"type": "string"},
                "confidence": {"type": "number"},
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "instruction": {"type": "string"},
                            "distance_m": {"type": "number"},
                            "duration_s": {"type": "number"},
                            "congestion_level": {"type": "string"},
                        },
                        "required": ["instruction", "distance_m", "duration_s", "congestion_level"],
                    },
                },
                "alternatives": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "reason": {"type": "string"},
                            "tradeoff": {"type": "string"},
                            "total_distance_m": {"type": "number"},
                            "total_duration_s": {"type": "number"},
                            "confidence": {"type": "number"},
                        },
                    },
                },
            },
        }
    elif agent_type == "operations":
        base["properties"]["structured_data"] = {
            "type": "object",
            "properties": {
                "predictions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "zone": {"type": "string"},
                            "risk_level": {"type": "string"},
                            "confidence": {"type": "number"},
                        },
                    },
                },
                "volunteer_recommendations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "zone": {"type": "string"},
                            "count": {"type": "integer"},
                            "reason": {"type": "string"},
                        },
                    },
                },
                "transportation_signal": {
                    "type": "object",
                    "properties": {
                        "shuttle_load_pct": {"type": "number"},
                        "parking_capacity_pct": {"type": "number"},
                        "exit_congestion": {"type": "string"},
                        "prediction_text": {"type": "string"},
                    },
                },
                "sustainability_signal": {
                    "type": "object",
                    "properties": {
                        "energy_load_kwh": {"type": "number"},
                        "waste_generation_kg": {"type": "number"},
                        "water_usage_liters": {"type": "number"},
                        "crowd_correlation_factor": {"type": "number"},
                        "trend": {"type": "string"},
                    },
                },
            },
        }
    elif agent_type == "accessibility":
        base["properties"]["structured_data"] = {
            "type": "object",
            "properties": {
                "accessibility_type": {"type": "string"},
                "adapted_instructions": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "language": {"type": "string"},
                "emergency_mode": {"type": "boolean"},
                "alternative_formats": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "boolean"},
                        "audio_description": {"type": "boolean"},
                    },
                },
            },
        }

    return base


def process_query(
    query: AgentQuery,
    sim_state: dict | None = None,
) -> AgentResponse:
    agent_type = query.agent_type

    cached = find_cached_response(query.query)
    if cached is not None:
        return cached

    provider = get_provider()
    if not provider.available():
        return _fallback_response(agent_type, "LLM provider not configured — set DEEPSEEK_API_KEY or GEMINI_API_KEY")

    context = build_context(sim_state)
    prompt_key = agent_type if agent_type in AGENT_SYSTEM_PROMPTS else "navigation"
    system_prompt = AGENT_SYSTEM_PROMPTS.get(prompt_key, "")

    user_message = (
        f"Current Stadium State:\n{context}\n\n"
        f"User Query: {query.query}\n"
        f"Language: {query.language}\n"
        f"User Context: {query.context if query.context else 'None provided'}"
    )

    response_schema = _build_response_schema(agent_type)
    print(f"Calling LLM provider: {provider.model_name()}")
    ai_response = provider.generate(system_prompt, user_message, response_schema)

    if ai_response is None:
        fallback = _fallback_response(agent_type, "LLM call failed")
        cached_response = find_cached_response(query.query)
        if cached_response is not None:
            return cached_response
        return fallback

    return AgentResponse(
        agent_type=agent_type,
        response_text=ai_response.get("response_text", ""),
        structured_data=ai_response.get("structured_data"),
        recommendations=ai_response.get("recommendations", []),
        confidence=ai_response.get("confidence", 0.0),
        cached=False,
    )


def _fallback_response(agent_type: str, reason: str) -> AgentResponse:
    fallbacks: dict[str, AgentResponse] = {
        "navigation": AgentResponse(
            agent_type="navigation",
            response_text="Navigation service is currently unavailable. Please try again or use the static stadium map.",
            recommendations=["Use the stadium map at information kiosks", "Ask a volunteer for directions"],
            confidence=0.0,
            cached=True,
        ),
        "operations": AgentResponse(
            agent_type="operations",
            response_text="Operations monitoring is temporarily unavailable. Displaying last known stadium state.",
            recommendations=["Check back in a few minutes", "Contact the operations desk for urgent issues"],
            confidence=0.0,
            cached=True,
        ),
        "accessibility": AgentResponse(
            agent_type="accessibility",
            response_text="Accessibility services are temporarily unavailable. Please visit Guest Services for assistance.",
            recommendations=["Visit Guest Services at Gate A or Gate D", "Use the stadium PA system for announcements"],
            confidence=0.0,
            cached=True,
        ),
    }
    response = fallbacks.get(agent_type, list(fallbacks.values())[0])
    response.structured_data = {"fallback_reason": reason}
    return response


def detect_intent(query: str) -> str:
    provider = get_provider()
    if not provider.available():
        return "operations"
    result = classify_intent(provider, query)
    return result.agent_type
