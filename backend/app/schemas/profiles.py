from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ProfileType = Literal["adult", "baby", "child", "maternity"]


class ProfileCreate(BaseModel):
    profile_type: ProfileType
    display_name: str = Field(min_length=1, max_length=255)
    relationship_to_user: str | None = Field(default=None, max_length=50)
    date_of_birth: date | None = None
    pregnancy_due_date: date | None = None
    medical_notes: str | None = Field(default=None, max_length=2_000)
    memory_consent: bool = False


class ProfileUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=255)
    relationship_to_user: str | None = Field(default=None, max_length=50)
    date_of_birth: date | None = None
    pregnancy_due_date: date | None = None
    medical_notes: str | None = Field(default=None, max_length=2_000)
    memory_consent: bool | None = None


class ProfileRead(ProfileCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime

