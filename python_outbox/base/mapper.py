from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

from .type import PublishableT, PublisherT


class AbstractMapper(Generic[PublishableT, PublisherT], ABC):
    @abstractmethod
    def convert(self, source: PublishableT) -> PublisherT:
        """Return the converted item from source"""
        pass
