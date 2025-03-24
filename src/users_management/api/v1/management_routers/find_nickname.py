from fastapi import APIRouter, Header, Path

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.core.schemas import SSuccessfulRequest
from users_management.settings import settings

router = APIRouter()


@router.get(
    f"{settings.api.nicknames}/{{nickname}}",
    response_model=SSuccessfulRequest,
    status_code=200,
)
async def find_nickname(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    nickname: str = Path(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> SSuccessfulRequest:
    api_access_provider.check_api_key(api_key)
    await users_use_case.find_user_by_nickname(nickname)
    return SSuccessfulRequest()
