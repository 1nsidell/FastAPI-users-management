from fastapi import APIRouter, Header, Path

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.settings import settings

router = APIRouter()


@router.delete(f"{settings.api.users}/{{user_id}}", status_code=204)
async def delete_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    user_id: int = Path(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> None:
    api_access_provider.check_api_key(api_key)
    await users_use_case.delete_user(user_id)
