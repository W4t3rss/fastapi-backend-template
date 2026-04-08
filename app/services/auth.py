
from dataclasses import dataclass
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.lifespan import logger
from app.core.security.code import get_code_cooldown_key
from app.core.security.hash import verify_password
from app.crud.users import get_user_by_user_name
from app.exceptions.auth import CodeExpiredException, CodeInvalidException, CodeSendTooFrequentlyException, InvalidCredentialsException, PhoneNotRegisteredException
from app.exceptions.base import AppBaseException
from app.exceptions.users import PhoneAlreadyExistsException
from app.schemas.auth import LoginRequest, ResetPasswordRequest, SendCodeRequest
from app.crud import get_user_by_phone_number
from app.core.security.code import create_code, create_code_hash_test, create_code_hash, verify_code_hash, get_code_cache_key, get_code_cooldown_key
from app.schemas.auth import SendCodeRequest, RegisterRequest
from app.core.security.jwt import create_access_token
from app.core.config import get_security_cfg
from app.schemas.users import UserCreate, UserUpdate
from app.services.users import create_user_service, update_user_service
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


@dataclass
class LoginResult:
    id: int
    user_name: str
    access_token: str
    token_type: str = "bearer"
    message: str = "Login successful"

async def login_service(db: AsyncSession, login: LoginRequest) -> LoginResult:
    try:
        user = await get_user_by_user_name(db, login.user_name)
        if not user or not verify_password(login.password, user.password):
            logger.warning("Login failed: invalid credentials, user_name={}", login.user_name)
            raise InvalidCredentialsException()
        
        access_token = create_access_token(
            data={"sub": str(user.id), "user_name": user.user_name}
        )

        logger.info("User logged in successfully: user_id={}, user_name={}", user.id, user.user_name)
        
        return LoginResult(
            id=user.id,
            user_name=user.user_name,
            access_token=access_token,
        )

    except AppBaseException:
        raise
    except Exception as e:
        logger.exception("Unexpected error during login: {}", e)
        raise


# Register
@dataclass
class RegisterResult:
    id: int
    user_name: str
    phone_number: str | None
    message: str = "Registration successful"

async def register_service(db: AsyncSession, redis: Redis, register: RegisterRequest) -> RegisterResult:
    try:
        # 1. 验证验证码
        cache_key = get_code_cache_key(security_cfg.REGISTER_SCENE, register.phone_number)
        stored_code_hash = await redis.get(cache_key)
        if not stored_code_hash:
            logger.warning("Register failed: code expired or not found, phone_number={}", register.phone_number)
            raise CodeExpiredException()
        if not verify_code_hash(register.code, stored_code_hash):
            logger.warning("Register failed: invalid code, phone_number={}", register.phone_number)
            raise CodeInvalidException()

        # 2. 创建用户（委托给 users service，内部已处理事务）
        user_create = UserCreate(
            user_name=register.user_name,
            phone_number=register.phone_number,
            password=register.password,
        )
        user = await create_user_service(db, user_create)

        # 3. 清理验证码
        await redis.delete(cache_key)

        logger.info(
            "User registered successfully: id={}, user_name={}, phone_number={}",
            user.id, user.user_name, user.phone_number
        )
        
        return RegisterResult(
            id=user.id,
            user_name=user.user_name,
            phone_number=user.phone_number,
        )

    except AppBaseException:
        await db.rollback()         
        raise
    except Exception as e:
        await db.rollback()         
        logger.exception("Unexpected error during registration: {}", e)
        raise


# Reset Password
async def reset_password_service(db: AsyncSession, redis: Redis, reset: ResetPasswordRequest) -> None:
    try:
        if not reset.phone_number:
            raise ValueError("Phone number is required for password reset")

        # 1. 验证验证码
        cache_key = get_code_cache_key(security_cfg.RESET_PASSWORD_SCENE, reset.phone_number)
        stored_code_hash = await redis.get(cache_key)
        if not stored_code_hash:
            logger.warning("Reset password failed: code expired or not found, phone_number={}", reset.phone_number)
            raise CodeExpiredException()
        if not verify_code_hash(reset.code, stored_code_hash):
            logger.warning("Reset password failed: invalid code, phone_number={}", reset.phone_number)
            raise CodeInvalidException()

        # 2. 获取用户
        user = await get_user_by_phone_number(db, reset.phone_number)
        if not user:
            logger.warning("Reset password failed: phone not registered, phone_number={}", reset.phone_number)
            raise PhoneNotRegisteredException()

        # 3. 更新密码
        user_update = UserUpdate(password=reset.new_password)
        await update_user_service(db, user.id, user_update)

        # 4. 清理验证码
        await redis.delete(cache_key)

        logger.info("Password reset successfully for phone_number={}", reset.phone_number)

    except AppBaseException:
        await db.rollback()          
        raise
    except Exception as e:
        await db.rollback()         
        logger.exception("Unexpected error during password reset: {}", e)
        raise

