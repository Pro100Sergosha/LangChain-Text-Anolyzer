from abc import ABC, abstractmethod
from typing import Dict


class AIClient(ABC):
    @abstractmethod
    async def analyze_text(self, text: str) -> Dict[str, str]:
        pass
