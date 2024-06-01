from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from infrastructure.message_brokers.base import BaseMessageBroker
from logic.init import init_container
from redis import asyncio as aioredis


async def init_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()


async def close_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.stop()


async def init_cache():
    redis = aioredis.from_url("redis://redis:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
