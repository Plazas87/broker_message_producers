"""Data readers package."""

from abc import ABC, abstractmethod
from typing import Generator, Generic, TypeVar

T = TypeVar("T")
V = TypeVar("V")


class IReader(ABC, Generic[T]):
    """Reader interface."""

    @abstractmethod
    def read(self) -> Generator[T, None, None]:
        """Create a generator over the data source."""
