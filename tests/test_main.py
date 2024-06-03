"""Test the main module."""

from cms_etl.main import main


def test_main(mocker):
    """Test the main function."""
    mocker.patch("cms_etl.utils.console.print")
    mocker.patch("cms_etl.utils.console.input")
    mocker.patch("cms_etl.app_context.AppContext")
    mock_run_main = mocker.patch("cms_etl.menu.MenuController.run_main_menu")
    main()
    mock_run_main.assert_called_once()
