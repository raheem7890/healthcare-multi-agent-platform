from typing import NotRequired, TypedDict

from app.schemas.chat import AgentResponse


class HealthcareState(TypedDict):
    request_id: str
    user_id: str
    session_id: str
    profile_id: str | None
    profile_type: str | None
    message: str
    recent_messages: list[dict]
    long_term_memory: list[str]
    intent: NotRequired[str]
    urgency: NotRequired[str]
    red_flags: NotRequired[list[str]]
    agent_response: NotRequired[AgentResponse]

