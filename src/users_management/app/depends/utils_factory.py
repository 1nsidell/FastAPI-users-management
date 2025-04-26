from typing import Annotated, Callable

from fastapi import Depends

from users_management.gateways.key_builders import get_key_by_user_id


def get_key_by_user_id_builder() -> Callable[[int], str]:
    return get_key_by_user_id


KeyByUserIdBuilder = Annotated[
    Callable[[int], str], Depends(get_key_by_user_id_builder)
]
