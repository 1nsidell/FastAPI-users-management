from fastapi import APIRouter

from src.api.health_check import liveness_router, readiness_router
from src.settings import settings

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
