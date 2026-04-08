
import hashlib
import hmac
import random
from app.core.config import get_security_cfg
security_cfg = get_security_cfg()


def create_code() -> str:
    """
    生成纯数字验证码
    """
    return "".join(random.choices("0123456789", k=security_cfg.CODE_LENGTH))


def create_code_hash(code: str) -> str:
    """
    对验证码做哈希，避免在 Redis 里明文存储验证码
    """
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


# 下面这个函数是为了测试用的，生产环境可以直接使用 create_code_hash，并且不返回原始验证码
def create_code_hash_test(code: str) -> tuple[str, str]:
    """
    对验证码做哈希，避免在 Redis 里明文存储验证码
    返回原始验证码，用于开发环境测试，生产环境可以只返回哈希值
    """
    return code, hashlib.sha256(code.encode("utf-8")).hexdigest()  


def verify_code_hash(code: str, code_hash: str) -> bool:
    """
    比较验证码与哈希是否匹配
    """
    current_hash = create_code_hash(code)
    return hmac.compare_digest(current_hash, code_hash)


def get_code_cache_key(scene: str, phone_number: str) -> str:
    """
    验证码缓存 key
    """
    return f"{security_cfg.CODE_CACHE_PREFIX}:{scene}:{phone_number}"


def get_code_cooldown_key(scene: str, phone_number: str) -> str:
    """
    验证码发送冷却 key
    """
    return f"{security_cfg.CODE_CACHE_PREFIX}:cooldown:{scene}:{phone_number}"