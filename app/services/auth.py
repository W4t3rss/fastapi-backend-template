
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.lifespan import logger
from app.core.security.code import get_code_cooldown_key
from app.exceptions.base import AppBaseException
from app.exceptions.users import PhoneAlreadyExistsException
from app.schemas.auth import SendCodeRequest
from app.crud import get_user_by_phone_number, get_user_by_id
from app.exceptions import *
from app.core.security.code import create_code, create_code_hash_test, create_code_hash, verify_code_hash, get_code_cache_key, get_code_cooldown_key
from app.schemas.auth import SendCodeRequest, RegisterRequest
from app.core.config import get_security_cfg
security_cfg = get_security_cfg()


# SendCode
async def send_code_service(db:AsyncSession, redis:Redis,send_code: SendCodeRequest) -> None:
    try:    
        if send_code.scene == security_cfg.REGISTER_SCENE:
            user = await get_user_by_phone_number(db, send_code.phone_number)
            if user:
                logger.warning("Send code failed: phone_number already registered, phone_number={}", send_code.phone_number)
                raise PhoneAlreadyExistsException()     
        elif send_code.scene == security_cfg.RESET_PASSWORD_SCENE:
            user = await get_user_by_phone_number(db, send_code.phone_number)
            if not user:
                logger.warning("Send code failed: phone_number not registered, phone_number={}", send_code.phone_number)
                raise PhoneNotRegisteredException()     
        else:
            logger.warning("Send code failed: invalid scene, scene={}", send_code.scene)
            raise ValueError("Invalid scene")
        
        cooldown_key = get_code_cooldown_key(send_code.scene, send_code.phone_number)
        cooldown_set = await redis.set(cooldown_key, 1, ex=security_cfg.CODE_COOLDOWN_SECONDS, nx=True)

        if not cooldown_set:
            logger.warning("Send code failed: cooldown active, scene={}, phone_number={}", send_code.scene, send_code.phone_number)
            raise CodeSendTooFrequentlyException()
        
        code = create_code()  # 生成验证码
        if send_code.return_code:
            code, code_hash = create_code_hash_test(code)
        if not send_code.return_code:
            code_hash = create_code_hash(code)
        cache_key = get_code_cache_key(send_code.scene, send_code.phone_number)
        await redis.set(cache_key, code_hash, ex=security_cfg.CODE_EXPIRE_SECONDS)

        if send_code.return_code:
            logger.CRITICAL("Verification code generated and stored in Redis: scene={}, phone_number={}, code={}", send_code.scene, send_code.phone_number, code)
        else:
            logger.info("Verification code generated and stored in Redis: scene={}, phone_number={}", send_code.scene, send_code.phone_number)

    except AppBaseException:
        await redis.delete(get_code_cooldown_key(send_code.scene, send_code.phone_number))
        raise
    except Exception as e:
        await redis.delete(get_code_cooldown_key(send_code.scene, send_code.phone_number))
        logger.exception("Unexpected error during sending code: {}", e)
        raise


# Login
async def login_service() -> dict:
    pass


# Register
async def register_service() -> dict:
    pass


# Reset Password
async def reset_password_service() -> None:
    pass


