from typing import Any, Dict

from fastapi import APIRouter, Header

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.users import SInfoUser
from users_management.settings import settings


class UserInfo:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.users,
            self.update_user,
            methods=["PATCH"],
            response_model=SInfoUser,
            status_code=200,
        )

    async def update_user(
        self,
        APIAccessProvider: APIAccessProvider,
        UsersUseCase: UsersUseCase,
        user_id: int,
        user_info: Dict[str, Any],
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> SInfoUser:
        APIAccessProvider.check_api_key(api_key)
        return await UsersUseCase.update_user(user_id, user_info)


user_info = UserInfo()

router = user_info.router
