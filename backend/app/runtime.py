from app.agents.baby_care import BabyCareAgent
from app.agents.booking import BookingAgent
from app.agents.general_care import GeneralCareAgent
from app.agents.llm import LLMService
from app.agents.maternity_care import MaternityCareAgent
from app.config import get_settings
from app.graph.workflow import build_workflow
from app.memory.session_store import create_session_store


settings = get_settings()
session_store = create_session_store(settings)
llm_service = LLMService(settings)
workflow = build_workflow(
    session_store=session_store,
    general_agent=GeneralCareAgent(llm_service),
    baby_agent=BabyCareAgent(llm_service),
    maternity_agent=MaternityCareAgent(llm_service),
    booking_agent=BookingAgent(),
)
