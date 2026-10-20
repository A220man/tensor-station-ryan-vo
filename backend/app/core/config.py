import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "tensor-station"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./tensor_station.db"

    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # OIDC / Keycloak
    OIDC_ENABLED: bool = True
    OIDC_ISSUER_URL: str = "http://localhost:8080/realms/tensor-station"
    OIDC_CLIENT_ID: str = "tensor-station-backend"
    OIDC_CLIENT_SECRET: str = ""
    OIDC_REDIRECT_URI: str = "http://localhost:3000/callback"
    OIDC_SCOPES: str = "openid profile email roles"

    # LLM Providers
    LLM_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "openai-compatible"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_BASE_URL: Optional[str] = None
    LLM_TIMEOUT: float = 30.0

    # Inference
    DEFAULT_DEVICE: str = "cuda"
    MAX_VRAM_USAGE_GB: float = 12.0
    ENABLE_MODEL_CACHING: bool = True
    MODEL_CACHE_DIR: str = "./models"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()