from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_ENV_FILE,
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Healthcare Multi-Agent API"
    app_env: str = "development"
    api_prefix: str = "/v1"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    database_url: str = "sqlite:///./healthcare.db"
    redis_url: str | None = None
    session_ttl_seconds: int = 86_400
    booking_draft_ttl_seconds: int = 1_800

    dev_auth_bypass: bool = True
    jwt_secret: str | None = None
    jwt_algorithm: str = "HS256"
    jwt_issuer: str | None = None
    jwt_audience: str | None = None

    llm_api_key: str | None = None
    llm_model: str = "gpt-4.1-mini"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        return value

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if settings.is_production and settings.dev_auth_bypass:
        raise RuntimeError("DEV_AUTH_BYPASS must be disabled in production")
    return settings
