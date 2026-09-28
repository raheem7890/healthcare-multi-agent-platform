from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Appointment, MemorySummary, PatientProfile


def owned_profile(db: Session, user_id: str, profile_id: str) -> PatientProfile:
    profile = db.scalar(
        select(PatientProfile).where(
            PatientProfile.id == profile_id,
            PatientProfile.user_id == user_id,
        )
    )
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


def owned_appointment(db: Session, user_id: str, appointment_id: str) -> Appointment:
    appointment = db.scalar(
        select(Appointment).where(Appointment.id == appointment_id, Appointment.user_id == user_id)
    )
    if appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment


def owned_memory(db: Session, user_id: str, memory_id: str) -> MemorySummary:
    memory = db.scalar(
        select(MemorySummary).where(MemorySummary.id == memory_id, MemorySummary.user_id == user_id)
    )
    if memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")
    return memory

