from cms_etl.menu.base_menu import MenuOption


class TestMenuOption:
    """Test the MenuOption class."""

    def test_init(self):
        """Test the initialization of the MenuOption."""
        name: str = "Option 1"

        def action():
            print("Option 1 selected")

        menu_option = MenuOption(name=name, action=action)

        assert menu_option.name == name
        assert menu_option.action == action  # pylint: disable=W0143
