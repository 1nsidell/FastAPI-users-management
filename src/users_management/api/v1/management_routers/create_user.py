from fastapi import APIRouter, Header

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.users import SInfoUser
from users_management.core.schemas import SAddInfoUser
from users_management.settings import settings

router = APIRouter()


@router.post(settings.api.users, response_model=SInfoUser, status_code=201)
async def create_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    user_info: SAddInfoUser,
    api_key: str = Header(..., alias="X-API-Key"),
) -> SInfoUser:
    api_access_provider.check_api_key(api_key)
    return await users_use_case.create_user(user_info)
