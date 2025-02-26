from fastapi import APIRouter

from src.api.v1.routers.create_user import router as create_user_router
from src.api.v1.routers.get_user import router as get_user_router
from src.api.v1.routers.update_user import router as update_user_router
from src.api.v1.routers.delete_user import router as delete_user_router
from src.settings import settings

v1_router = APIRouter(
    prefix=settings.api.v1_prefix,
    tags=["USER-MANAGEMENT-V1"],
)

v1_sub_routers = (
    create_user_router,
    get_user_router,
    update_user_router,
    delete_user_router,
)

for router in v1_sub_routers:
    v1_router.include_router(router)
