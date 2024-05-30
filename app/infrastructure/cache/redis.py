from functools import cached_property

from aioredis import Redis

from infrastructure.cache.base import AbstractCacheService
from logic.init import init_container
from settings.config import Settings


class RedisCacheService(AbstractCacheService):
    @cached_property
    def client(self):
        container = init_container()
        settings: Settings = container.resolve(Settings)
        return Redis(host=settings.redis_url)

    async def set_cache(self, key: str, value: str, ex: int):
        self.client.set(key, value, ex=ex)

    async def get_cache(self, key: str) -> str:
        return self.client.get(key)
