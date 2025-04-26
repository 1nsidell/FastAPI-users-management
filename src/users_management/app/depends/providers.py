"""
ioc container for creating providers.
"""

from typing import Annotated

from fastapi import Depends

from users_management.app.depends.config_factory import SettingsService
from users_management.app.providers import APIAccessProviderProtocol
from users_management.app.providers.impls.api_access import (
    APIAccessProviderImpl,
)


def get_api_access_provider(
    settings: SettingsService,
) -> APIAccessProviderProtocol:
    return APIAccessProviderImpl(settings.api_key)


APIAccessProvider = Annotated[
    APIAccessProviderProtocol, Depends(get_api_access_provider)
]
