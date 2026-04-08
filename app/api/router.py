
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from app.middlewares import AccessLogMiddleware, RequestContextMiddleware
from app.api.v1 import v1_router
from app.core.config import get_app_cfg
from app.core.lifespan import lifespan
from app.exceptions.base import AppBaseException
from app.exceptions.handler import (
    app_base_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    sqlalchemy_exception_handler,
    validation_exception_handler,
)
app_cfg = get_app_cfg()


def create_app() -> FastAPI:
    app = FastAPI(
        title=app_cfg.APP_NAME,  # 应用名称
        version=app_cfg.APP_VERSION,  # 应用版本
        description=app_cfg.APP_DESCRIPTION,  # 应用描述
        docs_url=app_cfg.DOCS_URL,  # Swagger UI文档路径
        redoc_url=app_cfg.REDOC_URL,  # ReDoc文档路径
        openapi_url=app_cfg.OPENAPI_URL,  # OpenAPI规范路径
        lifespan=lifespan,  # 应用生命周期函数
    )

    app.add_middleware(AccessLogMiddleware)
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_cfg.CORS_ALLOW_ORIGINS,
        allow_credentials=app_cfg.CORS_ALLOW_CREDENTIALS,
        allow_methods=app_cfg.CORS_ALLOW_METHODS,
        allow_headers=app_cfg.CORS_ALLOW_HEADERS,
    )

    app.include_router(v1_router, prefix=app_cfg.API_V1_PREFIX)

    app.add_exception_handler(AppBaseException, app_base_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    @app.get("/", include_in_schema=False)
    async def root() -> dict[str, str]:
        return {
            "message": f"{app_cfg.APP_NAME} is running",
            "docs": app_cfg.DOCS_URL,
            "version": app_cfg.APP_VERSION,
        }

    @app.get("/health", tags=["system"], summary="Health check")
    async def health_check() -> dict[str, str]:
        return {
            "status": "ok",
            "service": app_cfg.APP_NAME,
            "version": app_cfg.APP_VERSION,
        }

    return app


app = create_app()