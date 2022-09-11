from ..base.mapper import AbstractMapper
from ..base.type import PublishableStorageT


class IdentityMapper(AbstractMapper):
    """A mapper that implemente the identity function and return the input item"""

    def convert(self, source: PublishableStorageT) -> PublishableStorageT:
        return source
