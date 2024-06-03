import pandas as pd
import pytest
from cms_etl.table.commands.remove_column import RemoveColumnCommand


def test_remove_column_command(mock_table):
    """Test the RemoveColumnCommand class."""
    mock_table.df["c"] = [7, 7, 7]
    cmd = RemoveColumnCommand(mock_table, "c")
    assert cmd.cols == "c"
    assert cmd._cmd_args == {"cols": "c"}  # pylint: disable=protected-access
    cmd.execute()
    assert "c" not in mock_table.df.columns
    cmd.undo()
    assert "c" in mock_table.df.columns
    assert mock_table.df["c"].equals(pd.Series([7, 7, 7]))


def test_remove_column_command_with_multiple_columns(mock_table):
    """Test the RemoveColumnCommand class with multiple columns."""
    mock_table.df["c"] = [7, 7, 7]
    mock_table.df["d"] = [8, 8, 8]
    cmd = RemoveColumnCommand(mock_table, ["c", "d"])
    assert cmd.cols == ["c", "d"]
    assert cmd._cmd_args == {"cols": ["c", "d"]}  # pylint: disable=protected-access
    cmd.execute()
    assert "c" not in mock_table.df.columns
    assert "d" not in mock_table.df.columns
    cmd.undo()
    assert "c" in mock_table.df.columns
    assert "d" in mock_table.df.columns
    assert mock_table.df["c"].equals(pd.Series([7, 7, 7]))
    assert mock_table.df["d"].equals(pd.Series([8, 8, 8]))


def test_remove_column_command_with_non_existent_column(mock_table):
    """Test the RemoveColumnCommand class with a non-existent column."""
    with pytest.raises(ValueError):
        _ = RemoveColumnCommand(mock_table, "d")


def test_remove_column_command_with_non_existent_columns(mock_table):
    """Test the RemoveColumnCommand class with non-existent columns."""
    with pytest.raises(ValueError):
        _ = RemoveColumnCommand(mock_table, ["c", "d"])
