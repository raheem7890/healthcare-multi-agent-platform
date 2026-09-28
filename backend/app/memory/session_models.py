from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel


class SessionMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    agent: str | None = None
    timestamp: datetime

    @classmethod
    def now(cls, role: Literal["user", "assistant"], content: str, agent: str | None = None):
        return cls(role=role, content=content, agent=agent, timestamp=datetime.now(timezone.utc))

