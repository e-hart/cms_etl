"""Test Main Menu."""

from cms_etl.menu.menus.main_menu import MainMenu
from pytest_mock import MockerFixture


def test_main_menu(app_ctx, mocker: MockerFixture):
    """Test Main Menu."""
    mocker.patch("sys.exit")
    main_menu = MainMenu(app_ctx, "Main Menu")
    main_menu.get_choice = mocker.MagicMock(return_value="3")
    main_menu.clear = mocker.MagicMock()
    assert main_menu.title == "Main Menu"
    assert main_menu.ctx == app_ctx
    assert main_menu.menus == app_ctx.menu_ctrlr.menus
    assert not main_menu.options
    main_menu._set_options()  # pylint: disable=protected-access
    assert len(main_menu.options) > 0

    main_menu.run()
    main_menu.get_choice.assert_called_once()
    main_menu.clear.assert_called_once()


def test_choices(app_ctx, mocker: MockerFixture):
    """Test Main Menu Manage Tables."""
    main_menu = MainMenu(app_ctx, "Main Menu")
    main_menu.ctx.menu_ctrlr.open_menu = mocker.MagicMock()
    main_menu.manage_tables()
    main_menu.ctx.menu_ctrlr.open_menu.assert_called_once_with(
        main_menu.menus.manage_tables, "Manage Tables"
    )

    main_menu.ctx.menu_ctrlr.open_menu.reset_mock()
    main_menu.manage_dbs()
    main_menu.ctx.menu_ctrlr.open_menu.assert_called_once_with(
        main_menu.menus.manage_dbs, "Manage Database Connections"
    )

    main_menu.ctx.menu_ctrlr.open_menu.reset_mock()
    mock_exit = mocker.patch("sys.exit")
    mock_print = mocker.patch("cms_etl.utils.console.print")
    mock_clear = mocker.patch("cms_etl.utils.console.clear")
    main_menu.back()
    mock_clear.assert_called_once()
    mock_print.assert_called_once_with("Goodbye!")
    mock_exit.assert_called_once_with(0)


def test_invalid_choice_index(app_ctx, mocker: MockerFixture):
    """Test Main Menu Run."""
    main_menu = MainMenu(app_ctx, "Main Menu")
    main_menu.get_choice = mocker.MagicMock(return_value="4")

    main_menu.display = mocker.MagicMock()

    main_menu.run()
    main_menu.display.assert_called_once()
    main_menu.get_choice.assert_called_once()


def test_invalid_choice_value(app_ctx, mocker: MockerFixture):
    """Test Main Menu Run."""
    main_menu = MainMenu(app_ctx, "Main Menu")
    main_menu.get_choice = mocker.MagicMock(return_value="a")
    mock_console_print = mocker.patch("cms_etl.utils.console.print")
    main_menu.display = mocker.MagicMock()

    main_menu.run()
    main_menu.display.assert_called_once()
    main_menu.get_choice.assert_called_once()
    mock_console_print.assert_called_once_with("Invalid choice.")
