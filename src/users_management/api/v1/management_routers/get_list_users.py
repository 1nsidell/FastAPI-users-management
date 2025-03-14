from fastapi import APIRouter, Header, Query

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.users import SInfoUser
from users_management.settings import settings


class ListUserInfo:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.users,
            self.get_list_user,
            methods=["GET"],
            response_model=list[SInfoUser],
            status_code=200,
        )

    async def get_list_user(
        self,
        APIAccessProvider: APIAccessProvider,
        UsersUseCase: UsersUseCase,
        users_id: list[int] = Query(...),
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> list[SInfoUser]:
        APIAccessProvider.check_api_key(api_key)
        return await UsersUseCase.get_list_users_by_id(users_id)


list_user_info = ListUserInfo()
router = list_user_info.router
