from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr
from users_management.core.models.utils.tablename_converter import (
    tablename_converter,
)
from users_management.settings import settings


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=settings.sql_db.naming_convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{tablename_converter(cls.__name__)}s"
