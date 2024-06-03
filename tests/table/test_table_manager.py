"""Tests for the TableManager class."""

import pandas as pd
import pytest
from cms_etl.table.table_manager import TableManager


class TestTableManager:
    """Tests for the TableManager class."""

    @pytest.fixture
    def table_manager(self):
        """Return a TableManager instance."""
        return TableManager()

    def test_add_table(self, table_manager: TableManager):
        """Test the add_table method."""
        df = pd.DataFrame()
        table = table_manager.add_table(df, "test_table", "test table")
        assert table_manager.tables["test_table"] == table

    def test_remove_table(self, table_manager: TableManager):
        """Test the remove_table method."""
        df = pd.DataFrame()
        table_manager.add_table(df, "test_table", "test table")
        assert table_manager.tables["test_table"]
        table_manager.remove_table("test_table")
        assert "test_table" not in table_manager.tables

    def test_list_tables(self, table_manager: TableManager):
        """Test the list_tables method."""
        df = pd.DataFrame()
        table_manager.add_table(df, "test_table", "test table")
        tables = list(table_manager.list_tables())
        assert len(tables) == 1
        assert tables[0].name == "test_table"
        table_manager.add_table(df.copy(), "test_table2", "test table 2")
        tables = list(table_manager.list_tables())
        assert len(tables) == 2
        assert tables[1].name == "test_table2"

    def test_get_table(self, table_manager: TableManager):
        """Test the get_table method."""
        df = pd.DataFrame()
        table_manager.add_table(df, "test_table", "test table")
        table = table_manager.get_table("test_table")
        assert table.name == "test_table"

    def test_view_dataframe(self, table_manager: TableManager, capsys):
        """Test the view_dataframe method."""
        df = pd.DataFrame()
        table_manager.add_table(df, "test_table", "test table")
        table_manager.view_dataframe("test_table")
        captured = capsys.readouterr()
        assert captured.out == "Empty DataFrame\nColumns: []\nIndex: []\n"
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        table_manager.add_table(df, "test_table2", "test table 2")
        table_manager.view_dataframe("test_table2")
        captured = capsys.readouterr()
        assert captured.out == "   A  B\n0  1  4\n1  2  5\n2  3  6\n"
