"""
Module describes the provider protocol for checking incoming requests.
"""

from abc import abstractmethod
from typing import Protocol, Self


class APIAccessProviderProtocol(Protocol):
    _valid_api_key: str

    @abstractmethod
    def check_api_key(self: Self, api_key: str) -> None: ...
