
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import get_security_cfg
security_cfg = get_security_cfg()


def create_access_token(sub:str | int, expires_delta: timedelta | None = None) -> str:
    """
    生成 JWT 访问令牌
    param sub: 用户 ID 或其他唯一标识符
    param expires_delta: 令牌过期时间，默认为 security_cfg.ACCESS_TOKEN_EXPIRE_MINUTES 分钟
    return: JWT 访问令牌字符串
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=security_cfg.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"sub": str(sub),"iat": now,"exp": expire}
    encoded_jwt = jwt.encode(to_encode, security_cfg.SECRET_KEY, algorithm=security_cfg.ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> str | int:
    """
    验证 JWT 访问令牌并返回 sub
    param token: JWT 访问令牌字符串
    return: sub
    """
    try:
        payload = jwt.decode(token, security_cfg.SECRET_KEY, algorithms=[security_cfg.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise JWTError("sub not found in token")
        return sub
    except JWTError as e:
        raise JWTError(f"Token decode error: {str(e)}") from e