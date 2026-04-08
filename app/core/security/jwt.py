
from datetime import datetime, timedelta, timezone
from jose import ExpiredSignatureError, JWTError, jwt
from app.core.config import get_security_cfg
security_cfg = get_security_cfg()


def create_access_token(sub: str | int, expires_delta: timedelta | None = None) -> str:
    """
    生成 JWT 访问令牌
    """
    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta or timedelta(minutes=security_cfg.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode = {
        "sub": str(sub),
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(
        to_encode,
        security_cfg.SECRET_KEY,
        algorithm=security_cfg.ALGORITHM,
    )


def verify_access_token(token: str) -> str:
    """
    验证 JWT 访问令牌并返回 sub
    """
    try:
        payload = jwt.decode(
            token,
            security_cfg.SECRET_KEY,
            algorithms=[security_cfg.ALGORITHM],
        )
        sub = payload.get("sub")
        if sub is None:
            raise JWTError("sub not found in token")
        return sub
    except ExpiredSignatureError:
        raise
    except JWTError as e:
        raise JWTError(f"Token decode error: {str(e)}") from e