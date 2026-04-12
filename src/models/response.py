from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class GenerateResponse(BaseModel):
    prompt: str
    response: str
    provider: str
    model: str
    latency_ms: int
    tokens_used: Optional[int] = None
    cached: bool = False

class CompareResponse(BaseModel):
    prompt: str
    results: Dict[str, GenerateResponse]
    total_latency_ms: int

class ProviderInfo(BaseModel):
    name: str
    available: bool
    models: List[str]

class HealthResponse(BaseModel):
    status: str
    service: str
    providers: Dict[str, bool]
    timestamp: datetime