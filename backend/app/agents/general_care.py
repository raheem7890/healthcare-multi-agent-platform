from app.agents.llm import LLMService
from app.schemas.chat import AgentResponse


SYSTEM_PROMPT = """You are a general care education assistant. Provide cautious, concise health
information. Never diagnose, prescribe, change medication doses, or imply certainty. Recommend an
appropriate level of professional care and identify warning signs. The backend has already screened
immediate red flags, but you must remain safety conscious."""


class GeneralCareAgent:
    def __init__(self, llm: LLMService):
        self.llm = llm

    async def run(self, message: str) -> AgentResponse:
        fallback = (
            "I can help with general health information, but I can't diagnose the cause from chat. "
            "Monitor how you feel, rest and stay hydrated when appropriate, and arrange a clinician "
            "review if symptoms persist, worsen, or concern you."
        )
        text = await self.llm.respond(SYSTEM_PROMPT, message, fallback)
        return AgentResponse(
            response_text=text,
            category="general_care",
            urgency="routine",
            recommended_action="Monitor symptoms and contact a clinician if they persist or worsen.",
            follow_up_questions=["When did this start?", "Are the symptoms worsening?"],
            appointment_handoff=True,
        )

