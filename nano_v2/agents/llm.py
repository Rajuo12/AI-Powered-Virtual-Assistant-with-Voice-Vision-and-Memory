"""
Nano AI v2 - LLM Manager
Supports:
- Ollama
- Future Gemini/OpenAI support
"""

from __future__ import annotations

import requests

from nano_v2.config.settings import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)


class LLMManager:

    def __init__(self):

        self.provider = "ollama"

        self.model = OLLAMA_MODEL

    # -----------------------------

    def chat(self, prompt: str) -> str:

        try:

            url = f"{OLLAMA_BASE_URL}/api/generate"

            response = requests.post(
                url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=120,
            )

            response.raise_for_status()

            return response.json()["response"]

        except Exception as e:

            return f"[LLM ERROR] {e}"

    # -----------------------------

    def ping(self):

        try:

            r = requests.get(
                f"{OLLAMA_BASE_URL}/api/tags",
                timeout=5,
            )

            return r.status_code == 200

        except Exception:

            return False