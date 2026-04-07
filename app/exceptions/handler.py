
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.base import AppBaseException
from app.utils import logger


# AppBaseException handler
async def app_base_exception_handler(request: Request, exc: AppBaseException) -> JSONResponse:
    if exc.http_status_code >= 500:
        logger.error(
            "AppBaseException: error_code={}, message={}, details={}",
            exc.error_code,
            exc.message,
            exc.details,
        )
    else:
        logger.warning(
            "AppBaseException: error_code={}, message={}, details={}",
            exc.error_code,
            exc.message,
            exc.details,
        )

    return JSONResponse(
        status_code=exc.http_status_code,
        content=exc.to_dict(),
    )


# HTTPException handler
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.warning("HTTPException: status_code={}, detail={}", exc.status_code, exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": "HTTP_ERROR",
            "message": exc.detail,
            "details": None,
        },
    )


# RequestValidationError handler
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("RequestValidationError: {}", exc.errors())

    return JSONResponse(
        status_code=422,
        content={
            "error_code": "VALIDATION_ERROR",
            "message": "Validation error occurred.",
            "details": exc.errors(),
        },
    )


# SQLAlchemyError handler
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.exception("SQLAlchemyError: {}", exc)

    return JSONResponse(
        status_code=500,
        content={
            "error_code": "DATABASE_ERROR",
            "message": "A database error occurred.",
            "details": None,
        },
    )


# Generic exception handler
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception: {}", exc)

    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred.",
            "details": None,
        },
    )