"""Tests for the RenameColumnCommand class."""

import pandas as pd
from cms_etl.table.commands.rename_column import RenameColumnCommand


def test_rename_column_command(mock_table):
    """Test the RenameColumnCommand class."""
    mock_table.df["a"] = [1, 2, 3]
    cmd = RenameColumnCommand(mock_table, "a", "z")
    assert cmd.old_name == "a"
    assert cmd.new_name == "z"
    assert cmd._cmd_args == {  # pylint: disable=protected-access
        "old_name": "a",
        "new_name": "z",
    }
    cmd.execute()
    assert "a" not in mock_table.df.columns
    assert "z" in mock_table.df.columns
    cmd.undo()
    assert "a" in mock_table.df.columns
    assert "z" not in mock_table.df.columns
    assert mock_table.df["a"].equals(pd.Series([1, 2, 3]))
