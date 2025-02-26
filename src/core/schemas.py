from typing import Optional

from pydantic import BaseModel, ConfigDict


class SAddInfoUser(BaseModel):

    user_id: int
    nickname: str
    role_id: Optional[int] = 1


class SSuccessfulRequest(BaseModel):
    message: str = "success"
