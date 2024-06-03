"""Tests for the FindColumnDuplicatesCommand class."""

import pandas as pd
from cms_etl.table.commands.find_column_duplicates import FindColumnDuplicatesCommand
from cms_etl.table.table import Table


def test_find_duplicates_command():
    """Test the FindColumnDuplicatesCommand class."""
    df = pd.DataFrame({"a": [1, 2, 2, 3], "b": [4, 5, 6, 7], "c": [8, 9, 10, 11]})
    table = Table(df.copy(deep=True), "test_table")
    cmd = FindColumnDuplicatesCommand(table, "a")
    cmd.execute()
    assert len(table.df) == 2
    assert table.df["a"].reset_index(drop=True).equals(pd.Series([2, 2]))
    cmd.undo()
    assert len(table.df) == 4
    assert table.df["a"].reset_index(drop=True).equals(pd.Series([1, 2, 2, 3]))
