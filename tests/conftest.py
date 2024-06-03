"""This file is used to define fixtures that are used in the tests."""

import os
import sqlite3

import pandas as pd
import pytest
from cms_etl.app_context import AppContext
from cms_etl.db.adapters import SQLiteAdapter
from cms_etl.db.adapters.config import SQLiteConfig
from cms_etl.table.table import Table
from pytest_mock import MockerFixture

from .db_test_config import db_test_config


@pytest.fixture
def app_ctx(mocker: MockerFixture):
    """Application context fixture."""
    mocker.patch("cms_etl.utils.console.print")
    ctx = AppContext(db_test_config)
    return ctx


@pytest.fixture
def app_ctx_w_table(mocker: MockerFixture):
    """Application context fixture with a table."""
    mocker.patch("cms_etl.utils.console.print")
    ctx = AppContext(db_test_config)
    df = ctx.data_loader.load_csv("tests/data/test.csv")
    ctx.table_mgr.add_table(df, "test_table", "Test table...", s1_category_id=14)
    return ctx


@pytest.fixture
def mock_table():
    """Return a mock Table object."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    return Table(df, "test_table", "Test table...")


# sqlite db fixture
@pytest.fixture
def sqlite_test_db():
    """Return a SQLite database."""

    db_path = "tests/data/test.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE simple_table (
            a INTEGER,
            b INTEGER
        )
        """
    )
    c.execute("INSERT INTO simple_table VALUES (1, 4)")
    c.execute("INSERT INTO simple_table VALUES (2, 5)")
    c.execute("INSERT INTO simple_table VALUES (3, 6)")
    conn.commit()
    conn.close()
    return SQLiteAdapter(SQLiteConfig(file_path=db_path))
