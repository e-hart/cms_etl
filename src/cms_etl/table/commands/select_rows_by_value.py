"""Command to select rows in a DataFrame."""

import json
from dataclasses import dataclass

from cms_etl.table.base_command import Command
from cms_etl.utils import console, get_cmd_args


@dataclass
class SelectRowsByValueCommand(Command):
    """Command to select rows in a DataFrame."""

    column: str
    value: str | int | float | bool

    def __post_init__(self):
        self._cmd_args = get_cmd_args(self)
        self._og_df = self.table.df.copy(deep=True)

    def execute(self):
        """Execute the command."""
        mask = self.table.df[self.column] != self.value
        self.table.df.drop(self.table.df[mask].index, inplace=True)

    def undo(self):
        """Undo the command."""
        self.table.df = self._og_df.copy(deep=True)
        console.print(f"Undone: {json.dumps(self.serialize(), indent=4)}")
