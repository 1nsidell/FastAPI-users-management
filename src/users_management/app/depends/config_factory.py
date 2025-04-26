from typing import Annotated

from fastapi import Depends

from users_management.core.settings import RedisConfig, Settings, get_settings


SettingsService = Annotated[Settings, Depends(get_settings)]


def get_redis_config(settings: SettingsService) -> RedisConfig:
    return settings.redis


RedisConfigService = Annotated[RedisConfig, Depends(get_redis_config)]
