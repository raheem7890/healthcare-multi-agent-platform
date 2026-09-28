from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import PatientProfile, utc_now
from app.schemas.profiles import ProfileCreate, ProfileUpdate


class ProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: str) -> list[PatientProfile]:
        return list(
            self.db.scalars(
                select(PatientProfile)
                .where(PatientProfile.user_id == user_id)
                .order_by(PatientProfile.created_at)
            )
        )

    def create(self, user_id: str, data: ProfileCreate) -> PatientProfile:
        profile = PatientProfile(user_id=user_id, **data.model_dump())
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def update(self, profile: PatientProfile, data: ProfileUpdate) -> PatientProfile:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(profile, key, value)
        profile.updated_at = utc_now()
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def delete(self, profile: PatientProfile) -> None:
        self.db.delete(profile)
        self.db.commit()

