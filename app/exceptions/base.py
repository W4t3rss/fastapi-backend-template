
from typing import Any


# Base
class AppBaseException(Exception):
    def __init__(
            self,
            message: str ,
            *, 
            error_code:str = "ERROR",
            http_status_code: int = 400,
            details: Any | None = None
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.http_status_code = http_status_code
        self.details = details
        super().__init__(message)

    def to_dict(self) -> dict:
        return {
            "error_code": self.error_code,
            "message": self.message,
            # "http_status_code": self.http_status_code,   
            "details": self.details
        }


# 400 Bad Request
class BadRequestException(AppBaseException):
    def __init__(
        self,
        message: str,
        *,
        error_code: str = "BAD_REQUEST",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            http_status_code=400,
            details=details
        )


# 401 Unauthorized
class UnauthorizedException(AppBaseException):
    def __init__(
        self,
        message: str,
        *,
        error_code: str = "UNAUTHORIZED",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            http_status_code=401,
            details=details
        )


# 403 Forbidden
class ForbiddenException(AppBaseException):
    def __init__(
        self,
        message: str,
        *,
        error_code: str = "FORBIDDEN",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            http_status_code=403,
            details=details
        )


# 404 Not Found
class NotFoundException(AppBaseException):
    def __init__(
        self,
        message: str,
        *,
        error_code: str = "NOT_FOUND",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            http_status_code=404,
            details=details
        )


# 409 Conflict
class ConflictException(AppBaseException):
    def __init__(
        self,
        message: str,
        *,
        error_code: str = "CONFLICT",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            http_status_code=409,
            details=details
        )

# 422 Validation Error
class ValidationErrorException(AppBaseException):
    def __init__(
        self,
        message: str,
        *,
        error_code: str = "VALIDATION_ERROR",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            http_status_code=422,
            details=details
        )


# 503 Service Unavailable
class ServiceUnavailableException(AppBaseException):
    def __init__(
        self,
        message: str,
        *,
        error_code: str = "SERVICE_UNAVAILABLE",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            http_status_code=503,
            details=details
        )


# 500 Internal Server Error
class InternalServerErrorException(AppBaseException):
    def __init__(
        self,
        message: str,
        *,
        error_code: str = "INTERNAL_SERVER_ERROR",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            http_status_code=500,
            details=details
        )




