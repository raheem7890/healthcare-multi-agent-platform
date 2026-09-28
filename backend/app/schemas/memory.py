from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MemoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    profile_id: str | None
    memory_type: str
    summary_text: str
    importance_score: float
    created_at: datetime

