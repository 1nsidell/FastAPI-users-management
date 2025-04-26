"""
Module describing the interface for interacting with the cache repository.
"""

from abc import abstractmethod
from typing import List, Optional, Protocol, Self, TypeVar


T = TypeVar("T")


class CacheRepositoryProtocol(Protocol[T]):
    @abstractmethod
    async def add(self: Self, key: str, data: T) -> None: ...

    @abstractmethod
    async def delete(self: Self, key: str) -> None: ...

    @abstractmethod
    async def get(self: Self, key: str) -> Optional[T]: ...

    @abstractmethod
    async def add_list(self, data_list: List[T]) -> None: ...

    @abstractmethod
    async def get_list(
        self,
        keys: List[str],
    ) -> Optional[List[T]]: ...
