from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
from src.core.models.mixins import (
    CreatedTimestampMixin,
    UpdatedTimestampMixin,
)


class InfoUser(Base, CreatedTimestampMixin, UpdatedTimestampMixin):

    user_id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.role_id", ondelete="SET NULL"),
        nullable=False,
        default=1,
    )
    nickname: Mapped[str] = mapped_column(
        nullable=False, index=True, unique=True
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    avatar: Mapped[bool] = mapped_column(default=False, nullable=False)

    role: Mapped["Role"] = relationship(back_populates="users")


class Role(Base):

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(unique=True, nullable=False)

    users: Mapped[List["InfoUser"]] = relationship(
        back_populates="role", cascade="all, delete"
    )
