
from fastapi import APIRouter, Depends, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_security_cfg
from app.core.deps import get_db, get_redis
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
    SendCodeRequest,
    SendCodeResponse,
)
from app.services.auth import (
    login_service,
    register_service,
    reset_password_service,
    send_code_service,
)


security_cfg = get_security_cfg()
auth_router = APIRouter()


@auth_router.post(
    "/send-code",
    response_model=SendCodeResponse,
    status_code=status.HTTP_200_OK,
    summary="发送验证码",
)
async def send_code(
    send_code: SendCodeRequest,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> SendCodeResponse:
    result = await send_code_service(db, redis, send_code)
    return SendCodeResponse(
        code=result.code if (send_code.return_code or security_cfg.RETURN_CODE) else None,
        message=result.message,
    )


@auth_router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="用户注册",
)
async def register(
    register: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> RegisterResponse:
    result = await register_service(db, redis, register)
    return RegisterResponse.model_validate(result)


@auth_router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="用户登录",
)
async def login(
    login: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    result = await login_service(db, login)
    return LoginResponse.model_validate(result)


@auth_router.post(
    "/reset-password",
    response_model=ResetPasswordResponse,
    status_code=status.HTTP_200_OK,
    summary="重置密码",
)
async def reset_password(
    reset: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> ResetPasswordResponse:
    await reset_password_service(db, redis, reset)
    return ResetPasswordResponse()

