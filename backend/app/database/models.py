from datetime import date, datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


def uuid_str() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    external_auth_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    profiles: Mapped[list["PatientProfile"]] = relationship(back_populates="user")


class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    profile_type: Mapped[str] = mapped_column(String(30))
    display_name: Mapped[str] = mapped_column(String(255))
    relationship_to_user: Mapped[str | None] = mapped_column(String(50))
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    pregnancy_due_date: Mapped[date | None] = mapped_column(Date)
    medical_notes: Mapped[str | None] = mapped_column(Text)
    memory_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    user: Mapped[User] = relationship(back_populates="profiles")


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    session_id: Mapped[str] = mapped_column(String(64), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class MemorySummary(Base):
    __tablename__ = "memory_summaries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    profile_id: Mapped[str | None] = mapped_column(ForeignKey("patient_profiles.id"), index=True)
    memory_type: Mapped[str] = mapped_column(String(50), default="conversation_summary")
    summary_text: Mapped[str] = mapped_column(Text)
    importance_score: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    profile_id: Mapped[str] = mapped_column(ForeignKey("patient_profiles.id"), index=True)
    provider_id: Mapped[str] = mapped_column(String(100))
    provider_name: Mapped[str] = mapped_column(String(255))
    specialty: Mapped[str] = mapped_column(String(100))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(30), default="confirmed")
    booking_reference: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    request_id: Mapped[str] = mapped_column(String(64), index=True)
    user_id: Mapped[str | None] = mapped_column(String(36), index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    agent_type: Mapped[str | None] = mapped_column(String(50))
    event_payload: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
