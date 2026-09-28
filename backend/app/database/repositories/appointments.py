from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Appointment, utc_now


class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: str) -> list[Appointment]:
        return list(
            self.db.scalars(
                select(Appointment)
                .where(Appointment.user_id == user_id)
                .order_by(Appointment.scheduled_at)
            )
        )

    def create(self, **values: object) -> Appointment:
        appointment = Appointment(**values)
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def is_slot_available(
        self,
        *,
        provider_id: str,
        scheduled_at: datetime,
        exclude_appointment_id: str | None = None,
    ) -> bool:
        query = select(Appointment.id).where(
            Appointment.provider_id == provider_id,
            Appointment.scheduled_at == scheduled_at,
            Appointment.status != "cancelled",
        )
        if exclude_appointment_id:
            query = query.where(Appointment.id != exclude_appointment_id)
        return self.db.scalar(query) is None

    def save(self, appointment: Appointment) -> Appointment:
        appointment.updated_at = utc_now()
        self.db.commit()
        self.db.refresh(appointment)
        return appointment
