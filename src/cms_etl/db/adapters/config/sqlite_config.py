"""SQLite Connection Configuration"""

from dataclasses import dataclass, field

from cms_etl.db.adapters.config import DBConfig


@dataclass(kw_only=True)
class SQLiteConfig(DBConfig):
    """SQLite Configuration/Credentials Dataclass."""

    file_path: str
    if_not_exists: str = field(default="error")

    @property
    def name(self) -> str:
        return self.file_path.split("/")[-1]

    def __str__(self) -> str:
        return f"sqlite+pysqlite:///{self.file_path}"
