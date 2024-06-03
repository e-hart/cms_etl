"""Database Configuration Abstract Class."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class DBConfig(ABC):
    """Database Configuration."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the database name."""

    @abstractmethod
    def __str__(self) -> str:
        """Return the sqlalchemy connection string."""
