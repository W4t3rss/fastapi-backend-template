
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class SecurityCfg(BaseSettings):

    # .env 文件 -> 默认值
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
        )
    
    # JWT 配置
    SECRET_KEY: str = "I-hope-you-are-happy-every-day"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Code 验证码配置
    CODE_LENGTH: int = 6
    CODE_EXPIRE_MINUTES: int = 5
    CODE_COOLDOWN_SECONDS: int = 60
    CODE_CACHE_PREFIX: str = "auth:code:"  # Redis 中验证码的 key 前缀


@lru_cache
def get_security_cfg() -> SecurityCfg:
    return SecurityCfg()