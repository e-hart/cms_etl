"""Tests for the SortRowsCommand class."""

import pandas as pd
from cms_etl.table.commands.sort_rows import SortRowsCommand


def test_sort_rows_command(mock_table):
    """Test the SortRowsCommand class."""

    mock_table.df["a"] = [3, 2, 1]
    cmd = SortRowsCommand(mock_table, "a")
    assert cmd.col_name == "a"
    assert cmd.ascending
    assert cmd._cmd_args == {  # pylint: disable=protected-access
        "col_name": "a",
        "ascending": True,
    }
    cmd.execute()
    assert mock_table.df["a"].reset_index(drop=True).equals(pd.Series([1, 2, 3]))
    cmd.undo()
    assert mock_table.df["a"].reset_index(drop=True).equals(pd.Series([3, 2, 1]))


def test_sort_rows_command_descending(mock_table):
    """Test the SortRowsCommand class with descending order."""
    mock_table.df["a"] = [1, 2, 3]
    cmd = SortRowsCommand(mock_table, "a", ascending=False)
    assert not cmd.ascending
    cmd.execute()
    assert mock_table.df["a"].reset_index(drop=True).equals(pd.Series([3, 2, 1]))
    cmd.undo()
    assert mock_table.df["a"].reset_index(drop=True).equals(pd.Series([1, 2, 3]))
