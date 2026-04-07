
from typing import Any
from .base import BadRequestException, ForbiddenException, NotFoundException, UnauthorizedException
from app.core.config.error_cfg import get_error_cfg
error_cfg = get_error_cfg()


# 用户名或密码错误
class InvalidCredentialsException(UnauthorizedException):
    def __init__(self, message: str = "Invalid credentials", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.INVALID_CREDENTIALS, details=details)


# Token 无效
class TokenInvalidException(UnauthorizedException):
    def __init__(self, message: str = "Invalid token", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.TOKEN_INVALID, details=details)


# Token 已过期
class TokenExpiredException(UnauthorizedException):
    def __init__(self, message: str = "Token expired", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.TOKEN_EXPIRED, details=details)


# 缺少验证码
class CodeRequiredException(BadRequestException):
    def __init__(self, message: str = "Code is required", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.CODE_REQUIRED, details=details)


# 验证码错误
class CodeInvalidException(BadRequestException):
    def __init__(self, message: str = "Code is invalid", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.CODE_INVALID, details=details)


# 验证码过期
class CodeExpiredException(BadRequestException):
    def __init__(self, message: str = "Code has expired", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.CODE_EXPIRED, details=details)


# 验证码发送过于频繁
class CodeSendTooFrequentlyException(BadRequestException):
    def __init__(self, message: str = "Code sent too frequently", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.CODE_SEND_TOO_FREQUENTLY, details=details)


# 手机号未注册
class PhoneNotRegisteredException(NotFoundException):
    def __init__(self, message: str = "Phone number is not registered", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.PHONE_NOT_REGISTERED, details=details)


# 手机号未验证
class PhoneNotVerifiedException(ForbiddenException):
    def __init__(self, message: str = "Phone number is not verified", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.PHONE_NOT_VERIFIED, details=details)


# 原密码错误
class OldPasswordIncorrectException(BadRequestException):
    def __init__(self, message: str = "Old password is incorrect", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.OLD_PASSWORD_INCORRECT, details=details)

