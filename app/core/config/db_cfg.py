
from pydantic import BaseSettings, SettingsConfigDict


class DBCfg(BaseSettings):

    # .env 文件 -> 默认值
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
        )

    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/pet-system"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600
