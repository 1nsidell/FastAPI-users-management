import pytest

from users_management.gateways.connections.impls.sql import (
    SQLDatabaseHelperImpl,
)


@pytest.fixture(scope="session")
async def sql_helper(settings):
    SQLDHhelper = SQLDatabaseHelperImpl(settings)
    SQLDHhelper.startup()
    yield SQLDHhelper
    await SQLDHhelper.shutdown()
