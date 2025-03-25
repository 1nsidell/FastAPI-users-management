from typing import List

from fastapi import APIRouter, Header, Query
from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.users import SInfoUser
from users_management.settings import settings

router = APIRouter()


@router.get(settings.api.users, response_model=List[SInfoUser], status_code=200)
async def get_list_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    users_id: List[int] = Query(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> List[SInfoUser]:
    api_access_provider.check_api_key(api_key)
    return await users_use_case.get_list_users_by_id(users_id)
