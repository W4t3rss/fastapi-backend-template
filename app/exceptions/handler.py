
from app.utils import logger
from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.base import AppBaseException
from app.exceptions import *
from app.utils import logger
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError


# 继承自 AppBaseException 的异常处理器
async def app_base_exception_handler(request: Request, exc: AppBaseException) -> JSONResponse:
    """
    处理继承自 AppBaseException 的异常
    param request: 请求对象
    param exc: 异常对象
    return: JSON 响应
    """

    if exc.http_status_code >= 500:
        logger.error(
            f"AppBaseException: {exc.error_code} - {exc.message} - Details: {exc.details}"
        )
    else:
        logger.warning(
            f"AppBaseException: {exc.error_code} - {exc.message} - Details: {exc.details}"
        )

    return JSONResponse(
        status_code=exc.http_status_code,  # HTTP 状态码
        content=exc.to_dict()  # 异常信息字典
    )


# HTTPException 处理器
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    处理 HTTPException 异常
    param request: 请求对象
    param exc: HTTPException 异常对象
    return: JSON 响应
    """

    logger.warning(
        f"HTTPException: {exc.status_code} - {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,  # HTTP 状态码
        content={
            "error_code": "HTTP_ERROR",
            "message": exc.detail,
            "details": None
        }
    )


# Pydantic ValidationError 处理器
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """
    处理 Pydantic ValidationError 异常
    param request: 请求对象
    param exc: ValidationError 异常对象
    return: JSON 响应
    """

    logger.warning(
        f"ValidationError: {exc.errors()}"
    )

    return JSONResponse(
        status_code=422,  # Unprocessable Entity
        content={
            "error_code": "VALIDATION_ERROR",
            "message": "Validation error occurred.",
            "details": exc.errors()
        }
    )

# SQLAlchemy Error 处理器
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    处理 SQLAlchemyError 异常
    param request: 请求对象
    param exc: SQLAlchemyError 异常对象
    return: JSON 响应
    """

    logger.error(f"SQLAlchemyError: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,  # Internal Server Error
        content={
            "error_code": "DATABASE_ERROR",
            "message": "A database error occurred.",
            "details": str(exc)
        }
    )


# 处理未被捕获的异常
async def generic_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    处理未被捕获的异常
    param request: 请求对象
    param exc: 异常对象
    return: JSON 响应
    """

    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,  # Internal Server Error
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred.",
            "details": None
        }
    )