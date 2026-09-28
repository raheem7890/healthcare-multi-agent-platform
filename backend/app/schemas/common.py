from datetime import datetime

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str
    request_id: str | None = None


class StatusResponse(BaseModel):
    status: str
    timestamp: datetime

