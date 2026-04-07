
from typing import Any
from .base import ConflictException, ForbiddenException, NotFoundException
from app.core.config.error_cfg import get_error_cfg
error_cfg = get_error_cfg()



# 用户不存在
class UserNotFoundException(NotFoundException):
    def __init__(self, message: str = "User not found", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.USER_NOT_FOUND, details=details)


# 用户名已存在
class UsernameAlreadyExistsException(ConflictException):
    def __init__(self, message: str = "Username already exists", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.USERNAME_ALREADY_EXISTS, details=details)


# 手机号已存在
class PhoneAlreadyExistsException(ConflictException):
    def __init__(self, message: str = "Phone number already exists", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.PHONE_ALREADY_EXISTS, details=details)


# 不允许删除自己
class CannotDeleteSelfException(ForbiddenException):
    def __init__(self, message: str = "Cannot delete yourself", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.CANNOT_DELETE_SELF, details=details)


