from src.app.exceptions import CustomAccessDeniedException

from typing import Protocol, Self
from abc import abstractmethod


class APIAccessProviderProtocol(Protocol):

    @abstractmethod
    async def check_api_key(self: Self, api_key: str): ...


class APIAccessProviderImpl(APIAccessProviderProtocol):

    @staticmethod
    async def check_api_key(valid_api_key: str, api_key: str):
        if api_key != valid_api_key:
            raise CustomAccessDeniedException()
