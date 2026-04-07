
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisCfg(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_DECODE_RESPONSES: bool = True


@lru_cache
def get_redis_cfg() -> RedisCfg:
    return RedisCfg()