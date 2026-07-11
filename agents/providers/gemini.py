"""StadiumOS AI — Gemini LLM Provider

Secondary runtime provider. Used when LLM_PROVIDER=gemini is set.
"""

import json
import os
import traceback

from google.genai import types as genai_types


class GeminiProvider:
    MODEL = "gemini-2.0-flash"

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        self._client = None
        self._available = bool(self.api_key)

        if self._available:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Gemini client init failed: {e}")
                self._available = False

    def available(self) -> bool:
        return self._available

    def model_name(self) -> str:
        return self.MODEL

    def generate(self, system_prompt: str, user_message: str, response_schema: dict) -> dict | None:
        if not self._available or self._client is None:
            return None

        try:
            response = self._client.models.generate_content(
                model=self.MODEL,
                contents=user_message,
                config=genai_types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3,
                    response_mime_type="application/json",
                    response_schema=response_schema,
                ),
            )
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(text)

        except Exception as e:
            print("=== GEMINI CALL FAILED ===")
            print(f"Exception type: {type(e).__name__}")
            print(f"Exception message: {e}")
            traceback.print_exc()
            print("=== END GEMINI FAILURE ===")
            return None
