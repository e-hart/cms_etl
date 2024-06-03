"""Test the SQLiteAdapter class."""

import os

import pandas as pd
import pytest
from cms_etl.db.adapters import SQLiteAdapter
from cms_etl.db.adapters.config import SQLiteConfig


def test_sqlite_fixture(sqlite_test_db):
    """Test the SQLiteAdapter class."""
    assert isinstance(sqlite_test_db, SQLiteAdapter)
    assert sqlite_test_db.name == "test.db"
    assert sqlite_test_db.list_tables() == ["simple_table"]
    schema = sqlite_test_db.get_table_schema("simple_table")
    assert schema == [
        (0, "a", "INTEGER", 0, None, 0),
        (1, "b", "INTEGER", 0, None, 0),
    ]


def test_create_sqlite_interface():
    """Test creating a SQLiteAdapter object."""
    sqlite_config = SQLiteConfig(file_path="tests/data/test.db")
    sqlite_interface = SQLiteAdapter(sqlite_config)
    assert sqlite_interface.name == "test.db"
    assert sqlite_interface.config == sqlite_config


def test_df_to_table(sqlite_test_db):
    """Test the df_to_table method."""
    df = pd.DataFrame(
        {
            "int": [1, 2, 3],
            "str": ["aaa", "bbb", "ccc"],
            "float": [1.1, 2.2, 3.3],
            "bool": [True, False, True],
        }
    )
    table_name = "test_table"
    sqlite_test_db.df_to_table(df, table_name)
    assert table_name in sqlite_test_db.list_tables()
    assert sqlite_test_db.get_table_schema(table_name) == [
        (0, "int", "BIGINT", 0, None, 0),
        (1, "str", "TEXT", 0, None, 0),
        (2, "float", "FLOAT", 0, None, 0),
        (3, "bool", "BOOLEAN", 0, None, 0),
    ]
    df2 = sqlite_test_db.get_table(table_name)
    assert df.equals(df2)


def test_df_to_table_if_exists_replace(sqlite_test_db):
    """Test the df_to_table method with if_exists='replace'."""
    st_df = sqlite_test_db.get_table("simple_table")
    assert st_df.shape == (3, 2)
    df = pd.DataFrame(
        {
            "int": [1, 2, 3],
            "str": ["aaa", "bbb", "ccc"],
            "float": [1.1, 2.2, 3.3],
            "bool": [True, False, True],
        }
    )
    table_name = "simple_table"
    sqlite_test_db.df_to_table(df, table_name, if_exists="replace")
    df2 = sqlite_test_db.get_table(table_name)
    assert df.equals(df2)
    assert df2.shape == (3, 4)
    assert df2.columns.tolist() == ["int", "str", "float", "bool"]


def test_df_to_table_if_exists_fail(sqlite_test_db):
    """Test the df_to_table method with if_exists='fail'."""
    st_df = sqlite_test_db.get_table("simple_table")
    assert st_df.shape == (3, 2)
    df = pd.DataFrame(
        {
            "int": [1, 2, 3],
            "str": ["aaa", "bbb", "ccc"],
            "float": [1.1, 2.2, 3.3],
            "bool": [True, False, True],
        }
    )
    table_name = "simple_table"
    with pytest.raises(ValueError) as e:
        sqlite_test_db.df_to_table(df, table_name, if_exists="fail")
    print(e.exconly())


def test_execute_query(sqlite_test_db):
    """Test the execute_query method."""
    query = "SELECT * FROM simple_table"
    df = sqlite_test_db.execute_query(query)
    assert df.shape == (3, 2)
    assert df.columns.tolist() == ["a", "b"]
    assert df.index.tolist() == [0, 1, 2]
    assert df.values.tolist() == [[1, 4], [2, 5], [3, 6]]


def test_test_connection(sqlite_test_db):
    """Test the test_connection method."""
    assert sqlite_test_db.test_connection() is True


def test_invalid_db_path():
    """Test creating a SQLiteAdapter object with an invalid file path."""
    sqlite_config = SQLiteConfig(file_path="tests/data/non_existent.db")
    with pytest.raises(FileNotFoundError) as e:
        _ = SQLiteAdapter(sqlite_config)
    print(e.exconly())


def test_invalid_db_path_create():
    """Test creating a SQLiteAdapter object with an invalid file path and if_not_exists='create'."""
    assert not os.path.exists("tests/data/non_existent.db")
    sqlite_config = SQLiteConfig(file_path="tests/data/non_existent.db", if_not_exists="create")
    _ = SQLiteAdapter(sqlite_config)
    assert os.path.exists("tests/data/non_existent.db")
    os.remove("tests/data/non_existent.db")


def test_name_property(sqlite_test_db):
    """Test the name property."""
    assert (
        sqlite_test_db.name  # pylint: disable=protected-access
        == sqlite_test_db.config.name  # pylint: disable=protected-access
    )


def test_config_property(sqlite_test_db):
    """Test the config property."""
    assert (
        sqlite_test_db.config  # pylint: disable=protected-access
        == sqlite_test_db._config  # pylint: disable=protected-access
    )


def test_engine_property(sqlite_test_db):
    """Test the engine property."""
    assert (
        sqlite_test_db.engine  # pylint: disable=protected-access
        == sqlite_test_db._engine  # pylint: disable=protected-access
    )


def test_getitem(sqlite_test_db):
    """Test the __getitem__ method."""
    table_name = "simple_table"
    df = sqlite_test_db[table_name]
    assert df.shape == (3, 2)
    assert df.columns.tolist() == ["a", "b"]
    assert df.index.tolist() == [0, 1, 2]
    assert df.values.tolist() == [[1, 4], [2, 5], [3, 6]]
    with pytest.raises(ValueError):
        _ = sqlite_test_db["non_existent_table"]
    with pytest.raises(AttributeError):
        _ = sqlite_test_db[1]


def test_close(sqlite_test_db):
    """Test the close method."""
    sqlite_test_db.close()
    with pytest.raises(Exception):
        _ = sqlite_test_db.engine
