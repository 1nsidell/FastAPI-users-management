"""
ioc container for creating use cases.
"""

from typing import Annotated

from fastapi import Depends

from users_management.app.depends.services import UsersService
from users_management.app.use_cases import UsersUseCaseProtocol

from ..use_cases.impls.users import UsersUseCaseImpl


def get_users_use_case(
    users_service: UsersService,
) -> UsersUseCaseProtocol:
    return UsersUseCaseImpl(users_service=users_service)


UsersUseCase = Annotated[UsersUseCaseProtocol, Depends(get_users_use_case)]
