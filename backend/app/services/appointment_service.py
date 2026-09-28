from datetime import datetime, time, timedelta, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.database.models import Appointment
from app.database.repositories.appointments import AppointmentRepository
from app.schemas.appointments import (
    AppointmentCreate,
    AppointmentSlot,
    AppointmentUpdate,
    SlotSearchRequest,
)


SPECIALTY_TEAMS = {
    "general care": ("local-general", "General Care Team"),
    "pediatrics": ("local-pediatrics", "Pediatric Care Team"),
    "maternity": ("local-maternity", "Maternity Care Team"),
    "postpartum care": ("local-postpartum", "Postpartum Care Team"),
}
SLOT_HOURS = (9, 11, 14, 16)


class AppointmentService:
    def __init__(self, db: Session):
        self.repository = AppointmentRepository(db)

    async def search(self, request: SlotSearchRequest) -> list[AppointmentSlot]:
        if request.date_to <= request.date_from:
            raise ValueError("date_to must be later than date_from")
        if request.date_to - request.date_from > timedelta(days=31):
            raise ValueError("Appointment searches are limited to 31 days")

        provider_id, provider_name = SPECIALTY_TEAMS.get(
            request.specialty.lower(),
            ("local-specialist", f"{request.specialty} Team"),
        )
        tz = request.date_from.tzinfo or timezone.utc
        current_day = request.date_from.date()
        last_day = request.date_to.date()
        now = datetime.now(tz)
        slots: list[AppointmentSlot] = []

        while current_day <= last_day and len(slots) < 20:
            if current_day.weekday() < 5:
                for hour in SLOT_HOURS:
                    starts_at = datetime.combine(current_day, time(hour=hour), tzinfo=tz)
                    if starts_at < request.date_from or starts_at > request.date_to or starts_at <= now:
                        continue
                    if not self.repository.is_slot_available(
                        provider_id=provider_id,
                        scheduled_at=starts_at,
                    ):
                        continue
                    slots.append(
                        AppointmentSlot(
                            slot_id=f"local:{provider_id}:{starts_at.isoformat()}",
                            provider_id=provider_id,
                            provider_name=provider_name,
                            specialty=request.specialty,
                            starts_at=starts_at,
                            location=request.location or "Main Clinic",
                        )
                    )
            current_day += timedelta(days=1)
        return slots

    async def create(self, user_id: str, request: AppointmentCreate) -> Appointment:
        if not request.confirmed:
            raise ValueError("Explicit confirmation is required")
        if request.scheduled_at <= datetime.now(request.scheduled_at.tzinfo or timezone.utc):
            raise ValueError("Appointment time must be in the future")
        if not self.repository.is_slot_available(
            provider_id=request.provider_id,
            scheduled_at=request.scheduled_at,
        ):
            raise ValueError("This appointment slot is no longer available")
        return self.repository.create(
            user_id=user_id,
            profile_id=request.profile_id,
            provider_id=request.provider_id,
            provider_name=request.provider_name,
            specialty=request.specialty,
            scheduled_at=request.scheduled_at,
            status="confirmed",
            booking_reference=f"local-{uuid4()}",
        )

    async def reschedule(self, appointment: Appointment, request: AppointmentUpdate) -> Appointment:
        if not request.confirmed:
            raise ValueError("Explicit confirmation is required")
        if request.scheduled_at <= datetime.now(request.scheduled_at.tzinfo or timezone.utc):
            raise ValueError("Appointment time must be in the future")
        if not self.repository.is_slot_available(
            provider_id=appointment.provider_id,
            scheduled_at=request.scheduled_at,
            exclude_appointment_id=appointment.id,
        ):
            raise ValueError("This appointment slot is no longer available")
        appointment.scheduled_at = request.scheduled_at
        appointment.status = "confirmed"
        return self.repository.save(appointment)

    async def cancel(self, appointment: Appointment, confirmed: bool) -> Appointment:
        if not confirmed:
            raise ValueError("Explicit confirmation is required")
        appointment.status = "cancelled"
        return self.repository.save(appointment)
