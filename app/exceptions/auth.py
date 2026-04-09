
from typing import Any
from app.core.config.error_cfg import get_error_cfg
from .base import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    ServiceUnavailableException,
    UnauthorizedException,
)
error_cfg = get_error_cfg()


class InvalidCredentialsException(UnauthorizedException):
    def __init__(self, message: str = "Invalid credentials", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.INVALID_CREDENTIALS, details=details)


class TokenInvalidException(UnauthorizedException):
    def __init__(self, message: str = "Invalid token", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.TOKEN_INVALID, details=details)


class TokenExpiredException(UnauthorizedException):
    def __init__(self, message: str = "Token expired", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.TOKEN_EXPIRED, details=details)


class CodeRequiredException(BadRequestException):
    def __init__(self, message: str = "Code is required", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.CODE_REQUIRED, details=details)


class CodeInvalidException(BadRequestException):
    def __init__(self, message: str = "Code is invalid", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.CODE_INVALID, details=details)


class CodeExpiredException(BadRequestException):
    def __init__(self, message: str = "Code has expired", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.CODE_EXPIRED, details=details)


class CodeSendTooFrequentlyException(BadRequestException):
    def __init__(self, message: str = "Code sent too frequently", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.CODE_SEND_TOO_FREQUENTLY, details=details)


class VerificationCodeServiceUnavailableException(ServiceUnavailableException):
    def __init__(self, message: str = "Verification code service is unavailable", *, details: Any | None = None) -> None:
        super().__init__(
            message=message,
            error_code=error_cfg.VERIFICATION_CODE_SERVICE_UNAVAILABLE,
            details=details,
        )


class PhoneNotRegisteredException(NotFoundException):
    def __init__(self, message: str = "Phone number is not registered", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.PHONE_NOT_REGISTERED, details=details)


class PhoneNotVerifiedException(ForbiddenException):
    def __init__(self, message: str = "Phone number is not verified", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.PHONE_NOT_VERIFIED, details=details)


class OldPasswordIncorrectException(BadRequestException):
    def __init__(self, message: str = "Old password is incorrect", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.OLD_PASSWORD_INCORRECT, details=details)
