
from passlib.context import CryptContext


# 密码哈希上下文配置
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_password_hash(password: str) -> str:
    """
    生成密码哈希
    param password: 明文密码
    return: 哈希后的密码
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    param plain_password: 用户输入的明文密码    
    param hashed_password: 存储的哈希密码
    return: 验证结果, True / False
    """
    return pwd_context.verify(plain_password, hashed_password)
