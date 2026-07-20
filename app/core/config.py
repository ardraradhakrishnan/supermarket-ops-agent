from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    database_url: str = Field(..., alias="DATABASE_URL")
    # google_api_key: str = Field(..., alias="GOOGLE_API_KEY")
    telegram_bot_token: str = Field(..., alias="TELEGRAM_BOT_TOKEN")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    google_api_key: str | None = Field(default=None, alias="GOOGLE_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    Ensures environment variables are loaded only once.
    """
    return Settings()