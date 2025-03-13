"""
ioc container for creating use cases.
"""

from typing import Annotated

from fastapi import Depends

from src.app.depends.services import UsersService
from src.app.use_cases import UsersManagementUseCaseProtocol

from ..use_cases.impls.users_management import (
    UsersManagementUseCaseImpl,
)


def get_users_use_case(
    users_service: UsersService,
) -> UsersManagementUseCaseProtocol:
    return UsersManagementUseCaseImpl(users_service)


UsersUseCase = Annotated[
    UsersManagementUseCaseProtocol, Depends(get_users_use_case)
]
