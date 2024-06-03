"""Main menu for the interactive environment."""

import sys

from cms_etl.menu import BaseMenu, MenuOption
from cms_etl.utils import console


class MainMenu(BaseMenu):
    """Main menu."""

    # MARK: - Menu Setup
    def _set_options(self):
        self.options = [
            MenuOption(
                name="Manage Tables",
                action=self.manage_tables,
            ),
            MenuOption(
                name="Manage Database Connections",
                action=self.manage_dbs,
            ),
            MenuOption(name="Exit", action=self.back),
        ]

    # MARK: - Menu Actions
    def manage_tables(self):
        """Open the Manage Tables menu."""
        self.ctx.menu_ctrlr.open_menu(self.menus.manage_tables, "Manage Tables")

    def manage_dbs(self):
        """Open the Manage Database Connections menu."""
        self.ctx.menu_ctrlr.open_menu(self.menus.manage_dbs, "Manage Database Connections")

    def back(self):
        """Return to the previous menu."""
        self.clear()
        console.print("Goodbye!")
        sys.exit(0)
