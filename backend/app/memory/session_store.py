import asyncio
import json
from abc import ABC, abstractmethod

from redis.asyncio import Redis

from app.config import Settings
from app.memory.session_models import SessionMessage


class SessionStore(ABC):
    @abstractmethod
    async def get_messages(self, user_id: str, session_id: str) -> list[SessionMessage]: ...

    @abstractmethod
    async def append_messages(
        self, user_id: str, session_id: str, messages: list[SessionMessage]
    ) -> None: ...


class InMemorySessionStore(SessionStore):
    def __init__(self, max_messages: int = 12):
        self._messages: dict[str, list[SessionMessage]] = {}
        self._lock = asyncio.Lock()
        self.max_messages = max_messages

    @staticmethod
    def _key(user_id: str, session_id: str) -> str:
        return f"{user_id}:{session_id}"

    async def get_messages(self, user_id: str, session_id: str) -> list[SessionMessage]:
        async with self._lock:
            return list(self._messages.get(self._key(user_id, session_id), []))

    async def append_messages(
        self, user_id: str, session_id: str, messages: list[SessionMessage]
    ) -> None:
        async with self._lock:
            key = self._key(user_id, session_id)
            self._messages[key] = (self._messages.get(key, []) + messages)[-self.max_messages :]


class RedisSessionStore(SessionStore):
    def __init__(self, redis: Redis, ttl_seconds: int, max_messages: int = 12):
        self.redis = redis
        self.ttl_seconds = ttl_seconds
        self.max_messages = max_messages

    @staticmethod
    def _key(user_id: str, session_id: str) -> str:
        return f"healthcare:session:{user_id}:{session_id}:messages"

    async def get_messages(self, user_id: str, session_id: str) -> list[SessionMessage]:
        values = await self.redis.lrange(self._key(user_id, session_id), 0, -1)
        return [SessionMessage.model_validate_json(value) for value in values]

    async def append_messages(
        self, user_id: str, session_id: str, messages: list[SessionMessage]
    ) -> None:
        key = self._key(user_id, session_id)
        values = [message.model_dump_json() for message in messages]
        if values:
            await self.redis.rpush(key, *values)
            await self.redis.ltrim(key, -self.max_messages, -1)
            await self.redis.expire(key, self.ttl_seconds)


def create_session_store(settings: Settings) -> SessionStore:
    if not settings.redis_url:
        return InMemorySessionStore()
    client = Redis.from_url(settings.redis_url, decode_responses=True)
    return RedisSessionStore(client, settings.session_ttl_seconds)

