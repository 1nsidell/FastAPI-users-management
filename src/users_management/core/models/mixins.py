import datetime

from sqlalchemy.orm import Mapped, mapped_column
from users_management.core.models.utils.to_utc_converter import to_utc_converter


class IntIdPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-100)


class CreatedTimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=to_utc_converter, sort_order=100
    )


class UpdatedTimestampMixin:
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=to_utc_converter,
        onupdate=to_utc_converter,
        sort_order=101,
    )
