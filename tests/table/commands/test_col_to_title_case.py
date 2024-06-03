"""Tests for the ColumnToTitleCaseCommand class."""

import pandas as pd
import pytest
from cms_etl.table.commands.col_to_title_case import ColumnToTitleCaseCommand


def test_col_to_title_case_command(mock_table):
    """Test the ColumnToTitleCaseCommand class."""
    df = pd.DataFrame(
        {
            "a": ["foo", "bar's", "o'bazien", "do a barrel roll"],
            "b": [1, 2, 3, 4],
        }
    )
    mock_table.df = df
    # print("\n", mock_table.df)
    cmd = ColumnToTitleCaseCommand(mock_table, "a")
    assert cmd.col_name == "a"
    assert cmd._cmd_args == {"col_name": "a"}  # pylint: disable=protected-access
    cmd.execute()
    assert mock_table.df["a"].equals(pd.Series(["Foo", "Bar's", "O'Bazien", "Do a Barrel Roll"]))
    # print("\n", mock_table.df)
    cmd.undo()
    assert mock_table.df["a"].equals(pd.Series(["foo", "bar's", "o'bazien", "do a barrel roll"]))


def test_col_to_title_case_command_with_non_string_values(mock_table):
    """Test the ColumnToTitleCaseCommand class with non-string values."""

    mock_table.df["a"] = [1, 2, 3]
    with pytest.raises(ValueError):
        _ = ColumnToTitleCaseCommand(mock_table, "a")
