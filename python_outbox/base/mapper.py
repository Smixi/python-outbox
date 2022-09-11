from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

from .type import PublishableStorageT, PublishableT


class AbstractMapper(Generic[PublishableStorageT, PublishableT], ABC):
    @abstractmethod
    def convert(self, source: PublishableStorageT) -> PublishableT:
        """Return the converted item from source"""
        pass
