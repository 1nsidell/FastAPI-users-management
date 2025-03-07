from abc import abstractmethod
from typing import Any, Dict, List, Optional, Protocol, Self


class CacheRepositoryProtocol(Protocol):
    @abstractmethod
    async def add_user(self: Self, key: str, data: Dict[Any, Any]) -> None: ...

    @abstractmethod
    async def delete_user(self: Self, key: str) -> None: ...

    @abstractmethod
    async def get_user(self: Self, key: str) -> Any: ...

    @abstractmethod
    async def add_list_users(
        self,
        keys: List[str],
        data_list: List[Dict],
    ) -> None: ...

    @abstractmethod
    async def get_list_users(self, keys: List[str]) -> Optional[List[Dict]]: ...

    @abstractmethod
    async def delete_list_users(self, keys: List[str]) -> None: ...
