import pandas as pd
from cms_etl.table.commands.set_column_type import SetColumnTypeCommand
from cms_etl.table.table import Table


def test_set_column_type_command_int_to_float():
    """Test the SetColumnTypeCommand class."""
    df = pd.DataFrame({"a": [1, 2, 3]})
    tbl = Table(df, "test_table", "Test table...")
    assert pd.api.types.is_integer_dtype(tbl.df["a"])
    cmd = SetColumnTypeCommand(tbl, "a", "float")
    assert cmd.col_name == "a"
    assert cmd.col_type == "float"
    assert cmd._cmd_args == {  # pylint: disable=protected-access
        "col_name": "a",
        "col_type": "float",
    }
    cmd.execute()
    assert pd.api.types.is_float_dtype(tbl.df["a"])
    cmd.undo()
    assert pd.api.types.is_integer_dtype(tbl.df["a"])


def test_set_column_type_command_int_to_str():
    """Test the SetColumnTypeCommand class."""
    df = pd.DataFrame({"a": [1, 2, 3]})
    tbl = Table(df, "test_table", "Test table...")
    assert pd.api.types.is_integer_dtype(tbl.df["a"])
    cmd = SetColumnTypeCommand(tbl, "a", "str")
    assert cmd.col_name == "a"
    assert cmd.col_type == "str"
    assert cmd._cmd_args == {  # pylint: disable=protected-access
        "col_name": "a",
        "col_type": "str",
    }
    cmd.execute()
    assert pd.api.types.is_string_dtype(tbl.df["a"])
    cmd.undo()
    assert pd.api.types.is_integer_dtype(tbl.df["a"])


def test_set_column_type_command_float_to_int():
    """Test the SetColumnTypeCommand class."""
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0]})
    tbl = Table(df, "test_table", "Test table...")
    assert pd.api.types.is_float_dtype(tbl.df["a"])
    cmd = SetColumnTypeCommand(tbl, "a", "int")
    assert cmd.col_name == "a"
    assert cmd.col_type == "int"
    assert cmd._cmd_args == {  # pylint: disable=protected-access
        "col_name": "a",
        "col_type": "int",
    }
    cmd.execute()
    assert pd.api.types.is_integer_dtype(tbl.df["a"])
    cmd.undo()
    assert pd.api.types.is_float_dtype(tbl.df["a"])


def test_set_column_type_command_str_to_int():
    """Test the SetColumnTypeCommand class."""
    df = pd.DataFrame({"a": ["1", "2", "3"]})
    tbl = Table(df, "test_table", "Test table...")
    assert pd.api.types.is_string_dtype(tbl.df["a"])
    cmd = SetColumnTypeCommand(tbl, "a", "int")
    assert cmd.col_name == "a"
    assert cmd.col_type == "int"
    assert cmd._cmd_args == {  # pylint: disable=protected-access
        "col_name": "a",
        "col_type": "int",
    }
    cmd.execute()
    assert pd.api.types.is_integer_dtype(tbl.df["a"])
    cmd.undo()
    assert pd.api.types.is_string_dtype(tbl.df["a"])


def test_set_column_type_command_str_to_float():
    """Test the SetColumnTypeCommand class."""
    df = pd.DataFrame({"a": ["1.0", "2.0", "3.0"]})
    tbl = Table(df, "test_table", "Test table...")
    assert pd.api.types.is_string_dtype(tbl.df["a"])
    cmd = SetColumnTypeCommand(tbl, "a", "float")
    assert cmd.col_name == "a"
    assert cmd.col_type == "float"
    assert cmd._cmd_args == {  # pylint: disable=protected-access
        "col_name": "a",
        "col_type": "float",
    }
    cmd.execute()
    assert pd.api.types.is_float_dtype(tbl.df["a"])
    cmd.undo()
    assert pd.api.types.is_string_dtype(tbl.df["a"])
