from typing import ClassVar, Iterable

from sqlalchemy.orm import Session

from ..base.source import AbstractSource
from ..base.type import PayloadT
from .sqlalchemy_storage_box import (
    SQLAlchemyJsonStorageBox,
    SQLAlchemyPydanticStorageBox,
)
from .sqlalchemy_storage_box import SQLAlchemyStorageBoxMixin as SABox


class SQLAlchemyStorageBoxSource(AbstractSource[SABox[PayloadT]]):
    """A class that can fetch items through the default StorageBox"""

    def __init__(
        self,
        session: Session,
        orm_class: SQLAlchemyPydanticStorageBox
        | SQLAlchemyJsonStorageBox = SQLAlchemyPydanticStorageBox,
    ):
        self.session = session
        self.orm_class = orm_class

    def fetch_items(self, **kwargs) -> Iterable[SABox[PayloadT]]:
        """Return all message that have not been published and not failed"""
        return self.session.query(self.orm_class).filter(
            SABox.status == SABox.StatusEnum.WAITING
        )
