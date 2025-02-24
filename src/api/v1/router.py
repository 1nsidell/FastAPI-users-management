from fastapi import APIRouter

from src.settings import settings

v1_router = APIRouter(
    prefix=settings.api.v1_prefix,
    tags=["USER-MANAGMENT-V1"],
)

v1_sub_routers = ()

for router in v1_sub_routers:
    v1_router.include_router(router)
