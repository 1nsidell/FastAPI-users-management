from pydantic import BaseModel, ConfigDict


class SInfoUser(BaseModel):
    model_config = ConfigDict(strict=True)

    user_id: int
    nickname: str
    role: str
    is_active: bool
    is_verified: bool
    avatar: bool
