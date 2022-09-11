from abc import ABC, abstractmethod
from typing import Generic

from .mapper import AbstractMapper
from .publisher import AbstractPublisher
from .source import AbstractSource
from .type import PublishableT, PublisherT


class AbstractProducer(Generic[PublishableT, PublisherT], ABC):
    def __init__(
        self,
        source: AbstractSource,
        mapper: AbstractMapper[PublishableT, PublisherT],
        publisher: AbstractPublisher,
    ) -> None:
        self.source = source
        self.mapper = mapper
        self.publisher = publisher
        super().__init__()

    @abstractmethod
    def produce(self) -> int:
        """
        Fetch items from the source and publish them to any sink, return the number of published items.
        """
        pass
