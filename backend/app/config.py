"""Application configuration using Pydantic BaseSettings."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Google Gemini
    google_api_key: str = "your_google_api_key_here"
    gemini_model: str = "gemini-1.5-flash"

    # CORS
    cors_origins: list[str] = ["*"]

    # API
    api_prefix: str = ""
    app_name: str = "Women's Career Counselor API"
    debug: bool = True

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
