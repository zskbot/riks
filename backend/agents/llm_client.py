from typing import Any, Optional

import httpx

from config.settings import settings


class OllamaClient:
    """Small client for Ollama text generation."""

    def __init__(self, base_url: str = settings.ollama_url, model: str = settings.ollama_model) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system,
            "options": {"temperature": temperature, "num_predict": max_tokens},
            "stream": False,
        }
        response = httpx.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
        if not response.is_success:
            return {"success": False, "error": response.text, "content": ""}
        data = response.json()
        return {"success": True, "content": data.get("response", ""), "raw": data}


ollama_client = OllamaClient()
