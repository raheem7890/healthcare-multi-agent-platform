from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SlotSearchRequest(BaseModel):
    profile_id: str
    specialty: str = Field(min_length=2, max_length=100)
    date_from: datetime
    date_to: datetime
    location: str | None = Field(default=None, max_length=255)


class AppointmentSlot(BaseModel):
    slot_id: str
    provider_id: str
    provider_name: str
    specialty: str
    starts_at: datetime
    location: str


class AppointmentCreate(BaseModel):
    profile_id: str
    slot_id: str
    provider_id: str
    provider_name: str
    specialty: str
    scheduled_at: datetime
    confirmed: bool


class AppointmentUpdate(BaseModel):
    slot_id: str
    scheduled_at: datetime
    confirmed: bool


class AppointmentCancel(BaseModel):
    confirmed: bool


class AppointmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    profile_id: str
    provider_id: str
    provider_name: str
    specialty: str
    scheduled_at: datetime
    status: str
    booking_reference: str
    created_at: datetime
