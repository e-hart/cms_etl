"""Command to find duplicate columns in a DataFrame."""

import json
from dataclasses import dataclass

from cms_etl.table.base_command import Command
from cms_etl.utils import console, get_cmd_args, isolate_addr_head


@dataclass
class FindColumnDuplicatesCommand(Command):
    """Command to find duplicate columns in a DataFrame."""

    col_name: str

    def __post_init__(self):
        self._cmd_args = get_cmd_args(self)
        self._og_df = self.table.df.copy(deep=True)

    def execute(self):
        """Execute the command."""
        self.table.df = self.table.df[
            self.table.df[self.col_name].apply(isolate_addr_head).duplicated(keep=False)
        ].copy(deep=True)

    def undo(self):
        """Undo the command."""
        self.table.df = self._og_df.copy(deep=True)
        console.print(f"Undone: {json.dumps(self.serialize(), indent=4)}")
