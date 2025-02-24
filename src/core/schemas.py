from typing import Optional

from pydantic import BaseModel, ConfigDict


class SAddInfoUser(BaseModel):
    model_config = ConfigDict(strict=True)

    user_id: int
    nickname: str
    role_id: Optional[int]


class SSuccessfulRequest(BaseModel):
    message: str = "success"
