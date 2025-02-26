import os
from pathlib import Path
from typing import Dict
from pydantic import BaseModel
from sqlalchemy import URL


# ----------------------------- BaseProjectConfig -----------------------------
ROOT_DIR_SRC: Path = Path(__file__).parent


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiPrefix(BaseModel):
    healthcheck: str = "/healthcheck"
    prefix: str = "/api/user-management"
    v1_prefix: str = "/v1"
    user: str = "/user"


class DatabaseConfig(BaseModel):
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
    HOST: str = os.getenv("REDIS_HOST")
    PORT: str = os.getenv("REDIS_PORT")
    TOKEN_DB: str = os.getenv("REDIS_TOKEN_DB")
    CACHE_DB: str = os.getenv("REDIS_CACHE_DB")
    PASSWORD: str = os.getenv("REDIS_PASSWORD")

    @property
    def token_url(self) -> str:
        return f"redis://:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.TOKEN_DB}"

    @property
    def cache_url(self) -> str:
        return f"redis://:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.CACHE_DB}"


class Settings:
    api_key: str = os.getenv("API_KEY")
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()
    kv_repository: RedisConfig = RedisConfig()


def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
