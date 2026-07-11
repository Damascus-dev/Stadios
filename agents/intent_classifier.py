"""StadiumOS AI — Intent Classifier

Classifies user queries into agent types using the configured LLM provider.
"""

from agents.cache import find_cache_entry

INTENT_SYSTEM_PROMPT = """## Purpose
Classify user intent to route queries to the correct specialized agent (Navigation, Operations, or Accessibility).

## Input Schema
- query: string (the user's natural language input)

## Instructions
You are the intent classifier for StadiumOS AI. Given a user query, determine which specialized agent should handle it.

Classification rules:
- **navigation**: Questions about directions, routes, finding locations, getting to seats/gates/facilities, ETAs, "how do I get to...", "where is..."
- **operations**: Questions about crowd conditions, incidents, volunteer deployment, stadium status, predictions, recommendations, transportation (shuttles, parking), sustainability (energy, waste), "what's happening at...", "is it crowded..."
- **accessibility**: Questions about wheelchair access, accessible routes, language translation, hearing/vision assistance, emergency evacuation for people with disabilities, "I need help in [language]", "wheelchair route to..."

If a query could match multiple agents, use this priority:
1. accessibility (if any accessibility need is mentioned)
2. navigation (if asking for directions/routes)
3. operations (default for monitoring/status queries)

If a query is completely unrelated to stadium operations, return "out_of_scope".

## Output Schema
Return exactly:
{
  "agent_type": "navigation" | "operations" | "accessibility" | "out_of_scope",
  "confidence": 0.0-1.0,
  "reasoning": "one-sentence explanation"
}

## Constraints
- Never invent state not present in input context
- Always return via structured output, never free text
- One query to one agent (no multi-intent in this version)
- out_of_scope is a valid classification, not an error"""


class IntentResult:
    agent_type: str
    confidence: float
    reasoning: str


def classify(provider, query: str) -> IntentResult:
    cache_entry = find_cache_entry(query)
    if cache_entry is not None:
        result = IntentResult()
        result.agent_type = cache_entry.agent_type
        result.confidence = cache_entry.confidence
        result.reasoning = "matched cached demo scenario"
        return result

    intent_schema = {
        "type": "object",
        "properties": {
            "agent_type": {
                "type": "string",
                "enum": ["navigation", "operations", "accessibility", "out_of_scope"],
            },
            "confidence": {"type": "number"},
            "reasoning": {"type": "string"},
        },
        "required": ["agent_type", "confidence", "reasoning"],
    }

    try:
        data = provider.generate(INTENT_SYSTEM_PROMPT, query, intent_schema)
        if data is None:
            raise RuntimeError("provider returned None")

        result = IntentResult()
        result.agent_type = data.get("agent_type", "out_of_scope")
        result.confidence = data.get("confidence", 0.0)
        result.reasoning = data.get("reasoning", "")
        return result

    except Exception as e:
        result = IntentResult()
        result.agent_type = "operations"
        result.confidence = 0.5
        result.reasoning = f"fallback due to classification error: {e}"
        return result
