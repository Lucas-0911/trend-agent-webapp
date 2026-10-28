"""Base agent interface."""
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    name: str = "base"

    @abstractmethod
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Receive context, return updated context or result."""
        pass
