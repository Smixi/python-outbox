from ..base.mapper import AbstractMapper
from ..base.type import PublishableT


class IdentityMapper(AbstractMapper):
    """A mapper that implemente the identity function and return the input item"""

    def convert(self, source: PublishableT) -> PublishableT:
        return source
