import json

from sqlalchemy.orm import Session

from app.database.models import AuditEvent


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def record(
        self,
        *,
        request_id: str,
        user_id: str | None,
        event_type: str,
        agent_type: str | None = None,
        payload: dict[str, object] | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            request_id=request_id,
            user_id=user_id,
            event_type=event_type,
            agent_type=agent_type,
            event_payload=json.dumps(payload or {}),
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
