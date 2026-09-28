from app.schemas.chat import AgentResponse


PROHIBITED_PHRASES = ("i diagnose you", "definitely have", "stop taking your medication")


def validate_agent_response(response: AgentResponse) -> AgentResponse:
    normalized = response.response_text.lower()
    if any(phrase in normalized for phrase in PROHIBITED_PHRASES):
        return AgentResponse(
            response_text=(
                "I can't safely provide a definitive diagnosis or change a prescription. "
                "Please contact a licensed clinician for an assessment."
            ),
            category=response.category,
            urgency="soon",
            recommended_action="Contact a licensed clinician.",
            appointment_handoff=True,
        )
    return response

