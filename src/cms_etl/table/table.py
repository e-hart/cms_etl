"""Table class for DataFrame manipulation."""

from typing import List, Optional

import pandas as pd

from cms_etl.table.command_manager import CommandManager


class Table:
    """DataFrame wrapper class."""

    def __init__(self, df: pd.DataFrame, name: str, description: Optional[str] = None, **metadata):
        self.__init_df = df.copy()
        self.__df = df
        self.name = name
        self.description = description
        self.cmd_manager = CommandManager(self)
        self.tmp_df_dict = dict()
        self.metadata = {}
        if metadata:
            for key, value in metadata.items():
                self.metadata[key] = value

    def list_columns(self) -> List[str]:
        """List the columns in the DataFrame."""
        return self.__df.columns.tolist()

    def list_commands(self) -> List[str]:
        """List the available commands."""
        return [cmd for cmd in dir(self.cmd_manager) if not cmd.startswith("_")]

    def reset_dataframe(self):
        """Reset the DataFrame to its initial state."""
        self.__df = self.__init_df.copy(deep=True)
        self.cmd_manager = CommandManager(self)

    @property
    def df(self) -> pd.DataFrame:
        """Return the DataFrame."""
        return self.__df

    @df.setter
    def df(self, new_df: pd.DataFrame):
        self.__df = new_df

    def __repr__(self):
        return f"\nTable(name={self.name}, description={self.description}\n{self.__df})"

    def __str__(self):
        return f"\nTable: {self.name}\nDescription: {self.description}\n{self.__df}"
