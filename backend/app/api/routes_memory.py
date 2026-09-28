from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.repositories.memory import MemoryRepository
from app.schemas.memory import MemoryRead
from app.security.auth import CurrentUser, get_current_user
from app.security.authorization import owned_memory, owned_profile


router = APIRouter(prefix="/memory", tags=["memory"])


@router.get("", response_model=list[MemoryRead])
def list_memory(
    profile_id: str | None = None,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if profile_id:
        owned_profile(db, current_user.id, profile_id)
    return MemoryRepository(db).list_for_user(current_user.id, profile_id)


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memory(
    memory_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    memory = owned_memory(db, current_user.id, memory_id)
    db.delete(memory)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

