"""
Application config.
"""

import os
from pathlib import Path
from typing import Dict

from pydantic import BaseModel
from sqlalchemy import URL


class Paths:
    ROOT_DIR_SRC: Path = Path(__file__).parent
    PATH_TO_BASE_FOLDER = Path(__file__).parent.parent


class ApiPrefix(BaseModel):
    """URL paths."""

    prefix: str = "/api/users-management"
    healthcheck: str = "/healthcheck"
    liveness: str = "/liveness"
    readiness: str = "/readiness"
    v1_prefix: str = "/v1"
    users: str = "/users"


class DatabaseConfig(BaseModel):
    """Config to connect to SQL database"""

    DRIVER: str = os.getenv("DB_DRIVER")
    USER: str = os.getenv("DB_USER")
    PASS: str = os.getenv("DB_PASS")
    HOST: str = os.getenv("DB_HOST")
    PORT: int = int(os.getenv("DB_PORT"))
    NAME: str = os.getenv("DB_NAME")
    ECHO: bool = bool(int(os.getenv("DB_ECHO")))
    ECHO_POOL: bool = bool(int(os.getenv("DB_ECHO_POOL")))
    POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE"))
    MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW"))

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.DRIVER,
            username=self.USER,
            password=self.PASS,
            host=self.HOST,
            port=self.PORT,
            database=self.NAME,
        )

    naming_convention: Dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RedisConfig(BaseModel):
    """Config to connect to Redis database"""

    HOST: str = os.getenv("REDIS_HOST")
    PORT: int = int(os.getenv("REDIS_PORT"))
    CACHE_DB: int = int(os.getenv("REDIS_CACHE_DB"))
    USERNAME: str = os.getenv("REDIS_USERNAME")
    PASSWORD: str = os.getenv("REDIS_PASSWORD")

    USERS_CACHE_LIFETIME: int = int(os.getenv("REDIS_USERS_CACHE_LIFETIME"))

    @property
    def users_cache_url(self) -> str:
        return f"redis://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.CACHE_DB}"


class Settings:
    mode: bool = str(os.getenv("MODE"))
    api_key: str = os.getenv("API_KEY")
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    paths: Paths = Paths()


def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()  # Setting class singleton.
