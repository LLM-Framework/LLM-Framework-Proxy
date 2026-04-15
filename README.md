# LLM Proxy Service

Единый API-шлюз для доступа к российским и зарубежным LLM (YandexGPT, GigaChat, OpenAI) с единым интерфейсом.

## 🎯 Назначение

Сервис предоставляет унифицированный REST API для генерации ответов от различных языковых моделей.
Позволяет абстрагироваться от различий в API конкретных провайдеров.

# Запуск сервера

```commandline
make run
```

Ермолинская Александра Александровна
УрФУ, группа РИМ-150975к

# Режим без API-ключей (Mock)

## В файле .env укажите:

```
MOCK_MODE=true
```

## Или в коде generate.py временно замените провайдеров:

providers = {
"yandex": MockProvider(),
"gigachat": MockProvider(),
"openai": MockProvider()
}

# Проверка работоспособности

```bash

# Проверка здоровья
curl http://localhost:8002/health

# Список провайдеров
curl http://localhost:8002/api/v1/providers

# Тест генерации (Mock-режим)
curl -X POST http://localhost:8002/api/v1/generate/yandex \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Скажи привет"}'
```


---

# 🏗️ Архитектура


## Поток данных

```mermaid
sequenceDiagram
    participant Client
    participant LLMProxy as LLM Proxy Service
    participant Router as Generate Router
    participant Provider as YandexProvider
    participant YandexAPI as YandexGPT API
    
    Client->>LLMProxy: POST /generate/yandex
    Note over Client,LLMProxy: {prompt: "Скажи привет"}
    
    LLMProxy->>Router: Валидация запроса
    Router->>Router: Проверка provider_name
    
    Router->>Provider: generate(prompt, temperature)
    Note over Router,Provider: Вызов через BaseProvider
    
    Provider->>Provider: Формирование headers + body
    Provider->>YandexAPI: POST /completion
    Note over Provider,YandexAPI: Authorization: Api-Key xxx
    
    YandexAPI-->>Provider: {result: {...}}
    Provider->>Provider: Извлечение текста, измерение latency
    
    Provider-->>Router: (response_text, latency_ms, tokens)
    Router-->>LLMProxy: GenerateResponse
    LLMProxy-->>Client: JSON ответ

```

## Зависимости и технологии

```mermaid
graph LR
    subgraph Core["Основные"]
        FastAPI[FastAPI]
        Uvicorn[Uvicorn]
        Pydantic[Pydantic v2]
    end
    
    subgraph HTTP["HTTP клиенты"]
        HTTPX[HTTPX]
    end
    
    subgraph Utils["Утилиты"]
        Tenacity[Tenacity - retry]
        PythonDotEnv[python-dotenv]
    end
    
    subgraph Monitoring["Мониторинг"]
        Prometheus[Prometheus Client]
    end
    
    FastAPI --> Pydantic
    FastAPI --> Uvicorn
    Providers --> HTTPX
    Providers --> Tenacity
    Config --> PythonDotEnv
    API --> Prometheus

```

## Взаимодействие сервисов
 
```mermaid
graph LR
    Translator[Translator Service<br/>:8001] -->|переведённый промпт| Proxy
    Proxy[LLM Proxy Service<br/>:8002] -->|ответ LLM| Evaluator
    Evaluator[Evaluator Service<br/>:8003] -->|оценка| Frontend
    Frontend[Frontend<br/>Streamlit :8501] -->|запрос| Proxy

    style Translator fill:#e1f5fe,stroke:#01579b
    style Proxy fill:#fff3e0,stroke:#e65100
    style Evaluator fill:#e8f5e9,stroke:#1b5e20
    style Frontend fill:#f3e5f5,stroke:#4a148c
```

## Лицензия

MIT

## Автор
Ермолинская Александра Александровна
УрФУ, группа РИМ-150975к