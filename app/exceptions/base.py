
from typing import Any


# Base
class BaseException(Exception):
    def __init__(
            self,
            message: str ,
            *,  # 位置参数 message，其他参数必须使用关键字传递
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
            # 通常不建议在异常响应中直接返回 HTTP 状态码，因为它已经包含在 HTTP 响应的状态行中
            # "http_status_code": self.http_status_code,  # 
            "details": self.details
        }


# 400 Bad Request
class BadRequestException(BaseException):
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
class UnauthorizedException(BaseException):
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
class ForbiddenException(BaseException):
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
class NotFoundException(BaseException):
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
class ConflictException(BaseException):
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

# 422 Unprocessable Entity
class UnprocessableEntityException(BaseException):
    def __init__(
        self,
        message: str,
        *,
        error_code: str = "UNPROCESSABLE_ENTITY",
        details: Any | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            http_status_code=422,
            details=details
        )


# 500 Internal Server Error
class InternalServerErrorException(BaseException):
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




