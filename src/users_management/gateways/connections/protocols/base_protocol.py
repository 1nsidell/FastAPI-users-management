from abc import abstractmethod
from typing import Protocol, TypeVar


T_co = TypeVar("T_co", covariant=True)


class GatewayConnectionProtocol(Protocol[T_co]):

    @abstractmethod
    def startup(self) -> None: ...

    @abstractmethod
    def get_connection(self) -> T_co: ...

    @abstractmethod
    async def shutdown(self) -> None: ...
