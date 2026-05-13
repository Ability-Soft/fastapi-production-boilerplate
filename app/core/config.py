# Built by AbilitySoft | abilitysoft.net
"""
Application configuration loaded from environment variables.

Uses pydantic-settings to validate and parse .env values at startup,
ensuring the app fails fast on misconfiguration rather than at runtime.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration object.

    All values are read from environment variables or the `.env` file.
    Defaults are provided for development; override them in production.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ───────────────────────────────────────────────
    APP_NAME: str = "FastAPI Boilerplate"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Production-ready FastAPI boilerplate by AbilitySoft"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"  # development | staging | production

    # ── Server ────────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_HOSTS: List[str] = ["*"]

    # ── Database (PostgreSQL) ─────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db"
    DB_ECHO_LOG: bool = False  # Echo SQL queries to console (noisy)
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # ── Redis ─────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── JWT Authentication ────────────────────────────────────────
    SECRET_KEY: str = "CHANGE-ME-in-production-use-openssl-rand-hex-32"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── CORS ──────────────────────────────────────────────────────
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # ── Logging ───────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"

    # ── Pagination defaults ───────────────────────────────────────
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    Using ``lru_cache`` ensures the .env file is parsed only once per process.
    """
    return Settings()
