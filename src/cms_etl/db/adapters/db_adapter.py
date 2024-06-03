"""ABC for Database Interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal, Sequence

import pandas as pd
from sqlalchemy import Engine, Row, create_engine, exc

from cms_etl.db.adapters.config import DBConfig


@dataclass
class DatabaseAdapter[T: DBConfig](ABC):
    """Base Class for DatabaseAdapters.

    If you override the __post_init__ method in the concrete class,
    be sure to call super().__post_init__().

    ### Abstract methods to be implemented by DatabaseAdapters:
    - name: Return the name of the database.
    - list_tables: Return a list of tables in the database.
    - get_table_schema: Return the schema for a table.
    """

    _engine: Engine = field(init=False)
    _config: T = field(init=False)

    def __post_init__(self):
        self._engine = create_engine(str(self.config))
        try:
            self.test_connection()
        except exc.SQLAlchemyError as e:
            raise e

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the database."""

    @abstractmethod
    def list_tables(self) -> list[str]:
        """Return a list of tables in the database."""

    @abstractmethod
    def get_table_schema(self, table: str) -> Sequence[Row[Any]]:
        """Return the schema for a table."""

    @property
    def config(self) -> T:
        """Database configuration property."""
        return self._config

    @property
    def engine(self) -> Engine:
        """Database engine property."""
        return self._engine

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute a query."""
        return pd.read_sql(query, self.engine)

    def get_table(self, table: str) -> pd.DataFrame:
        """Return a DataFrame of the specified table."""
        return pd.read_sql_table(table, self.engine)

    def __getitem__(self, table: str) -> pd.DataFrame:
        """Return a DataFrame of the specified table."""
        return self.get_table(table)

    def df_to_table(
        self,
        df: pd.DataFrame,
        table: str,
        if_exists: Literal["replace", "fail"] = "fail",
        index: bool = False,
    ):
        """Write a DataFrame to a table in the database."""
        df.to_sql(table, self.engine, if_exists=if_exists, index=index)

    def test_connection(self):
        """Test the connection to the database."""
        try:
            connection = self.engine.connect()
            connection.close()
            return True
        except exc.SQLAlchemyError as e:
            raise e

    def close(self):
        """Dispose of the database engine."""
        self.engine.dispose()
        del self._engine
