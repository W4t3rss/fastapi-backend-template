
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppCfg(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Pet System API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "FastAPI backend for pet system"

    API_V1_PREFIX: str = "/v1"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"

    CORS_ALLOW_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]


@lru_cache
def get_app_cfg() -> AppCfg:
    return AppCfg()