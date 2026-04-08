
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
    REGISTER_SCENE: str = "register"
    RESET_PASSWORD_SCENE: str = "reset_password"
    CODE_LENGTH: int = 6
    CODE_EXPIRE_SECONDS: int = 5 * 60
    CODE_COOLDOWN_SECONDS: int = 60
    CODE_CACHE_PREFIX: str = "auth:code:"  # Redis 中验证码的 key 前缀

    RETURN_CODE: bool = True  # 是否在响应中返回验证码，生产环境应该设置为 False


@lru_cache
def get_security_cfg() -> SecurityCfg:
    return SecurityCfg()