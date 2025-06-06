from ..v1.management_routers.create_user import router as create_user_router
from ..v1.management_routers.delete_user import router as delete_user_router
from ..v1.management_routers.get_list_users import (
    router as get_list_users_router,
)
from ..v1.management_routers.get_user import router as get_user_router
from ..v1.management_routers.update_user import router as update_user_router
from .management_routers.exist_nickname import router as exist_nickname_router


__all__ = [
    "create_user_router",
    "delete_user_router",
    "exist_nickname_router",
    "get_list_users_router",
    "get_user_router",
    "update_user_router",
]
