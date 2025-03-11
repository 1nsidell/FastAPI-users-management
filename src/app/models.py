from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base
from src.core.models.mixins import (
    CreatedTimestampMixin,
    UpdatedTimestampMixin,
)


class InfoUser(Base, CreatedTimestampMixin, UpdatedTimestampMixin):

    user_id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(
        nullable=False, index=True, unique=True
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    avatar: Mapped[bool] = mapped_column(default=False, nullable=False)
