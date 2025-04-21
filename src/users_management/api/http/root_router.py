from fastapi import APIRouter

from users_management.api.http.health_check.router import healthcheck_router
from users_management.api.http.v1.router import v1_router
from users_management.core.settings import settings


root_router = APIRouter(prefix=settings.api.prefix)

root_sub_routers = (
    healthcheck_router,
    v1_router,
)

for router in root_sub_routers:
    root_router.include_router(router)
