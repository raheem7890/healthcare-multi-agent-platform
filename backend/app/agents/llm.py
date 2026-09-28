from langchain_openai import ChatOpenAI

from app.config import Settings


class LLMService:
    def __init__(self, settings: Settings):
        self.model = (
            ChatOpenAI(model=settings.llm_model, api_key=settings.llm_api_key, temperature=0.1)
            if settings.llm_api_key
            else None
        )

    async def respond(self, system_prompt: str, user_message: str, fallback: str) -> str:
        if self.model is None:
            return fallback
        result = await self.model.ainvoke(
            [("system", system_prompt), ("human", user_message)]
        )
        return str(result.content)

