from typing import Any
from .base import ConflictException, NotFoundException
from app.core.config.error_cfg import get_error_cfg
error_cfg = get_error_cfg()


# 宠物不存在
class PetNotFoundException(NotFoundException):
    def __init__(self, message: str = "Pet not found", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.PET_NOT_FOUND, details=details)


# 宠物主人不存在
class OwnerNotFoundException(NotFoundException):
    def __init__(self, message: str = "Owner not found", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.OWNER_NOT_FOUND, details=details)


# 宠物已存在
class PetAlreadyExistsException(ConflictException):
    def __init__(self, message: str = "Pet already exists", *, details: Any | None = None) -> None:
        super().__init__(message=message, error_code=error_cfg.PET_ALREADY_EXISTS, details=details)

