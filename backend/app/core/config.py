"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import field_validator, model_validator
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
    access_token_expire_minutes: int = 30
    public_base_url: str = "http://127.0.0.1:8000"
    cookie_secure: bool = False
    browser_session_hours: int = 12
    remember_days: int = 30
    google_client_id: str = ""
    google_client_secret: str = ""
    apple_client_id: str = ""
    apple_team_id: str = ""
    apple_key_id: str = ""
    apple_private_key: str = ""
    allowed_origins: list[str] = ["http://localhost:8080"]
    unlock_all_lessons: bool = False

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @model_validator(mode="after")
    def prevent_production_unlock_override(self):
        if self.environment.casefold() == "production" and self.unlock_all_lessons:
            raise ValueError(
                "ATHENA_UNLOCK_ALL_LESSONS cannot be enabled in production"
            )
        if self.environment.casefold() == "production" and (
            not self.cookie_secure or not self.public_base_url.startswith("https://")
        ):
            raise ValueError(
                "Production authentication requires HTTPS and ATHENA_COOKIE_SECURE=true"
            )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
