"""Database Manager"""

from typing import Dict, Optional

from sqlalchemy import Engine, exc

from cms_etl.db.adapter_factory import get_adapter
from cms_etl.db.adapters import DatabaseAdapter
from cms_etl.db.adapters.config import DBConfig
from cms_etl.utils import console


class DBManager:
    """Database Manager"""

    def __init__(self, db_config: Optional[DBConfig]) -> None:
        self._databases: Dict[str, DatabaseAdapter] = (
            {db_config.name: get_adapter(db_config)} if db_config else {}
        )

    def __getitem__(self, key: str) -> DatabaseAdapter:
        """Return the database interface for the specified connection."""
        return self._databases[key]

    def get_engine(self, key: str) -> Engine | None:
        """Return the engine for the specified connection."""
        if key not in self._databases:
            console.log(f"Database connection '{key}' not found.")
            return

        return self._databases[key].engine

    def add_db(self, key: str, db_cfg: DBConfig) -> None:
        """Add a new connection."""
        new_db = None
        try:
            new_db = get_adapter(db_cfg)
        except exc.SQLAlchemyError as e:
            console.log(f"Failed to add database: {e}")
            new_db = None
        except FileNotFoundError as e:
            console.log(f"Failed to add database: {e}")
            new_db = None

        if new_db is not None:
            self._databases[key] = new_db

    def remove_db(self, key: str) -> None:
        """Remove a connection."""
        try:
            if key in self._databases:
                self._databases[key].close()
                del self._databases[key]
        except exc.SQLAlchemyError as e:
            console.log(f"Failed to remove database: {e}")

    def list_dbs(self) -> list[str]:
        """Return a list of databases."""
        return list(self._databases.keys())

    def close(self):
        """Close all connections."""
        for db in self._databases.values():
            db.close()

    def __del__(self):
        self.close()
