from fastapi import APIRouter, Header, Path

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.users import SInfoUser
from users_management.settings import settings


class UserInfo:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            f"{settings.api.users}/{{user_id}}",
            self.get_user,
            methods=["GET"],
            response_model=SInfoUser,
            status_code=200,
        )

    async def get_user(
        self,
        APIAccessProvider: APIAccessProvider,
        UsersUseCase: UsersUseCase,
        user_id: int = Path(...),
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> SInfoUser:
        APIAccessProvider.check_api_key(api_key)
        return await UsersUseCase.get_user_by_id(user_id)


user_info = UserInfo()
router = user_info.router
