from src.app.depends import UsersService
from src.app.services import UsersManagementServiceProtocol
from src.app.use_cases import UsersManagementUseCaseProtocol

from ..use_cases.impls.users_management_use_case import (
    UsersManagementUseCaseImpl,
)


def get_users_use_case(
    users_service: UsersManagementServiceProtocol,
) -> UsersManagementUseCaseProtocol:
    return UsersManagementUseCaseImpl(users_service)


UsersUseCase: UsersManagementUseCaseProtocol = get_users_use_case(UsersService)
