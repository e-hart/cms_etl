"""Command to remove columns from a DataFrame."""

from dataclasses import dataclass

from cms_etl.table.base_command import Command
from cms_etl.utils import console, get_cmd_args


@dataclass
class RemoveColumnCommand(Command):
    """Command to remove columns from a DataFrame."""

    cols: str | list[str]

    def __post_init__(self):
        self._cmd_args = get_cmd_args(self)
        # check if column(s) exist
        match self.cols:
            case str():
                if self.cols not in self.table.df.columns:
                    raise ValueError(f"Column '{self.cols}' does not exist.")
            case list():
                for col in self.cols:
                    if col not in self.table.df.columns:
                        raise ValueError(f"Column '{col}' does not exist.")

        self._og_data = self.table.df.copy(deep=True)

    def execute(self):
        """Execute the command."""
        self.table.df.drop(columns=self.cols, inplace=True)

    def undo(self):
        """Undo the command."""
        self.table.df = self._og_data
        console.print(f"Undone: {(self.serialize())}")
