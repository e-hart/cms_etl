"""Test the Menu Controller."""

# FILEPATH: /Users/mbp/cms_etl/tests/test_menu_controller.py

import pytest
from cms_etl.app_context import AppContext
from cms_etl.menu import BaseMenu, MenuController
from cms_etl.menu.menus.main_menu import MainMenu


class TestMenuController:
    """Test the Menu Controller."""

    @pytest.fixture
    def menu_controller(self, app_ctx):
        """Menu Controller fixture."""
        return MenuController(app_ctx)

    def test_init(self, menu_controller):
        """Test the initialization of the Menu Controller."""
        assert isinstance(menu_controller.ctx, AppContext)
        assert menu_controller.menus
        assert menu_controller.menu_stack.is_empty

    def test_main_loop(self, menu_controller):
        """Test the main loop of the Menu Controller."""
        menu_controller.main_loop()
        assert menu_controller.menu_stack.is_empty

    # def test_main_menu(self, menu_controller):
    #     """Test the Main Menu."""
    #     menu_controller.run_main_menu()
    #     assert not menu_controller.menu_stack.is_empty
    #     assert isinstance(menu_controller.menu_stack.peek()[0], BaseMenu)
    #     assert menu_controller.menu_stack.peek()[0].__name__ == "MainMenu"
    #     assert menu_controller.menu_stack.peek()[1] == ["Main Menu"]
    #     assert menu_controller.menu_stack.peek()[2] == {}
    #     menu_controller.back()

    def test_open_close_menu(self, menu_controller):
        """Test the open menu method."""
        menu_controller.open_menu(MainMenu, "Main Menu")
        assert not menu_controller.menu_stack.is_empty
        assert issubclass(menu_controller.menu_stack.peek()[0], BaseMenu)
        assert menu_controller.menu_stack.peek()[0].__name__ == "MainMenu"
        assert menu_controller.menu_stack.peek()[1] == ["Main Menu"]
        assert menu_controller.menu_stack.peek()[2] == {}
        menu_controller.back()
        assert menu_controller.menu_stack.is_empty

    def test_back(self, menu_controller):
        """Test the back method."""
        menu_controller.open_menu(MainMenu, "Main Menu")
        menu_controller.open_menu(menu_controller.menus.manage_tables, "Manage Tables")
        assert len(menu_controller.menu_stack) == 2
        assert menu_controller.current_menu == menu_controller.menus.manage_tables
        menu_controller.back()
        assert len(menu_controller.menu_stack) == 1
        assert menu_controller.current_menu == MainMenu

    def test_open_menu_with_args(self, menu_controller):
        """Test the open menu method with arguments."""
        menu_controller.open_menu(MainMenu, "Menu Title", "arg1", "arg2")
        assert not menu_controller.menu_stack.is_empty
        assert issubclass(menu_controller.menu_stack.peek()[0], BaseMenu)
        assert menu_controller.menu_stack.peek()[0].__name__ == "MainMenu"
        assert menu_controller.menu_stack.peek()[1] == ["Menu Title", "arg1", "arg2"]
        assert menu_controller.menu_stack.peek()[2] == {}
        menu_controller.back()

    def test_open_menu_with_kwargs(self, menu_controller):
        """Test the open menu method with keyword arguments."""
        menu_controller.open_menu(MainMenu, "Menu Title", kwarg1="kwarg1", kwarg2="kwarg2")
        assert not menu_controller.menu_stack.is_empty
        assert issubclass(menu_controller.menu_stack.peek()[0], BaseMenu)
        assert menu_controller.menu_stack.peek()[0].__name__ == "MainMenu"
        assert menu_controller.menu_stack.peek()[1] == ["Menu Title"]
        assert menu_controller.menu_stack.peek()[2] == {
            "kwarg1": "kwarg1",
            "kwarg2": "kwarg2",
        }
        menu_controller.back()
        assert menu_controller.menu_stack.is_empty

    def test_open_menu_with_args_and_kwargs(self, menu_controller):
        """Test the open menu method with arguments and keyword arguments."""
        menu_controller.open_menu(
            MainMenu, "Menu Title", "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2"
        )
        assert not menu_controller.menu_stack.is_empty
        assert issubclass(menu_controller.menu_stack.peek()[0], BaseMenu)
        assert menu_controller.menu_stack.peek()[0].__name__ == "MainMenu"
        assert menu_controller.menu_stack.peek()[1] == ["Menu Title", "arg1", "arg2"]
        assert menu_controller.menu_stack.peek()[2] == {
            "kwarg1": "kwarg1",
            "kwarg2": "kwarg2",
        }
        menu_controller.back()
        assert menu_controller.menu_stack.is_empty

    def test_open_menu_with_invalid_menu(self, menu_controller):
        """Test the open menu method with an invalid menu."""

        class InvalidMenu:
            """Invalid Menu."""

        with pytest.raises(ValueError):
            menu_controller.open_menu(InvalidMenu, "Invalid menu")
        assert menu_controller.menu_stack.is_empty
