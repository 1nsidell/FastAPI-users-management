from fastapi import APIRouter, Header

from src.app.depends import APIAccessProvider, UsersUseCase
from src.app.schemas.users import SInfoUser
from src.core.schemas import SAddInfoUser
from src.settings import settings


class UserInfo:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.users,
            self.create_user,
            methods=["POST"],
            response_model=SInfoUser,
            status_code=201,
        )

    async def create_user(
        self,
        APIAccessProvider: APIAccessProvider,
        UsersUseCase: UsersUseCase,
        user_info: SAddInfoUser,
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> SInfoUser:
        APIAccessProvider.check_api_key(api_key)
        return await UsersUseCase.create_user(user_info)


user_info = UserInfo()

router = user_info.router
