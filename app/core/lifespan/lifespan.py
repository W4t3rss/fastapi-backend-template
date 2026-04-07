
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .redis import close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield                     
    await close_redis()      
