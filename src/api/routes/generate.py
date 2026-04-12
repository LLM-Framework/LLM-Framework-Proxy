from fastapi import APIRouter, HTTPException
from src.models.request import GenerateRequest
from src.models.response import GenerateResponse
from src.providers import YandexProvider, GigaChatProvider, OpenAIProvider
import time

router = APIRouter()

# Инициализация провайдеров
providers = {
    "yandex": YandexProvider(),
    "gigachat": GigaChatProvider(),
    "openai": OpenAIProvider()
}


@router.post("/generate/{provider_name}")
async def generate(provider_name: str, request: GenerateRequest):
    if provider_name not in providers:
        raise HTTPException(status_code=404, detail=f"Provider {provider_name} not found")

    provider = providers[provider_name]

    if not provider.available:
        raise HTTPException(status_code=503, detail=f"Provider {provider_name} is unavailable")

    try:
        response_text, latency, tokens = await provider.generate(
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        return GenerateResponse(
            prompt=request.prompt,
            response=response_text,
            provider=provider_name,
            model=request.model or provider.default_model,
            latency_ms=latency,
            tokens_used=tokens if tokens > 0 else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))