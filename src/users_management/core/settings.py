"""
Application config.
"""

import os
from pathlib import Path
from typing import Dict

from pydantic import BaseModel
from sqlalchemy import URL


class Paths:
    ROOT_DIR_SRC = Path(__file__).parents[2]
    PATH_TO_BASE_FOLDER = Path(__file__).parents[3]


class ApiPrefix(BaseModel):
    """URL paths."""

    prefix: str = "/api/users-management"
    healthcheck: str = "/healthcheck"
    liveness: str = "/liveness"
    readiness: str = "/readiness"
    v1_prefix: str = "/v1"
    users: str = "/users"
    nicknames: str = users + "/nicknames"


class SQLDatabaseConfig(BaseModel):
    """Config to connect to SQL database"""

    DRIVER: str = os.getenv("SQL_DRIVER", "postgresql+asyncpg")
    USER: str = os.getenv("SQL_USER", "guest")
    PASS: str = os.getenv("SQL_PASS", "guest")
    HOST: str = os.getenv("SQL_HOST", "localhost")
    PORT: int = int(os.getenv("SQL_PORT", "5432"))
    NAME: str = os.getenv("SQL_NAME", "postgres")
    ECHO: bool = bool(int(os.getenv("SQL_ECHO", "0")))
    ECHO_POOL: bool = bool(int(os.getenv("SQL_ECHO_POOL", "0")))
    POOL_SIZE: int = int(os.getenv("SQL_POOL_SIZE", "5"))
    MAX_OVERFLOW: int = int(os.getenv("SQL_MAX_OVERFLOW", "10"))

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

    HOST: str = os.getenv("REDIS_HOST", "loaclhost")
    PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    CACHE_DB: int = int(os.getenv("REDIS_CACHE_DB", "0"))
    USERNAME: str = os.getenv("REDIS_USERNAME", "guest")
    PASSWORD: str = os.getenv("REDIS_PASSWORD", "guest")

    CACHE_LIFETIME: int = int(os.getenv("REDIS_CACHE_LIFETIME", "5"))

    @property
    def users_cache_url(self) -> str:
        return f"redis://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.CACHE_DB}"


class Settings:
    mode: str = str(os.getenv("MODE", "PROD"))
    api_key: str = os.getenv("API_KEY", "secret")
    api: ApiPrefix = ApiPrefix()
    sql_db: SQLDatabaseConfig = SQLDatabaseConfig()
    redis: RedisConfig = RedisConfig()
    paths: Paths = Paths()


def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()  # Global settings instance.
