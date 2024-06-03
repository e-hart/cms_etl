"""Application context."""

from typing import Optional

from cms_etl.db import DBManager
from cms_etl.db.adapters.config import DBConfig
from cms_etl.menu import MenuController
from cms_etl.table.table_loader import TableLoader
from cms_etl.table.table_manager import TableManager


class AppContext:
    """Application context."""

    def __init__(self, db_cfg: Optional[DBConfig]):
        self.db_mgr = DBManager(db_cfg)
        self.data_loader = TableLoader(self.db_mgr)
        self.table_mgr = TableManager()
        self.menu_ctrlr = MenuController(self)
