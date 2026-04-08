
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .logger import logger
from .redis import close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup completed")
    try:
        yield
    finally:
        await close_redis()
        logger.info("Application shutdown completed")