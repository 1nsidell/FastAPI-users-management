from src.app.depends import UsersService
from src.app.services import UsersServiceProtocol
from src.app.use_cases import UsersUseCaseImpl, UsersUseCaseProtocol


def get_users_use_case(
    users_service: UsersServiceProtocol,
) -> UsersUseCaseProtocol:
    return UsersUseCaseImpl(users_service)


UsersUseCase: UsersUseCaseProtocol = get_users_use_case(UsersService)
