from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.repositories.profiles import ProfileRepository
from app.schemas.profiles import ProfileCreate, ProfileRead, ProfileUpdate
from app.security.auth import CurrentUser, get_current_user
from app.security.authorization import owned_profile


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("", response_model=list[ProfileRead])
def list_profiles(
    current_user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    return ProfileRepository(db).list_for_user(current_user.id)


@router.post("", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
def create_profile(
    payload: ProfileCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ProfileRepository(db).create(current_user.id, payload)


@router.patch("/{profile_id}", response_model=ProfileRead)
def update_profile(
    profile_id: str,
    payload: ProfileUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = owned_profile(db, current_user.id, profile_id)
    return ProfileRepository(db).update(profile, payload)


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    profile_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = owned_profile(db, current_user.id, profile_id)
    ProfileRepository(db).delete(profile)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

