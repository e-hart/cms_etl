"""Command to set the type of a column in a DataFrame."""

import json
from dataclasses import dataclass

from cms_etl.table.base_command import Command
from cms_etl.utils import console, get_cmd_args, get_dtype_obj


@dataclass
class SetColumnTypeCommand(Command):
    """Command to set the type of a column in a DataFrame."""

    col_name: str
    col_type: str

    def __post_init__(self):
        self._cmd_args = get_cmd_args(self)
        self._dtype = get_dtype_obj(self.col_type)
        self._og_col = self.table.df[self.col_name].copy(deep=True)

    def execute(self):
        """Execute the command."""
        self.table.df[self.col_name] = self.table.df[self.col_name].astype(self._dtype)

    def undo(self):
        """Undo the command."""
        self.table.df[self.col_name] = self._og_col.copy(deep=True)
        console.print(f"Undone: {json.dumps(self.serialize(), indent=4)}")
