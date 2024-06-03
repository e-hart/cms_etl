"""MySQL Adapter."""

from dataclasses import dataclass

from sqlalchemy import text

from cms_etl.db.adapters import DatabaseAdapter
from cms_etl.db.adapters.config import MySQLConfig


@dataclass
class MySQLAdapter(DatabaseAdapter):
    """MySQL Adapter class."""

    _config: MySQLConfig

    @property
    def name(self) -> str:
        """Return the name of the database."""
        return self.config.db_name

    def list_tables(self) -> list[str]:
        """Return a list of tables in the database."""
        with self.engine.connect() as c:
            return [t[0] for t in c.execute(text("SHOW TABLES")).fetchall()]

    def get_table_schema(self, table: str):
        """Return the schema for a table."""
        with self.engine.connect() as c:
            return c.execute(text(f"DESCRIBE {table}")).fetchall()
