from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from src.core.models.base import Base
from src.core.models.mixins import (
    CreatedTimestampMixin,
    IntIdPkMixin,
    UpdatedTimestampMixin,
)


class InfoUser(Base, IntIdPkMixin, CreatedTimestampMixin, UpdatedTimestampMixin):

    user_id: Mapped[int] = mapped_column(unique=True, nullable=False, index=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="SET NULL"),
        nullable=True,
        default=1,
    )
    nickname: Mapped[str] = mapped_column(nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    avatar: Mapped[bool] = mapped_column(default=False, nullable=False)

    role: Mapped["Role"] = relationship(back_populates="users")


class Role(Base, IntIdPkMixin):

    role: Mapped[str] = mapped_column(unique=True, nullable=False)

    users: Mapped[List["InfoUser"]] = relationship(
        back_populates="role", cascade="all, delete"
    )
