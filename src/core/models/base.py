from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.settings import settings
from src.core.models.utils.tablename_converter import tablename_converter


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=settings.db.naming_convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{tablename_converter(cls.__name__)}s"
