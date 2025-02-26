from src.app.use_cases import UsersUseCaseProtocol, UsersUseCaseImpl
from src.app.services import UsersServiceProtocol
from src.app.depends import UsersService


def get_users_use_case(users_service: UsersServiceProtocol) -> UsersUseCaseProtocol:
    return UsersUseCaseImpl(users_service)


UsersUseCase: UsersUseCaseProtocol = get_users_use_case(UsersService)
