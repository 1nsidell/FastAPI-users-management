from fastapi import APIRouter, Header

from src.app.depends import APIAccessProvider, UsersUseCase
from src.core.schemas import SAddInfoUser, SSuccessfulRequest
from src.settings import settings


class UserInfo:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.user,
            self.create_user,
            methods=["POST"],
            response_model=SSuccessfulRequest,
            status_code=201,
        )

    async def create_user(
        self,
        api_access: APIAccessProvider,
        user_info: SAddInfoUser,
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> SSuccessfulRequest:
        await api_access.check_api_key(api_key)
        await UsersUseCase.create_user(user_info)
        return SSuccessfulRequest()


user_info = UserInfo()

router = user_info.router
