"""This package contains all the menu classes that are used in the cms_etl application."""

from .compare.compare_tables import CompareTablesMenu
from .edit_table import EditTableMenu
from .load_data import LoadDataMenu
from .main_menu import MainMenu
from .manage_dbs import ManageDatabasesMenu
from .manage_tables import ManageTablesMenu


class Menus:
    """A class that contains all the menus that are used in the cms_etl application."""

    def __init__(self):
        self.main_menu = MainMenu
        self.manage_dbs = ManageDatabasesMenu
        self.manage_tables = ManageTablesMenu
        self.load_data = LoadDataMenu
        self.edit_table = EditTableMenu
        self.compare_tables = CompareTablesMenu

    def get_menu(self, menu_name):
        """Returns the menu object that corresponds to the given menu name."""
        return getattr(self, menu_name)

    def get_menu_names(self):
        """Returns a list of all the menu names."""
        return [menu_name for menu_name in dir(self) if not menu_name.startswith("__")]
