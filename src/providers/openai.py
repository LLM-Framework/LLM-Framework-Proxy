import httpx
import time
from typing import Optional
from src.providers.base import BaseProvider
from src.config import settings


class OpenAIProvider(BaseProvider):
    def __init__(self):
        super().__init__("openai")
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.api_key = settings.openai_api_key
        self.default_model = settings.openai_model

    async def generate(
            self,
            prompt: str,
            model: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: int = 1000
    ) -> tuple[str, int, int]:
        start_time = time.time()

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "model": model or self.default_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.post(
                self.api_url,
                headers=headers,
                json=body
            )

            if response.status_code != 200:
                raise Exception(f"OpenAI API error: {response.text}")

            data = response.json()
            result = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            latency = int((time.time() - start_time) * 1000)
            tokens_used = data.get("usage", {}).get("total_tokens", 0)

            return result, latency, tokens_used

    async def health_check(self) -> bool:
        if not self.api_key:
            return False
        return True