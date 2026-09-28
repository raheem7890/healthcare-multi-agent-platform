from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.repositories.appointments import AppointmentRepository
from app.database.repositories.audit import AuditRepository
from app.schemas.appointments import (
    AppointmentCancel,
    AppointmentCreate,
    AppointmentRead,
    AppointmentSlot,
    AppointmentUpdate,
    SlotSearchRequest,
)
from app.security.auth import CurrentUser, get_current_user
from app.security.authorization import owned_appointment, owned_profile
from app.services.appointment_service import AppointmentService


router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("", response_model=list[AppointmentRead])
def list_appointments(
    current_user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    return AppointmentRepository(db).list_for_user(current_user.id)


@router.post("/slots/search", response_model=list[AppointmentSlot])
async def search_slots(
    payload: SlotSearchRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    owned_profile(db, current_user.id, payload.profile_id)
    try:
        return await AppointmentService(db).search(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.post("", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    payload: AppointmentCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    owned_profile(db, current_user.id, payload.profile_id)
    try:
        appointment = await AppointmentService(db).create(current_user.id, payload)
        AuditRepository(db).record(
            request_id=str(uuid4()),
            user_id=current_user.id,
            event_type="appointment_created",
            agent_type="booking",
            payload={"appointment_id": appointment.id},
        )
        return appointment
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.patch("/{appointment_id}", response_model=AppointmentRead)
async def reschedule_appointment(
    appointment_id: str,
    payload: AppointmentUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appointment = owned_appointment(db, current_user.id, appointment_id)
    try:
        updated = await AppointmentService(db).reschedule(appointment, payload)
        AuditRepository(db).record(
            request_id=str(uuid4()),
            user_id=current_user.id,
            event_type="appointment_rescheduled",
            agent_type="booking",
            payload={"appointment_id": appointment.id},
        )
        return updated
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.delete("/{appointment_id}", response_model=AppointmentRead)
async def cancel_appointment(
    appointment_id: str,
    payload: AppointmentCancel,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appointment = owned_appointment(db, current_user.id, appointment_id)
    try:
        updated = await AppointmentService(db).cancel(appointment, payload.confirmed)
        AuditRepository(db).record(
            request_id=str(uuid4()),
            user_id=current_user.id,
            event_type="appointment_cancelled",
            agent_type="booking",
            payload={"appointment_id": appointment.id},
        )
        return updated
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
