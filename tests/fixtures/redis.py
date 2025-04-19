import pytest

from users_management.gateways.connections.impls.redis import (
    RedisConnectionManagerImpl,
)


@pytest.fixture(scope="session")
async def redis_manager(settings):
    RedisManager = RedisConnectionManagerImpl(settings)
    RedisManager.startup()
    yield RedisManager
    await RedisManager.shutdown()
