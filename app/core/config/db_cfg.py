
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class DbCfg(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
        )
    
    DB_URL: str = ""
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600
    LIMIT: int = 10

    INIT_ADMIN: str = "admin"
    INIT_ADMIN_PASSWORD: str = ""


@lru_cache
def get_db_cfg() -> DbCfg:
    return DbCfg()


