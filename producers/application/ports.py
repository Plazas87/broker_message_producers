

from abc import ABC, abstractmethod
from typing import Generator, Generic, TypeVar

T = TypeVar("T")
V = TypeVar("V")


class IReader(ABC, Generic[T]):
    """Reader interface."""

    @abstractmethod
    def read(self) -> Generator[T, None, None]:
        """Create a generator over the data source."""


class ISerializer(ABC, Generic[T, V]):
    """Serializer interface."""

    @abstractmethod
    def serialize(self, data: T) -> V:
        """Serialize data."""


class IProducer(ABC):
    """IProducer interface."""

    @abstractmethod
    def publish(self) -> None:
        """Publish messages to a Broker."""