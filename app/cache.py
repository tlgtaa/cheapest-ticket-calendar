import aioredis


class Cache:
    async def startup(self):
        self.redis = await aioredis.create_redis_pool(
            "redis://127.0.0.1", encoding="utf8"
        )

    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()

    async def get(self, *args, **kwargs):
        return await self.redis.get(*args, **kwargs)

    async def set(self, *args, **kwargs):
        return await self.redis.set(*args, **kwargs)


cache = Cache()
