"""Manage Tables."""

from typing import Dict

import pandas as pd

from cms_etl.table.table import Table
from cms_etl.utils import console


class TableManager:
    """Manage Tables"""

    def __init__(self):
        self.tables: Dict[str, Table] = {}

    def add_table(self, df: pd.DataFrame, table_name: str, description: str = "", **kwargs):
        """Add a DataFrame to the manager."""
        self.tables[table_name] = Table(df, table_name, description, **kwargs)
        return self.tables[table_name]

    def remove_table(self, name: str):
        """Remove a DataFrame from the manager."""
        del self.tables[name]

    def list_tables(self):
        """List the names of the managed DataFrames."""
        return self.tables.values()

    def get_table(self, name: str):
        """Get a Table from the manager."""
        return self.tables[name]

    def view_dataframe(self, name: str):
        """View a DataFrame from the manager."""
        console.print(self.tables[name].df)
