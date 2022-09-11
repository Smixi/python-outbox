from abc import ABC, abstractmethod
from typing import Generic

from python_outbox.base.type import PublishableT


class AbstractPublisher(Generic[PublishableT], ABC):
    @abstractmethod
    def publish(self, item: PublishableT) -> None:
        """
        Take a publisher item and publish it to another system
        """
        pass


class PublishFailedException(Exception):
    pass
