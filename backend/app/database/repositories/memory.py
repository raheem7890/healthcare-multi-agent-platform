from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import MemorySummary


class MemoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: str, profile_id: str | None = None) -> list[MemorySummary]:
        query = select(MemorySummary).where(MemorySummary.user_id == user_id)
        if profile_id:
            query = query.where(MemorySummary.profile_id == profile_id)
        return list(self.db.scalars(query.order_by(MemorySummary.created_at.desc())))

    def create(self, user_id: str, profile_id: str, summary: str) -> MemorySummary:
        item = MemorySummary(user_id=user_id, profile_id=profile_id, summary_text=summary)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

