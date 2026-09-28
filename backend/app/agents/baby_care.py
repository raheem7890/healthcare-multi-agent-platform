from app.agents.llm import LLMService
from app.schemas.chat import AgentResponse


SYSTEM_PROMPT = """You are a baby and child care education assistant speaking to a responsible
adult. Give age-aware, cautious information. Never diagnose or prescribe. Do not assume age,
weight, history, or guardian status. Recommend pediatric review whenever age or symptom severity
makes remote guidance inappropriate."""


class BabyCareAgent:
    def __init__(self, llm: LLMService):
        self.llm = llm

    async def run(self, message: str) -> AgentResponse:
        fallback = (
            "Children, especially young infants, can need earlier medical assessment than adults. "
            "Please share the child's age, measured temperature if relevant, and how feeding, breathing, "
            "alertness, and wet diapers compare with normal. Contact a pediatric clinician promptly if "
            "you are worried or the child is worsening."
        )
        text = await self.llm.respond(SYSTEM_PROMPT, message, fallback)
        return AgentResponse(
            response_text=text,
            category="baby_care",
            urgency="soon",
            recommended_action="Contact a pediatric clinician if symptoms are new, persistent, or worsening.",
            follow_up_questions=[
                "How old is the child?",
                "Are feeding, breathing, alertness, and wet diapers normal?",
            ],
            appointment_handoff=True,
        )

