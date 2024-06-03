"""Tests for the AddColumnCommand class."""

import pandas as pd
from cms_etl.table.commands.add_column import AddColumnCommand


def test_add_column_after_command(mock_table):
    """Test the AddColumnCommand class."""

    cmd = AddColumnCommand(mock_table, "c", 7, after="a")
    assert cmd.col_name == "c"
    assert cmd.fill_value == 7
    assert cmd.after == "a"
    assert cmd.before is None
    assert cmd._cmd_args == {
        "col_name": "c",
        "fill_value": 7,
        "after": "a",
        "before": None,
    }
    assert cmd._col_pos == 1
    cmd.execute()
    assert "c" in mock_table.df.columns
    assert mock_table.df["c"].equals(pd.Series([7, 7, 7]))
    assert mock_table.df.columns.tolist() == ["a", "c", "b"]
    cmd.undo()
    assert "c" not in mock_table.df.columns


def test_add_column_before_command(mock_table):
    """Test the AddColumnCommand class."""
    cmd = AddColumnCommand(mock_table, "c", 7, before="a")
    assert cmd.col_name == "c"
    assert cmd.fill_value == 7
    assert cmd.after is None
    assert cmd.before == "a"
    assert cmd._cmd_args == {
        "col_name": "c",
        "fill_value": 7,
        "after": None,
        "before": "a",
    }
    assert cmd._col_pos == 0
    cmd.execute()
    assert "c" in mock_table.df.columns
    assert mock_table.df["c"].equals(pd.Series([7, 7, 7]))
    assert mock_table.df.columns.tolist() == ["c", "a", "b"]
    cmd.undo()
    assert "c" not in mock_table.df.columns
    assert mock_table.df.columns.tolist() == ["a", "b"]
    assert mock_table.df.equals(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))


def test_add_column_no_position_command(mock_table):
    """Test the AddColumnCommand class."""
    cmd = AddColumnCommand(mock_table, "c", 7)
    assert cmd.col_name == "c"
    assert cmd.fill_value == 7
    assert cmd.after is None
    assert cmd.before is None
    assert cmd._cmd_args == {
        "col_name": "c",
        "fill_value": 7,
        "after": None,
        "before": None,
    }
    assert cmd._col_pos is None
    cmd.execute()
    assert "c" in mock_table.df.columns
    assert mock_table.df["c"].equals(pd.Series([7, 7, 7]))
    assert mock_table.df.columns.tolist() == ["a", "b", "c"]
    cmd.undo()
    assert "c" not in mock_table.df.columns
    assert mock_table.df.columns.tolist() == ["a", "b"]
    assert mock_table.df.equals(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))


def test_undo(mock_table):
    """Test the undo method of the AddColumnCommand."""
    cmd = AddColumnCommand(mock_table, "c", 7, after="a")
    cmd.execute()
    assert "c" in mock_table.df.columns
    cmd.undo()
    assert "c" not in mock_table.df.columns
    assert mock_table.df.columns.tolist() == ["a", "b"]
    assert mock_table.df.equals(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
