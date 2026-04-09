
from passlib.context import CryptContext


# 密码哈希上下文配置
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
