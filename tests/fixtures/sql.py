import pytest

from users_management.gateways.connections.impls.sql import (
    SQLDatabaseManagerImpl,
)


@pytest.fixture(scope="session")
async def sql_helper(settings):
    SQLDHhelper = SQLDatabaseManagerImpl(settings)
    SQLDHhelper.startup()
    yield SQLDHhelper
    await SQLDHhelper.shutdown()
