from typing import Optional

from pydantic import BaseModel, PositiveInt


class SAddInfoUser(BaseModel):

    user_id: PositiveInt
    nickname: str
    role_id: Optional[int] = 1


class SSuccessfulRequest(BaseModel):
    message: str = "success"
