"""Tests for the SQLExport class."""

import numpy as np
from cms_etl.db.sql_export import SQLExport

# import pandas as pd


class TestSQLExport:
    """Tests for the SQLExport class."""

    def test_init(self, app_ctx_w_table):
        """Test the init method."""
        sql_export = SQLExport(app_ctx_w_table, "test_table", "test_db")
        assert sql_export.table_key == "test_table"
        assert sql_export.db_key == "senior-one-prod"
        assert sql_export.table is not None
        assert sql_export.table.name == "test_table"
        assert sql_export.db_interface is not None

    def test_get_city_state_ids(self, app_ctx_w_table):
        """Test the get_city_state_ids method."""
        sql_export = SQLExport(app_ctx_w_table, "test_table", "test_db")
        df = sql_export.ctx.table_mgr.get_table("test_table").df
        # print(df, "\n")
        for row in df.itertuples():
            city_id, state_id = sql_export.get_city_state_ids(row.city, row.state)
            # print(f"{row.city=}, {row.state=}, {city_id=}, {state_id=}")
            assert isinstance(city_id, np.integer)
            assert isinstance(state_id, np.integer)
