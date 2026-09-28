from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_schema() -> None:
    from app.database import models  # noqa: F401

    inspector = inspect(engine)
    if "appointments" in inspector.get_table_names():
        columns = {column["name"] for column in inspector.get_columns("appointments")}
        if "factory_reference_id" in columns and "booking_reference" not in columns:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE appointments "
                        "RENAME COLUMN factory_reference_id TO booking_reference"
                    )
                )
    Base.metadata.create_all(bind=engine)
