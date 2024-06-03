"""Command to convert a column to title case."""

import json
from dataclasses import dataclass

from titlecase import titlecase

from cms_etl.table.base_command import Command
from cms_etl.utils import console, get_cmd_args


@dataclass
class ColumnToTitleCaseCommand(Command):
    """Command to convert a column to title case."""

    col_name: str

    def __post_init__(self):
        self._cmd_args = get_cmd_args(self)
        if self.table.df[self.col_name].dtype.kind not in "OSU":
            console.print("Column values must be of type string, unicode, or object.")
            raise ValueError
        self._og_col = self.table.df[self.col_name].copy(deep=True)

    def execute(self):
        """Execute the command."""
        self.table.df[self.col_name] = self.table.df[self.col_name].apply(titlecase)

    def undo(self):
        """Undo the command."""
        self.table.df[self.col_name] = self._og_col
        console.print(f"Undone: {json.dumps(self.serialize(), indent=4)}")
