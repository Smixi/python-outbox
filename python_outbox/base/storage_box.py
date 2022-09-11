from typing import Generic, TypeVar

T = TypeVar("T")


class StorageBoxMixin(Generic[T]):
    """A class that can hold any generic type into its system into persistent storage"""

    def pull(self) -> T:
        raise NotImplementedError()

    def put(self, item: T) -> None:
        raise NotImplementedError()
