from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.runtime import session_store, workflow
from app.schemas.chat import ChatRequest, ChatResponse
from app.security.auth import CurrentUser, get_current_user
from app.security.authorization import owned_profile
from app.services.chat_service import ChatService


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = owned_profile(db, current_user.id, payload.profile_id) if payload.profile_id else None
    return await ChatService(db, session_store, workflow).respond(current_user.id, payload, profile)

