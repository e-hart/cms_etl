"""Command to rename a column in a DataFrame."""

import json
from dataclasses import dataclass

from cms_etl.table.base_command import Command
from cms_etl.utils import console, get_cmd_args


@dataclass
class RenameColumnCommand(Command):
    """Command to rename a column in a DataFrame."""

    old_name: str
    new_name: str

    def __post_init__(self):
        self._cmd_args = get_cmd_args(self)

    def execute(self):
        """Execute the command."""
        self.table.df.rename(columns={self.old_name: self.new_name}, inplace=True)

    def undo(self):
        """Undo the command."""
        self.table.df.rename(columns={self.new_name: self.old_name}, inplace=True)
        console.print(f"Undone: {json.dumps(self.serialize(), indent=4)}")
