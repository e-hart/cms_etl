"""Test for the CommandManager class."""

# pylint: disable=protected-access

import json
import os
from unittest.mock import MagicMock

import pandas as pd
import pytest
from cms_etl.table import Table
from cms_etl.table.base_command import Command
from cms_etl.table.command_manager import CommandData, CommandManager
from pytest_mock import MockerFixture


class TestCommandManager:
    """Tests for the CommandManager class."""

    @pytest.fixture
    def table(self):
        """Return a Table instance."""
        df = pd.DataFrame()
        return Table(df, "test_table", "test table")

    @pytest.fixture
    def command_manager(self, table: Table):
        """Return a CommandManager instance."""
        return CommandManager(table)

    class MockCommand(Command):
        """A test command."""

        def execute(self): ...

        def undo(self): ...

    @pytest.fixture
    def mock_command(self, command_manager: CommandManager, mocker: MockerFixture):
        """Return a mock command."""
        command = self.MockCommand(command_manager.table)
        # mock execute and undo methods
        mock_cmd = mocker.MagicMock(spec=command)

        return mock_cmd

    def test_execute_command(
        self, command_manager: CommandManager, mock_command: MagicMock | MagicMock
    ):
        """Test the execute_command method."""
        command_manager.exec_cmd(mock_command)
        mock_command.execute.assert_called_once()
        assert len(command_manager._commands) == 1
        assert len(command_manager._redo_stack) == 0

    def test_undo(self, command_manager: CommandManager, mock_command: MagicMock | MagicMock):
        """Test the undo method."""
        command_manager.exec_cmd(mock_command)
        command_manager.undo()
        mock_command.undo.assert_called_once()
        assert len(command_manager._commands) == 0

    def test_redo(self, command_manager: CommandManager, mock_command: MagicMock | MagicMock):
        """Test the redo method."""
        command_manager.exec_cmd(mock_command)
        mock_command.execute.assert_called_once()
        assert len(command_manager._commands) == 1
        assert len(command_manager._redo_stack) == 0
        command_manager.undo()
        assert len(command_manager._commands) == 0
        assert len(command_manager._redo_stack) == 1
        command_manager.redo()
        assert mock_command.execute.call_count == 2  # pylint: disable=no-member
        assert len(command_manager._commands) == 1
        assert len(command_manager._redo_stack) == 0

    def test_can_undo(self, command_manager: CommandManager, mock_command: MagicMock | MagicMock):
        """Test the can_undo property."""
        assert not command_manager.can_undo
        command_manager.exec_cmd(mock_command)
        assert command_manager.can_undo
        command_manager.undo()
        assert not command_manager.can_undo

    def test_can_redo(self, command_manager: CommandManager, mock_command: MagicMock | MagicMock):
        """Test the can_redo property."""
        assert not command_manager.can_redo
        command_manager.exec_cmd(mock_command)
        assert not command_manager.can_redo
        command_manager.undo()
        assert command_manager.can_redo
        command_manager.redo()
        assert not command_manager.can_redo

    def test_list_command_class_names(self, command_manager: CommandManager):
        """Test the list_command_class_names method."""
        assert command_manager.list_command_class_names() == [
            "AddColumnCommand",
            "ColumnToTitleCaseCommand",
            "FindColumnDuplicatesCommand",
            "RemoveColumnCommand",
            "RenameColumnCommand",
            "SelectRowsByValueCommand",
            "SetColumnTypeCommand",
            "SortRowsCommand",
            "SplitAddressLinesCommand",
        ]

    def test_deserialize_command(self, command_manager: CommandManager):
        """Test the deserialize_command method."""
        serial_cmd = CommandData(
            "FindColumnDuplicatesCommand",
            {"col_name": "test_col"},
        )
        command = command_manager.deserialize_command(serial_cmd)
        assert isinstance(command, Command)
        assert command.__class__.__name__ == "FindColumnDuplicatesCommand"
        assert command._cmd_args["col_name"] == "test_col"

    def test_list_macros(self, command_manager: CommandManager):
        """Test the list_macros method."""
        if not os.path.exists("macros"):
            os.makedirs("macros")
        with open("macros/temp_test.json", "w", encoding="utf-8") as f:
            f.write("[]")
        assert "temp_test" in command_manager.list_macros()
        # cleanup
        os.remove("macros/temp_test.json")
        assert not os.path.exists("macros/temp_test.json")

    def test_run_macro(self, command_manager: CommandManager):
        """Test the run_macro method."""
        assert command_manager.table.df.empty
        command_manager.table.df = pd.DataFrame({"existing_col": [1, 2, 3]})
        assert len(command_manager.table.df.columns) == 1
        if not os.path.exists("macros"):
            os.makedirs("macros")
        with open("macros/temp_test.json", "w", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    [
                        {
                            "command": "AddColumnCommand",
                            "args": {"col_name": "test_col", "fill_value": 0},
                        }
                    ]
                )
            )
        command_manager.run_macro("temp_test")
        assert len(command_manager.table.df.columns) == 2
        assert "test_col" in command_manager.table.df.columns
        # cleanup
        os.remove("macros/temp_test.json")
        assert not os.path.exists("macros/temp_test.json")

    def test_save_as_macro(self, command_manager: CommandManager):
        """Test the save_as_macro method."""
        if not os.path.exists("macros"):
            os.makedirs("macros")
        command_manager.table.df = pd.DataFrame({"existing_col": [1, 2, 3]})
        command_manager.exec_cmd(
            command_manager.deserialize_command(
                CommandData(
                    "AddColumnCommand",
                    {"col_name": "test_col", "fill_value": 0},
                )
            )
        )
        command_manager.save_as_macro("temp_test")
        assert os.path.exists("macros/temp_test.json")
        with open("macros/temp_test.json", "r", encoding="utf-8") as f:
            macro = json.load(f)
        assert len(macro) == 1
        assert macro[0]["command"] == "AddColumnCommand"
        assert macro[0]["args"] == {
            "col_name": "test_col",
            "fill_value": 0,
            "after": None,
            "before": None,
        }
        # cleanup
        os.remove("macros/temp_test.json")
        assert not os.path.exists("macros/temp_test.json")
