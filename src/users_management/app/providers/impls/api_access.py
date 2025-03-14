"""Module describes the provider implementation for checking incoming requests."""

import logging
from typing import Self

from users_management.app.exceptions import AccessDeniedException
from users_management.app.providers import APIAccessProviderProtocol

log = logging.getLogger("app")


class APIAccessProviderImpl(APIAccessProviderProtocol):
    def __init__(self: Self, valid_api_key: str):
        self.valid_api_key = valid_api_key

    def check_api_key(self: Self, api_key: str) -> None:
        if api_key != self.valid_api_key:
            raise AccessDeniedException()
        log.debug("API key successfully verified.")
