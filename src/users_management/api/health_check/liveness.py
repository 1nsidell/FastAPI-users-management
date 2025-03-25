from fastapi import APIRouter

from users_management.core.schemas import SSuccessfulRequest
from users_management.settings import settings

router = APIRouter()


@router.get(
    settings.api.liveness,
    response_model=SSuccessfulRequest,
    status_code=200,
)
async def get_liveness() -> SSuccessfulRequest:
    return SSuccessfulRequest()
