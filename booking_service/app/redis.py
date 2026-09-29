import redis.asyncio as aioredis
from app.core.config import settings

class RedisClient:
    def __init__(self) -> None:
        self.client: aioredis.Redis | None = None

    async def connect(self) -> None:
        self.client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    async def close(self) -> None:
        if self.client:
            await self.client.close()

    async def get(self, key: str) -> str | None:
        if not self.client:
            return None
        return await self.client.get(key)

    async def set(self, key: str, value: str, expire: int = 60) -> None:
        if self.client:
            await self.client.set(key, value, ex=expire)

    async def delete_by_pattern(self, pattern: str) -> None:
        """Инвалидация ключей по паттерну (например, 'hotels:*')"""
        if self.client:
            keys = await self.client.keys(pattern)
            if keys:
                await self.client.delete(*keys)

redis_client = RedisClient()