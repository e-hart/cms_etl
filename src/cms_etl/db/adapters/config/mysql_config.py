"""MySQL Configuration/Credentials."""

from dataclasses import dataclass, field

from cms_etl.db.adapters.config import DBConfig


@dataclass(kw_only=True)
class MySQLConfig(DBConfig):
    """MySQL Configuration/Credentials Dataclass."""

    user: str
    password: str
    host: str
    port: int = field(default=3306)
    db_name: str

    @property
    def name(self) -> str:
        return self.db_name

    def __str__(self) -> str:
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
