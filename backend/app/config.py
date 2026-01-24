"""
Application configuration management.
Loads settings from environment variables.
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str

    # AI Services
    ANTHROPIC_API_KEY: str
    AI_MODEL: str = "claude-sonnet-4-5"  # Default: Claude Sonnet 4.5 (auto-updates)

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application
    APP_NAME: str = "German Learning App"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Redis (optional)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'  # Ignore unknown environment variables (e.g., BATCH_* vars)
    )


# Global settings instance
settings = Settings()
