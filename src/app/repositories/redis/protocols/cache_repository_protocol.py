from typing import Protocol, Dict, Any, Self
from abc import abstractmethod


class CacheRepositoryProtocol(Protocol):
    @abstractmethod
    async def add(self: Self, key: Any, data: Dict[Any, Any]) -> None: ...

    @abstractmethod
    async def delete(self: Self, key: Any) -> bool: ...

    @abstractmethod
    async def get(self: Self, key: Any) -> Any: ...

    @abstractmethod
    async def close(self: Self) -> None: ...
