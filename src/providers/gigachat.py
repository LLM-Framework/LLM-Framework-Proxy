import httpx
import time
from typing import Optional
from src.providers.base import BaseProvider
from src.config import settings


class GigaChatProvider(BaseProvider):
    def __init__(self):
        super().__init__("gigachat")
        self.auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.api_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        self.api_key = settings.gigachat_api_key
        self.default_model = settings.gigachat_model
        self._access_token = None
        self._token_expires_at = 0

    async def _get_token(self) -> str:
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "RqUID": "12345678-1234-1234-1234-123456789abc",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.auth_url,
                headers=headers,
                data="scope=GIGACHAT_API_PERS"
            )

            if response.status_code != 200:
                raise Exception(f"GigaChat auth error: {response.text}")

            data = response.json()
            self._access_token = data.get("access_token")
            self._token_expires_at = time.time() + data.get("expires_at", 3600) - 60
            return self._access_token

    async def generate(
            self,
            prompt: str,
            model: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: int = 1000
    ) -> tuple[str, int, int]:
        start_time = time.time()
        token = await self._get_token()

        headers = {
            "Authorization": f"Bearer {token}",
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
                raise Exception(f"GigaChat API error: {response.text}")

            data = response.json()
            result = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            latency = int((time.time() - start_time) * 1000)
            tokens_used = data.get("usage", {}).get("total_tokens", 0)

            return result, latency, tokens_used

    async def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            await self.generate("ping", max_tokens=1)
            return True
        except:
            return False