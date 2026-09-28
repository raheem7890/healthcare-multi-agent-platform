from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.connection import Base
from app.database.models import PatientProfile, User
from app.schemas.appointments import AppointmentCreate, SlotSearchRequest
from app.services.appointment_service import AppointmentService


@pytest.fixture
def db() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.mark.asyncio
async def test_local_booking_flow(db: Session) -> None:
    user = User(external_auth_id="booking-test")
    db.add(user)
    db.flush()
    profile = PatientProfile(user_id=user.id, profile_type="adult", display_name="Test User")
    db.add(profile)
    db.commit()

    start = datetime.now(timezone.utc) + timedelta(days=1)
    end = start + timedelta(days=7)
    service = AppointmentService(db)
    slots = await service.search(
        SlotSearchRequest(
            profile_id=profile.id,
            specialty="General Care",
            date_from=start,
            date_to=end,
        )
    )

    assert slots
    slot = slots[0]
    appointment = await service.create(
        user.id,
        AppointmentCreate(
            profile_id=profile.id,
            slot_id=slot.slot_id,
            provider_id=slot.provider_id,
            provider_name=slot.provider_name,
            specialty=slot.specialty,
            scheduled_at=slot.starts_at,
            confirmed=True,
        ),
    )
    assert appointment.status == "confirmed"
    assert appointment.booking_reference.startswith("local-")
