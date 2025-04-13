from fastapi import APIRouter

from users_management.api.http.health_check import (
    liveness_router,
    readiness_router,
)
from users_management.core.settings import settings

healthcheck_router = APIRouter(
    prefix=settings.api.healthcheck,
    tags=["HEALTH-CHECK"],
)

healthcheck_router_sub_routers = (
    liveness_router,
    readiness_router,
)

for router in healthcheck_router_sub_routers:
    healthcheck_router.include_router(router)
