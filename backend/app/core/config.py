"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed, single-source configuration for the API."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ATHENA_",
        extra="ignore",
        enable_decoding=False,
    )

    environment: str = "development"
    database_url: str = "sqlite:///./athena.db"
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    allowed_origins: list[str] = ["http://localhost:8080"]
    unlock_all_lessons: bool = False

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
