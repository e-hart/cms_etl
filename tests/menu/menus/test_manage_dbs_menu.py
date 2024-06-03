"""Test Manage Databases Menu."""

import pytest
from cms_etl.menu.menus.manage_dbs import ManageDatabasesMenu
from pytest_mock import MockerFixture


class TestManageDatabasesMenu:
    """Test Manage Databases Menu."""

    def test_manage_databases_menu(self, app_ctx, mocker: MockerFixture):
        """Test Manage Databases Menu."""
        manage_dbs_menu = ManageDatabasesMenu(app_ctx, "Manage Databases")
        manage_dbs_menu.get_choice = mocker.MagicMock(return_value="3")
        manage_dbs_menu.clear = mocker.MagicMock()
        assert manage_dbs_menu.title == "Manage Databases"
        assert manage_dbs_menu.ctx == app_ctx
        assert not manage_dbs_menu.options
        manage_dbs_menu._set_options()  # pylint: disable=protected-access
        assert len(manage_dbs_menu.options) > 0

        manage_dbs_menu.run()
        manage_dbs_menu.get_choice.assert_called_once()
        manage_dbs_menu.clear.assert_called_once()

    def test_add_database(self, app_ctx, mocker: MockerFixture):
        """Test Add Database."""
        mock_print = mocker.patch("cms_etl.utils.console.print")
        mock_input = mocker.patch("cms_etl.utils.console.input")
        mock_prompt_for_db_config = mocker.patch(
            "cms_etl.menu.menus.manage_dbs.prompt_mysql_config"
        )

        manage_dbs_menu = ManageDatabasesMenu(app_ctx, "Manage Databases")
        mock_mysql_config = mocker.patch("cms_etl.menu.menus.manage_dbs.MySQLConfig")

        manage_dbs_menu.ctx.db_mgr.add_db = mocker.MagicMock()
        manage_dbs_menu.add_database()
        mock_print.assert_called_once_with("Add Database Connection")
        mock_input.assert_called_once_with("Enter name for Database: ")
        mock_prompt_for_db_config.assert_called_once()
        mock_mysql_config.assert_called_once()
        manage_dbs_menu.ctx.db_mgr.add_db.assert_called_once()

        manage_dbs_menu.ctx.db_mgr.add_db.side_effect = Exception("Test")
        mocker.patch("cms_etl.utils.console.log")
        with pytest.raises(Exception):
            manage_dbs_menu.add_database()

    def test_list_databases(self, app_ctx, mocker: MockerFixture):
        """Test List Databases."""
        mock_rule = mocker.patch("cms_etl.utils.console.rule")
        mock_print = mocker.patch("cms_etl.utils.console.print")

        manage_dbs_menu = ManageDatabasesMenu(app_ctx, "Manage Databases")
        manage_dbs_menu.ctx.db_mgr.list_dbs = mocker.MagicMock(return_value=["db1", "db2"])
        manage_dbs_menu.list_databases()
        mock_rule.assert_called_once_with("Databases")
        assert mock_print.call_count == 2

    def test_remove_database(self, app_ctx, mocker: MockerFixture):
        """Test Remove Database."""
        mock_rule = mocker.patch("cms_etl.utils.console.rule")
        mock_print = mocker.patch("cms_etl.utils.console.print")
        mock_input = mocker.patch("cms_etl.utils.console.input")

        manage_dbs_menu = ManageDatabasesMenu(app_ctx, "Manage Databases")
        manage_dbs_menu.ctx.db_mgr.remove_db = mocker.MagicMock()
        manage_dbs_menu.ctx.db_mgr.remove_db.side_effect = KeyError
        manage_dbs_menu.remove_database()
        mock_rule.assert_called()
        mock_print.assert_called()
        mock_input.assert_called_once()
        manage_dbs_menu.ctx.db_mgr.remove_db.assert_called_once()

        manage_dbs_menu.ctx.db_mgr.remove_db.reset_mock()
        manage_dbs_menu.remove_database()
        manage_dbs_menu.ctx.db_mgr.remove_db.assert_called_once()
        mock_print.assert_called()
