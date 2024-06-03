"""Adapter Factory Module"""

from cms_etl.db.adapters import DatabaseAdapter, MySQLAdapter, SQLiteAdapter
from cms_etl.db.adapters.config import DBConfig, MySQLConfig, SQLiteConfig


def get_adapter(config: DBConfig) -> DatabaseAdapter:
    """Return the appropriate database adapter."""
    match config:
        case MySQLConfig():
            return MySQLAdapter(config)
        case SQLiteConfig():
            return SQLiteAdapter(config)
        case _:
            raise ValueError("Invalid database configuration.")
