from pydantic import PositiveInt

from users_management.core.schemas.base import BaseSchema


class CreateUserRequest(BaseSchema):
    """The schema of the user creation request."""

    user_id: PositiveInt
    nickname: str
