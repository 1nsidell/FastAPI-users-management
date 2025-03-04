from fastapi import APIRouter

from src.core.schemas import SSuccessfulRequest
from src.settings import settings


class Liveness:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.liveness,
            self.get_liveness,
            methods=["GET"],
            response_model=SSuccessfulRequest,
            status_code=200,
        )

    async def get_liveness(
        self,
    ) -> SSuccessfulRequest:
        return SSuccessfulRequest()


liveness = Liveness()

router = liveness.router
