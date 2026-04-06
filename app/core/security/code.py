from operator import is_
import random
from datetime import datetime, timedelta, timezone
from app.core.config import get_security_cfg
security_cfg = get_security_cfg()


def create_code() -> tuple[str, datetime]:
    """
    生成验证码字符串 和 对应过期时间
    return: (验证码字符串, 验证码过期时间的 datetime 对象)
    """
    length = security_cfg.CODE_LENGTH
    code = ''.join(random.choices('0123456789', k=length))
    now = datetime.now(timezone.utc)
    expire_time = now + timedelta(minutes=security_cfg.CODE_EXPIRE_MINUTES) 
    return code, expire_time


def verify_code_expired(expire_time: datetime) -> bool:
    """
    判断验证码是否过期
    param expire_time: 验证码过期时间的 datetime 对象
    return: True 如果验证码已过期，否则 False
    """
    now = datetime.now(timezone.utc)
    return now > expire_time