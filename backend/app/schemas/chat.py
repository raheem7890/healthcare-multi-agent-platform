from typing import Literal

from pydantic import BaseModel, Field


AgentCategory = Literal["general_care", "baby_care", "maternity_care", "booking", "emergency"]
Urgency = Literal["routine", "soon", "urgent", "emergency"]


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=8, max_length=64)
    profile_id: str | None = None
    message: str = Field(min_length=1, max_length=4_000)


class AgentResponse(BaseModel):
    response_text: str
    category: AgentCategory
    urgency: Urgency
    recommended_action: str
    follow_up_questions: list[str] = Field(default_factory=list)
    appointment_handoff: bool = False
    disclaimer_required: bool = True
    citations: list[str] = Field(default_factory=list)


class ChatResponse(BaseModel):
    request_id: str
    session_id: str
    agent: AgentCategory
    urgency: Urgency
    response: str
    recommended_action: str
    follow_up_questions: list[str]
    appointment_handoff_available: bool
    disclaimer: str | None = None

