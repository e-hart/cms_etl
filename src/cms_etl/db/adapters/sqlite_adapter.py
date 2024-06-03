"""SQLite adapter."""

import os
from dataclasses import dataclass

from sqlalchemy import text

from cms_etl.db.adapters import DatabaseAdapter
from cms_etl.db.adapters.config import SQLiteConfig


@dataclass
class SQLiteAdapter(DatabaseAdapter):
    """SQLite adapter class."""

    _config: SQLiteConfig

    def __post_init__(self):
        if not os.path.exists(self.config.file_path) and self.config.if_not_exists == "error":
            raise FileNotFoundError(
                f"File {self.config.file_path} does not exist. "
                "If you are trying to create a new database, "
                "set if_not_exists='create' when creating the adapter."
            )
        super().__post_init__()

    @property
    def name(self) -> str:
        """Return the name of the database."""
        return self.config.name

    def list_tables(self) -> list[str]:
        """Return a list of tables in the database."""
        with self.engine.connect() as c:
            return [
                t[0]
                for t in c.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table';")
                ).fetchall()
            ]

    def get_table_schema(self, table: str):
        """Return the schema for a table."""
        with self.engine.connect() as c:
            return c.execute(text(f"PRAGMA table_info({table})")).fetchall()
