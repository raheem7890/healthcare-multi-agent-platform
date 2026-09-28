from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas.common import StatusResponse


router = APIRouter(tags=["health"])


@router.get("/health", response_model=StatusResponse)
def health() -> StatusResponse:
    return StatusResponse(status="ok", timestamp=datetime.now(timezone.utc))

