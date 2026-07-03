from __future__ import annotations

from typing import Any


class RedisWorldStateStore:
    """Redis boundary with an in-memory fallback for local tests/demo."""

    def __init__(self) -> None:
        self._memory: dict[str, Any] = {}
        self._redis = None
        try:
            import redis  # type: ignore

            self._redis = redis.Redis.from_url("redis://localhost:6379/0", decode_responses=True)
            self._redis.ping()
        except Exception:
            self._redis = None

    def set_json(self, key: str, value: dict) -> None:
        if self._redis:
            import json

            self._redis.set(key, json.dumps(value, default=str))
        self._memory[key] = value

    def get_json(self, key: str):
        if self._redis:
            import json

            raw = self._redis.get(key)
            if raw:
                return json.loads(raw)
        return self._memory.get(key)

    def reset(self) -> None:
        self._memory.clear()
