from fastapi import APIRouter, Header, Path

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.users import SInfoUser
from users_management.settings import settings

router = APIRouter()


@router.get(
    f"{settings.api.users}/{{user_id}}",
    response_model=SInfoUser,
    status_code=200,
)
async def get_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    user_id: int = Path(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> SInfoUser:
    api_access_provider.check_api_key(api_key)
    return await users_use_case.get_user_by_id(user_id)
