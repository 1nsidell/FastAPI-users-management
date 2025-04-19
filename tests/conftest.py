from fastapi.testclient import TestClient
import pytest

from users_management.core.settings import Settings
from users_management.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def settings():
    return Settings()
