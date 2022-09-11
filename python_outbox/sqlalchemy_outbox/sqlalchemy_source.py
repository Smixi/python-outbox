from typing import Iterable

from sqlalchemy.orm import Session

from ..base.source import AbstractSource
from .sqlalchemy_storage_box import SQLAlchemyStorageBoxMixin as SABox


class SQLAlchemyPydanticStorageBoxSource(AbstractSource):
    """A class that can fetch items through the default StorageBox"""

    def __init__(self, session: Session):
        self.session = session

    def fetch_items(self, **kwargs) -> Iterable[SABox]:
        """Return all message that have not been published and not failed"""
        return self.session.query(SABox).filter(
            SABox.status == SABox.StatusEnum.WAITING
        )
