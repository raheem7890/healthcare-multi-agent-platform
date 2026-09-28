from sqlalchemy.orm import Session

from app.database.repositories.memory import MemoryRepository


class LongTermMemoryService:
    """Consent-aware access to durable memory summaries."""

    def __init__(self, db: Session):
        self.repository = MemoryRepository(db)

    def retrieve(self, user_id: str, profile_id: str | None) -> list[str]:
        return [item.summary_text for item in self.repository.list_for_user(user_id, profile_id)[:5]]

    def remember(self, user_id: str, profile_id: str, summary: str, consent: bool) -> None:
        if consent and summary.strip():
            self.repository.create(user_id, profile_id, summary.strip()[:2_000])

