"""Utilities for working with DataFrames."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from cms_etl.table.table import Table


@dataclass
class Command(ABC):
    """Base class for commands."""

    table: Table
    _cmd_args: Dict[str, Any] = field(init=False, repr=False)

    def serialize(self):
        """Serialize the command."""
        return {
            "command": self.__class__.__name__,
            "args": self._cmd_args,
        }

    @abstractmethod
    def execute(self):
        """Execute the command."""

    @abstractmethod
    def undo(self):
        """Undo the command."""
