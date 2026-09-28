from app.schemas.chat import AgentResponse


def build_emergency_response(red_flags: list[str]) -> AgentResponse:
    self_harm = "self_harm" in red_flags
    if self_harm:
        text = (
            "You may be in immediate danger. Contact local emergency services or a crisis service now, "
            "and stay with a trusted person if you can. If you might act on these thoughts, move away "
            "from anything you could use to harm yourself."
        )
    else:
        text = (
            "These symptoms may need immediate medical attention. Contact your local emergency services "
            "or go to the nearest emergency department now. Do not wait for a chat response if the "
            "person is getting worse."
        )
    return AgentResponse(
        response_text=text,
        category="emergency",
        urgency="emergency",
        recommended_action="Seek immediate emergency help.",
        follow_up_questions=[],
        appointment_handoff=False,
    )

