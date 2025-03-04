from fastapi import APIRouter, Header

from src.app.depends import APIAccessProvider, UsersUseCase
from src.settings import settings


class UserInfo:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.users,
            self.delete_user,
            methods=["DELETE"],
            response_model=None,
            status_code=204,
        )

    async def delete_user(
        self,
        APIAccessProvider: APIAccessProvider,
        UsersUseCase: UsersUseCase,
        user_id: int,
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> None:
        APIAccessProvider.check_api_key(api_key)
        await UsersUseCase.delete_user(user_id)


user_info = UserInfo()

router = user_info.router
