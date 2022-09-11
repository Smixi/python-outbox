from abc import ABC, abstractmethod
from typing import Generic

from python_outbox.base.type import PublisherT


class AbstractPublisher(Generic[PublisherT], ABC):
    @abstractmethod
    def publish(self, item: PublisherT) -> None:
        """
        Take a publisher item and publish it to another system
        """
        pass


class PublishFailedException(Exception):
    pass
