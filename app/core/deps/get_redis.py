
from collections.abc import AsyncGenerator
from redis.asyncio import Redis
from app.db.redis import redis_client


async def get_redis() -> AsyncGenerator[Redis, None]:
    yield redis_client