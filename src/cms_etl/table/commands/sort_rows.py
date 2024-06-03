"""Command to sort a DataFrame by a column."""

import json
from dataclasses import dataclass, field

from cms_etl.table.base_command import Command
from cms_etl.utils import console, get_cmd_args


@dataclass
class SortRowsCommand(Command):
    """Command to sort a DataFrame by a column."""

    col_name: str
    ascending: bool = field(default=True)

    def __post_init__(self):
        self._cmd_args = get_cmd_args(self)
        self._og_df = self.table.df.copy(deep=True)

    def execute(self):
        """Execute the command."""
        self.table.df.sort_values(by=self.col_name, ascending=self.ascending, inplace=True)

    def undo(self):
        """Undo the command."""
        self.table.df = self._og_df.copy(deep=True)
        console.print(f"Undone: {json.dumps(self.serialize(), indent=4)}")
