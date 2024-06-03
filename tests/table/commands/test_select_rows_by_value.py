"""Tests for the SelectRowsByValueCommand class."""

import pandas as pd
from cms_etl.table.commands.select_rows_by_value import SelectRowsByValueCommand
from cms_etl.table.table import Table


def test_select_rows_by_value_command(mock_table: Table):
    """Test the SelectRowsByValueCommand class."""
    mock_table.df["a"] = [1, 2, 3]
    cmd = SelectRowsByValueCommand(mock_table, "a", 2)
    assert cmd.column == "a"
    assert cmd.value == 2
    assert cmd._cmd_args == {  # pylint: disable=protected-access
        "column": "a",
        "value": 2,
    }
    cmd.execute()
    assert len(mock_table.df) == 1
    assert mock_table.df["a"].reset_index(drop=True).equals(pd.Series([2]))
    cmd.undo()
    assert len(mock_table.df) == 3
    assert mock_table.df["a"].reset_index(drop=True).equals(pd.Series([1, 2, 3]))
