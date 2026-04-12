from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class Provider(str, Enum):
    YANDEX = "yandex"
    GIGACHAT = "gigachat"
    OPENAI = "openai"

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000)
    provider: Provider
    model: Optional[str] = None
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(1000, ge=1, le=8000)

class CompareRequest(BaseModel):
    prompt: str
    providers: List[Provider]
    temperature: float = 0.7