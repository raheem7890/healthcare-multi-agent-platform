from uuid import uuid4

from sqlalchemy.orm import Session

from app.database.repositories.audit import AuditRepository
from app.graph.state import HealthcareState
from app.memory.long_term_memory import LongTermMemoryService
from app.memory.session_store import SessionStore
from app.schemas.chat import ChatRequest, ChatResponse


DISCLAIMER = "This information is educational and does not replace care from a licensed clinician."


class ChatService:
    def __init__(self, db: Session, session_store: SessionStore, workflow):
        self.db = db
        self.session_store = session_store
        self.workflow = workflow

    async def respond(self, user_id: str, request: ChatRequest, profile=None) -> ChatResponse:
        request_id = str(uuid4())
        recent = await self.session_store.get_messages(user_id, request.session_id)
        memories = LongTermMemoryService(self.db).retrieve(user_id, request.profile_id)
        state: HealthcareState = {
            "request_id": request_id,
            "user_id": user_id,
            "session_id": request.session_id,
            "profile_id": request.profile_id,
            "profile_type": profile.profile_type if profile else None,
            "message": request.message,
            "recent_messages": [item.model_dump(mode="json") for item in recent],
            "long_term_memory": memories,
        }
        result = await self.workflow.ainvoke(state)
        agent_response = result["agent_response"]
        if profile and profile.memory_consent and agent_response.category not in {"emergency", "booking"}:
            LongTermMemoryService(self.db).remember(
                user_id,
                profile.id,
                f"{agent_response.category}: user asked about {request.message[:500]}",
                consent=True,
            )
        AuditRepository(self.db).record(
            request_id=request_id,
            user_id=user_id,
            event_type="chat_routed",
            agent_type=agent_response.category,
            payload={"urgency": agent_response.urgency, "session_id": request.session_id},
        )
        return ChatResponse(
            request_id=request_id,
            session_id=request.session_id,
            agent=agent_response.category,
            urgency=agent_response.urgency,
            response=agent_response.response_text,
            recommended_action=agent_response.recommended_action,
            follow_up_questions=agent_response.follow_up_questions,
            appointment_handoff_available=agent_response.appointment_handoff,
            disclaimer=DISCLAIMER if agent_response.disclaimer_required else None,
        )
