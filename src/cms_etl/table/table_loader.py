"""Load data from various sources into DataFrames."""

import datetime
import decimal
from typing import Optional

import pandas as pd
from sqlalchemy import inspect

from cms_etl.db import DBManager
from cms_etl.table.loaders import CMSSourceLoader
from cms_etl.utils import console


class TableLoader:
    """Load data from various sources (csv, db tables) into DataFrames"""

    def __init__(self, db_manager: Optional[DBManager] = None):
        self.db_mgr = db_manager
        self.cms_loader = CMSSourceLoader()

    def load_csv(self, path: str) -> pd.DataFrame:
        """Load a DataFrame from a CSV file."""
        return pd.read_csv(path)

    def load_from_db(self, table: str, db_key: str) -> pd.DataFrame | None:
        """Load a DataFrame from a database table."""
        e_str = f"Failed to load table '{table}' from database '{db_key}'."

        if self.db_mgr is None:
            console.log("A DBManager instance is required to load data from a database.")
            return None

        df = self.db_mgr[db_key].get_table(table)

        if df.empty:
            console.log(e_str)
            return None

        # validate/correct the data types of the columns
        df = self._validate_column_types(df, table, db_key)

        return df

    def _validate_column_types(self, df: pd.DataFrame, table: str, db_key: str):
        """Validate the data types of the columns"""
        if self.db_mgr is None:
            console.log(
                "A DBManager instance is required to validate the data types of the columns."
            )
            return df

        df = df.copy(deep=True)

        inspector = inspect(self.db_mgr[db_key].engine)
        columns = inspector.get_columns(table)

        for col in columns:
            if col["type"].python_type in (datetime.datetime, datetime.date):
                continue
            match col["type"].python_type():
                case str():
                    console.log(f"Converting column '{col['name']}' to string.")
                    df[col["name"]] = df[col["name"]].astype(pd.StringDtype())
                case int():
                    console.log(f"Converting column '{col['name']}' to integer.")
                    df[col["name"]] = df[col["name"]].astype(pd.Int64Dtype())
                case decimal.Decimal():
                    console.log(f"Converting column '{col['name']}' to float.")
                    df[col["name"]] = df[col["name"]].astype(pd.Float64Dtype())
                case bool():
                    console.log(f"Converting column '{col['name']}' to boolean.")
                    df[col["name"]] = df[col["name"]].astype(pd.BooleanDtype())
                case _:
                    console.log(
                        f"Column '{col['name']}' has an unsupported data type: {col['type'].python_type}"
                    )

        return df
