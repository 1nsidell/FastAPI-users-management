from fastapi import APIRouter

from src.api.v1 import (
    create_user_router,
    delete_user_router,
    find_nickname_router,
    get_list_users_router,
    get_user_router,
    update_user_router,
)
from src.settings import settings

v1_router = APIRouter(
    prefix=settings.api.v1_prefix,
    tags=["USER-MANAGEMENT-V1"],
)

v1_sub_routers = (
    get_user_router,
    get_list_users_router,
    find_nickname_router,
    create_user_router,
    update_user_router,
    delete_user_router,
)

for router in v1_sub_routers:
    v1_router.include_router(router)
