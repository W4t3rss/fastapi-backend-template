
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .admin import init_admin_user
from .logger import logger
from .redis import close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup initiated")
    await init_admin_user()
    logger.info("Application startup completed")
    try:
        yield
    finally:
        await close_redis()
        logger.info("Application shutdown completed")