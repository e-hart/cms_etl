"""Manage Database Connections menu."""

from sqlalchemy import exc

from cms_etl.db.adapters.config import MySQLConfig
from cms_etl.db.adapters.config.sqlite_config import SQLiteConfig
from cms_etl.menu import BaseMenu, MenuOption
from cms_etl.utils import Pick, console, prompt_mysql_config, prompt_sqlite_config, select_from_list


class ManageDatabasesMenu(BaseMenu):
    """Manage Database Connections menu."""

    def _set_options(self):
        self.options = [
            MenuOption(name="Add Connection", action=self.add_database),
            MenuOption(name="Remove Connection", action=self.remove_database),
            MenuOption(name="List Connections", action=self.list_databases),
            MenuOption(name="Back", action=self.back),
        ]

    def add_database(self):
        """Add a DB"""
        db_types = ["MySQL", "SQLite"]
        console.print("Add Database Connection")
        key = console.input("Enter name for Database: ")

        db_type = select_from_list(Pick.one, db_types, title="Select Database Type")
        db_config = None
        if db_type == "MySQL":
            db_config = MySQLConfig(**prompt_mysql_config())
        if db_type == "SQLite":
            db_config = SQLiteConfig(**prompt_sqlite_config())
        if db_config is None or db_type not in db_types:
            console.print("Invalid database type.")
            return
        try:
            self.ctx.db_mgr.add_db(key, db_config)
        except exc.SQLAlchemyError as e:
            console.log(f"Failed to add connection: {e}")

    def list_databases(self):
        """List connected databases."""
        self.clear()
        console.rule("Databases")
        for db in self.ctx.db_mgr.list_dbs():
            console.print(f"[blue]•[/blue] {db}")

    def remove_database(self):
        """Remove a DB"""
        console.rule("[bold red]Remove Connection")
        self.list_databases()
        key = console.input("Enter key for connection: ")
        try:
            self.ctx.db_mgr.remove_db(key)
        except KeyError:
            console.print(f"Connection '{key}' not found.")
        else:
            console.print(f"Connection '{key}' removed successfully.")
