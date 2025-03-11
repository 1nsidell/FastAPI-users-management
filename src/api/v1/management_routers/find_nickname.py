from fastapi import APIRouter, Header, Path

from src.app.depends import APIAccessProvider, UsersUseCase
from src.core.schemas import SSuccessfulRequest
from src.settings import settings


class UserNickname:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            f"{settings.api.nicknames}/{{nickname}}",
            self.find_nickname,
            methods=["GET"],
            response_model=SSuccessfulRequest,
            status_code=200,
        )

    async def find_nickname(
        self,
        APIAccessProvider: APIAccessProvider,
        UsersUseCase: UsersUseCase,
        nickname: str = Path(...),
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> SSuccessfulRequest:
        APIAccessProvider.check_api_key(api_key)
        await UsersUseCase.find_user_by_nickname(nickname)
        return SSuccessfulRequest()


user_nickname = UserNickname()
router = user_nickname.router
