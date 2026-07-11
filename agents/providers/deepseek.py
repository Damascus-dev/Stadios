"""StadiumOS AI — DeepSeek LLM Provider

Uses DeepSeek's OpenAI-compatible API endpoint.
Default runtime provider for StadiumOS AI.
"""

import json
import os
import traceback
from http.client import HTTPSConnection


class DeepSeekProvider:
    BASE_HOST = "api.deepseek.com"
    MODEL = "deepseek-chat"

    def __init__(self):
        self.api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        self._available = bool(self.api_key)

    def available(self) -> bool:
        return self._available

    def model_name(self) -> str:
        return self.MODEL

    def generate(self, system_prompt: str, user_message: str, response_schema: dict) -> dict | None:
        if not self._available:
            print("DeepSeek: API key not configured (DEEPSEEK_API_KEY missing)")
            return None

        payload = json.dumps({
            "model": self.MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.3,
            "max_tokens": 2048,
            "response_format": {"type": "json_object"},
        })

        try:
            conn = HTTPSConnection(self.BASE_HOST, timeout=30)
            conn.request(
                "POST",
                "/v1/chat/completions",
                body=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
            )
            resp = conn.getresponse()
            body = resp.read().decode()
            conn.close()

            if resp.status != 200:
                print(f"DeepSeek API error: {resp.status} {resp.reason}")
                print(body[:500])
                return None

            data = json.loads(body)
            content = data["choices"][0]["message"]["content"]

            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()

            return json.loads(content)

        except Exception as e:
            print("=== DEEPSEEK CALL FAILED ===")
            print(f"Exception type: {type(e).__name__}")
            print(f"Exception message: {e}")
            traceback.print_exc()
            print("=== END DEEPSEEK FAILURE ===")
            return None
