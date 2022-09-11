from ..base.mapper import AbstractMapper
from ..base.type import PayloadT, PublishableT
from .sqlalchemy_storage_box import SQLAlchemyStorageBoxMixin as SABox


class SQLAlchemyStorageBoxMapper(AbstractMapper[SABox[PayloadT], PayloadT]):
    """A class that can map a StorageBox item to its payload"""

    def convert(self, source: SABox[PayloadT]) -> PayloadT:
        return source.pull()
