
from redis.asyncio import Redis
from app.core.config import get_redis_cfg
redis_cfg = get_redis_cfg()


redis_client: Redis = Redis.from_url(
    redis_cfg.REDIS_URL,
    decode_responses=redis_cfg.REDIS_DECODE_RESPONSES,
)


async def close_redis() -> None:
    await redis_client.aclose()