from sqlalchemy.orm import Mapped, mapped_column

from users_management.core.models.base import Base
from users_management.core.models.mixins import (
    CreatedTimestampMixin,
    UpdatedTimestampMixin,
)


class InfoUser(Base, CreatedTimestampMixin, UpdatedTimestampMixin):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(
        nullable=False, index=True, unique=True
    )
    avatar: Mapped[bool] = mapped_column(default=False, nullable=False)
