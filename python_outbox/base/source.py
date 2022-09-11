from abc import ABC, abstractmethod
from typing import Generic, Iterable

from .type import PublishableT


class AbstractSource(Generic[PublishableT], ABC):
    "The Source class is used to retrieve any publishable from a persistent storage that are not yet produced"

    @abstractmethod
    def fetch_items(self, **kwargs) -> Iterable[PublishableT]:
        pass
