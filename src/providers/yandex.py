import httpx
import json
import time
from typing import Optional
from src.providers.base import BaseProvider
from src.config import settings


class YandexProvider(BaseProvider):
    def __init__(self):
        super().__init__("yandex")
        self.api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.api_key = settings.yandex_api_key
        self.folder_id = settings.yandex_folder_id
        self.default_model = settings.yandex_model

    async def generate(
            self,
            prompt: str,
            model: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: int = 1000
    ) -> tuple[str, int, int]:
        start_time = time.time()

        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "modelUri": f"gpt://{self.folder_id}/{model or self.default_model}",
            "completionOptions": {
                "stream": False,
                "temperature": temperature,
                "maxTokens": max_tokens
            },
            "messages": [
                {
                    "role": "user",
                    "text": prompt
                }
            ]
        }

        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.post(
                self.api_url,
                headers=headers,
                json=body
            )

            if response.status_code != 200:
                raise Exception(f"YandexGPT API error: {response.text}")

            data = response.json()
            result = data.get("result", {}).get("alternatives", [{}])[0].get("message", {}).get("text", "")
            latency = int((time.time() - start_time) * 1000)

            return result, latency, 0

    async def health_check(self) -> bool:
        if not self.api_key or not self.folder_id:
            return False
        try:
            await self.generate("ping", max_tokens=1)
            return True
        except:
            return False