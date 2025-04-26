from users_management.core.schemas import BaseSchema


class SInfoUser(BaseSchema):

    user_id: int
    nickname: str
    avatar: bool
