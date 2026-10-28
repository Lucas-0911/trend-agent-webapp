"""Event Bus — trung tâm giao tiếp theo hướng sự kiện."""
from typing import Any, Callable, Dict, List
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self.history: List[Dict[str, Any]] = []
        self.max_history = 200

    def emit(self, event: str, data: Dict[str, Any] = None, source: str = "system"):
        payload = {
            "id": str(uuid.uuid4())[:8],
            "event": event,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": source,
            "data": data or {},
        }
        self.history.insert(0, payload)
        if len(self.history) > self.max_history:
            self.history.pop()

        logger.info(f"[Event] {event} ← {source}")
        for handler in self._handlers.get(event, []):
            try:
                handler(payload)
            except Exception as e:
                logger.error(f"Handler error on {event}: {e}")
        for handler in self._handlers.get("*", []):
            try:
                handler(payload)
            except Exception as e:
                logger.error(f"Wildcard handler error: {e}")

    def on(self, event: str, handler: Callable):
        self._handlers.setdefault(event, []).append(handler)

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.history[:limit]


# Singleton
bus = EventBus()
