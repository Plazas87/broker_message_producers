"""Serializers package."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
V = TypeVar("V")


class ISerializer(ABC, Generic[T, V]):
    """Serializer interface."""

    @abstractmethod
    def serialize(self, data: T) -> V:
        """Serialize data."""
