from fastapi import APIRouter
from datetime import datetime
from src.models.response import HealthResponse
from src.api.routes.generate import providers

router = APIRouter()


@router.get("/health")
async def health():
    provider_status = {}
    for name, provider in providers.items():
        provider_status[name] = await provider.health_check()

    return HealthResponse(
        status="healthy",
        service="llm-proxy",
        providers=provider_status,
        timestamp=datetime.now()
    )


@router.get("/providers")
async def list_providers():
    return {
        "providers": [
            {
                "name": "yandex",
                "available": providers["yandex"].available,
                "models": ["yandexgpt-lite", "yandexgpt-pro"]
            },
            {
                "name": "gigachat",
                "available": providers["gigachat"].available,
                "models": ["GigaChat", "GigaChat-Pro"]
            },
            {
                "name": "openai",
                "available": providers["openai"].available,
                "models": ["gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
            }
        ]
    }