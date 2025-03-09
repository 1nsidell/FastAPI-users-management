"""
Schemes for response/request.
"""

from typing import Optional

from pydantic import BaseModel, PositiveInt


class SAddInfoUser(BaseModel):
    """Data for user creation."""

    user_id: PositiveInt
    nickname: str
    role_id: Optional[int] = 1


class SSuccessfulRequest(BaseModel):
    """Response on a successful request that does not require data."""

    message: str = "success"
