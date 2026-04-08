
from app.db.redis import redis_client

async def close_redis() -> None:
    await redis_client.aclose()