from ..base.mapper import AbstractMapper
from .sqlalchemy_storage_box import SQLAlchemyStorageBoxMixin as SABox


class SQLAlchemyStorageBoxMapper(AbstractMapper):
    """A class that can map a StorageBox item to its payload"""

    def convert(self, source: SABox):
        return source.pull()
