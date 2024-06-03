"""Manage Tables menu module."""

import warnings

from pandasgui import show

from cms_etl.menu import BaseMenu, MenuOption
from cms_etl.utils import console


class ManageTablesMenu(BaseMenu):
    """Manage Tables menu."""

    # MARK: - Menu Setup
    def _set_options(self):
        base_options = [
            MenuOption(name="Add Table", action=self.add_table),
        ]

        additional_options = [
            MenuOption(name="Remove Table", action=self.remove_table),
            MenuOption(name="List Tables", action=self.list_tables),
            MenuOption(name="View Table in Console", action=self.view_table_in_console),
            MenuOption(name="Open in Viewer", action=self.open_in_viewer),
            MenuOption(name="Edit Table", action=self.edit_table),
            MenuOption(name="Compare/Match Tables", action=self.compare_tables),
        ]
        back = [MenuOption(name="Back", action=self.back)]

        if self.ctx.table_mgr.list_tables():
            self.options = base_options + additional_options + back
        else:
            self.options = base_options + back

    # MARK: - Menu Actions
    def add_table(self):
        """Add a Table to the TableManager."""
        self.ctx.menu_ctrlr.open_menu(self.menus.load_data, "Load Data")

    def edit_table(self):
        """Edit a Table in the TableManager."""
        name = self._choose_table()
        if name:
            self.ctx.menu_ctrlr.open_menu(
                self.menus.edit_table, f"Edit Table: {name}", self._get_table(name)
            )

    def remove_table(self):
        """Remove a Table from the TableManager."""
        name = self._choose_table()
        if name:
            self.ctx.table_mgr.remove_table(name)
            console.print(f"Table '{name}' removed.")

    def list_tables(self):
        """List the names of the loaded Tables."""
        console.rule("[bold blue]Tables")
        for i, table in enumerate(self.ctx.table_mgr.list_tables(), start=1):
            console.print(f"{i}• [blue]{table.name}[/blue]{f": {table.description}" or ''}")

    def _get_table(self, name: str):
        """Get a Table from the TableManager."""
        return self.ctx.table_mgr.get_table(name)

    def compare_tables(self):
        """Select Tables for Comparison."""
        self.ctx.menu_ctrlr.open_menu(self.menus.compare_tables, "Select Tables for Comparison")

    def _choose_table(self) -> str | None:
        """Select a Table from the TableManager."""
        self.list_tables()
        tables = self.ctx.table_mgr.list_tables()
        print("\n")
        try:
            index = console.input("Enter index of table: ")
            name = list(tables)[int(index) - 1].name
            return name
        except (IndexError, ValueError):
            console.print("Invalid choice.")
        return None

    # MARK: - View Actions
    def view_table_in_console(self):
        """View a Table from the TableManager."""
        table_name = self._choose_table()
        if table_name:
            console.print(f"\n{self._get_table(table_name)}")

    def open_in_viewer(self):
        """View a Table from the TableManager in the DataFrame Viewer."""
        t_name = self._choose_table()
        if not t_name:
            return
        table = self._get_table(t_name)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            show(table.df)
