from abc import ABC, abstractmethod
from typing import Optional


class BaseProvider(ABC):
    def __init__(self, name: str):
        self.name = name
        self._available = True

    @abstractmethod
    async def generate(
            self,
            prompt: str,
            model: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: int = 1000
    ) -> tuple[str, int, int]:
        """
        Returns: (response_text, latency_ms, tokens_used)
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass

    @property
    def available(self) -> bool:
        return self._available

    @available.setter
    def available(self, value: bool):
        self._available = value