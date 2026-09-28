from app.agents.llm import LLMService
from app.schemas.chat import AgentResponse


SYSTEM_PROMPT = """You are a pregnancy and postpartum education assistant. Be sensitive,
trimester-aware only when the user supplies gestational context, and conservative about escalation.
Never diagnose or prescribe. Direct concerning pregnancy or postpartum symptoms to maternity triage
or emergency care as appropriate."""


class MaternityCareAgent:
    def __init__(self, llm: LLMService):
        self.llm = llm

    async def run(self, message: str) -> AgentResponse:
        fallback = (
            "Pregnancy and postpartum symptoms should be considered in the context of gestational age "
            "and your clinical history. Please contact your maternity team if this is new, persistent, "
            "or worrying. Seek urgent care for bleeding, severe pain, breathing difficulty, severe "
            "headache with vision changes, or reduced fetal movement."
        )
        text = await self.llm.respond(SYSTEM_PROMPT, message, fallback)
        return AgentResponse(
            response_text=text,
            category="maternity_care",
            urgency="soon",
            recommended_action="Contact your maternity team for individualized advice.",
            follow_up_questions=[
                "How many weeks pregnant are you, or how long ago did you give birth?",
                "When did this begin?",
            ],
            appointment_handoff=True,
        )

