"""Application settings using pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Server configuration
    app_port: int = 4000
    app_host: str = "0.0.0.0"

    # Input timeout configuration (in seconds)
    input_timeout: int = 540  # 9 minutes

    # Local assistant configuration
    assistant_host: str = "localhost"
    assistant_port: int = 4141
    assistant_timeout: int = 10  # seconds
    assistant_model: str = "gpt-5-mini"

    # Notification configuration
    notification_enabled: bool = True
    notification_max_content_length: int = 200


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
