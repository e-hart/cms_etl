"""Test the application context."""

from cms_etl.app_context import AppContext
from cms_etl.menu.menu_controller import MenuController
from pytest_mock import MockerFixture

from tests.db_test_config import db_test_config


def test_app_context(mocker: MockerFixture):
    """Test the application context."""
    mock_print = mocker.patch("cms_etl.utils.console.print")
    app_ctx = AppContext(db_test_config)
    # mock_print.assert_called()
    assert app_ctx.db_mgr
    assert app_ctx.data_loader
    assert app_ctx.table_mgr
    assert app_ctx.menu_ctrlr
    assert isinstance(app_ctx.menu_ctrlr, MenuController)
    assert app_ctx.menu_ctrlr.ctx == app_ctx
    assert app_ctx.menu_ctrlr.menus
    assert app_ctx.menu_ctrlr.menu_stack.is_empty
    assert app_ctx.data_loader.db_mgr == app_ctx.db_mgr
