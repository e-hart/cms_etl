"""Tests for the TableLoader class."""

import pandas as pd
import pytest
from cms_etl.db.db_manager import DBManager
from cms_etl.table.table_loader import TableLoader

from tests.db_test_config import db_test_config


class TestTableLoader:
    """Tests for the TableLoader class."""

    @pytest.fixture
    def table_loader(self):
        """Return a TableLoader instance."""
        return TableLoader()

    @pytest.fixture
    def table_loader_with_db_mgr(self):
        """Return a TableLoader instance with a mocked DBManager."""
        db_mgr = DBManager(db_test_config)
        return TableLoader(db_mgr)

    def test_load_csv(self, table_loader: TableLoader):
        """Test the load_csv method."""
        # print cwd
        df = table_loader.load_csv("tests/data/simple_table.csv")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (3, 2)
        assert df.columns.tolist() == ["A", "B"]
        assert df.index.tolist() == [0, 1, 2]
        assert df.values.tolist() == [[1, 4], [2, 5], [3, 6]]
