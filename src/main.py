from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import generate, health
from src.config import settings

app = FastAPI(
    title="LLM Proxy Service",
    description="Единый шлюз для доступа к YandexGPT, GigaChat и OpenAI",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты
app.include_router(generate.router, prefix="/api/v1", tags=["Generation"])
app.include_router(health.router, tags=["Health"])

@app.get("/")
async def root():
    return {"service": "LLM Proxy Service", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.proxy_host,
        port=settings.proxy_port,
        reload=settings.debug
    )