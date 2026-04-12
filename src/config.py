from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Service
    proxy_host: str = "0.0.0.0"
    proxy_port: int = 8002
    debug: bool = True
    log_level: str = "INFO"

    # YandexGPT
    yandex_api_key: Optional[str] = None
    yandex_folder_id: Optional[str] = None
    yandex_model: str = "yandexgpt-lite"

    # GigaChat
    gigachat_api_key: Optional[str] = None
    gigachat_model: str = "GigaChat"
    gigachat_scope: str = "GIGACHAT_API_PERS"

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"

    # Circuit Breaker
    circuit_breaker_failure_threshold: int = 3
    circuit_breaker_recovery_timeout: int = 30

    # Timeouts
    request_timeout: int = 30
    max_retries: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()