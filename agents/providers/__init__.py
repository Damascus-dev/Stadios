"""StadiumOS AI — LLM Provider Abstraction Layer

All runtime inference is routed through this interface.
The orchestrator never communicates directly with provider-specific SDKs.
"""

import os
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Interface every LLM provider must implement."""

    @abstractmethod
    def generate(self, system_prompt: str, user_message: str, response_schema: dict) -> dict | None:
        ...

    @abstractmethod
    def available(self) -> bool:
        ...

    @abstractmethod
    def model_name(self) -> str:
        ...


def get_provider() -> LLMProvider:
    provider_name = os.environ.get("LLM_PROVIDER", "deepseek").lower().strip()

    if provider_name == "deepseek":
        from .deepseek import DeepSeekProvider
        return DeepSeekProvider()
    elif provider_name == "gemini":
        from .gemini import GeminiProvider
        return GeminiProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}. Supported: deepseek, gemini")
