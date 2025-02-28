from fastapi import APIRouter, Header

from src.app.depends import APIAccessProvider, UsersUseCase
from src.app.schemas.users import SInfoUser
from src.settings import settings


class UserInfo:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.user,
            self.get_user,
            methods=["GET"],
            response_model=SInfoUser,
            status_code=200,
        )

    async def get_user(
        self,
        user_id: int,
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> SInfoUser:
        APIAccessProvider.check_api_key(api_key)
        return await UsersUseCase.get_user(user_id)


user_info = UserInfo()

router = user_info.router
