"""Command to add a column to a DataFrame."""

import json
from dataclasses import dataclass, field
from typing import Optional

from cms_etl.table.base_command import Command
from cms_etl.utils import console, get_cmd_args


@dataclass
class AddColumnCommand(Command):
    """Command to add a column to a DataFrame."""

    # MARK: - Command Setup
    col_name: str
    fill_value: str | int | float | bool
    after: Optional[str] = field(default=None, kw_only=True)
    before: Optional[str] = field(default=None, kw_only=True)

    def __post_init__(self):
        self._cmd_args = get_cmd_args(self)
        self._col_pos = (
            self.table.df.columns.get_loc(self.after or self.before)
            if self.after or self.before
            else None
        )

        if self._col_pos is not None and isinstance(self._col_pos, int):
            if self.after:
                self._col_pos += 1
        else:
            self._col_pos = None

    # MARK: - Command Execution
    def execute(self):
        """Execute the command."""
        if self._col_pos is None or not isinstance(self._col_pos, int):
            self.table.df[self.col_name] = self.fill_value
        else:
            self.table.df.insert(
                self._col_pos,
                self.col_name,
                self.fill_value,
            )

    # MARK: - Undo Method
    def undo(self):
        """Undo the command."""
        del self.table.df[self.col_name]
        console.print(f"Undone: {json.dumps(self.serialize(), indent=4)}")
