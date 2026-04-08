
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
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


# app/api/v1/auth/send-code
@auth_router.post(
    "/send-code",
    response_model=SendCodeResponse,
    status_code=status.HTTP_200_OK,
    summary="Send verification code",
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


# app/api/v1/auth/register
@auth_router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="User registration",
)
async def register(
    register: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> RegisterResponse:
    result = await register_service(db, redis, register)
    return RegisterResponse.model_validate(result)


# app/api/v1/auth/login
@auth_router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
)
async def login(
    login: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    result = await login_service(db, login)
    return LoginResponse.model_validate(result)


# app/api/v1/auth/token
@auth_router.post(
    "/token",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="OAuth2 password login",
)
async def issue_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    login = LoginRequest(
        user_name=form_data.username,
        password=form_data.password,
    )
    result = await login_service(db, login)
    return LoginResponse.model_validate(result)


# app/api/v1/auth/reset-password
@auth_router.post(
    "/reset-password",
    response_model=ResetPasswordResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset password",
)
async def reset_password(
    reset: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> ResetPasswordResponse:
    await reset_password_service(db, redis, reset)
    return ResetPasswordResponse()

