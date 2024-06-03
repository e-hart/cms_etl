"""Manage commands."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict

from cms_etl.table.base_command import Command
from cms_etl.table.commands import Commands
from cms_etl.utils import Stack

if TYPE_CHECKING:
    from cms_etl.table.table import Table


@dataclass
class CommandData:
    """A dataclass for serialized command data after loading."""

    command: str
    args: Dict[str, Any]


@dataclass
class CommandManager:
    """Manage commands."""

    table: Table
    _commands: Stack[Command] = field(init=False, default_factory=Stack)
    _redo_stack: Stack[Command] = field(init=False, default_factory=Stack)
    _cmds: Commands = field(init=False, default_factory=Commands)

    def exec_cmd(self, command: Command, track: bool = True):
        """Execute a command. Set track to False to prevent the command from being tracked."""
        command.execute()
        if track:
            self._commands.push(command)
            self._redo_stack.clear()

    def redo(self):
        """Redo the last undone command."""
        command = self._redo_stack.pop()
        self._commands.push(command)
        command.execute()

    def undo(self):
        """Undo the last command."""
        command = self._commands.pop()
        self._redo_stack.push(command)
        command.undo()

    @property
    def can_undo(self):
        """Check if there are actions to undo."""
        return len(self._commands) > 0

    @property
    def can_redo(self):
        """Check if there are actions to redo."""
        return len(self._redo_stack) > 0

    def save_as_macro(self, name: str):
        """Save a sequence of commands as a macro."""
        macro = [cmd.serialize() for cmd in self._commands]
        macro_json = json.dumps(macro)
        macro_dir = Path(os.curdir) / "macros"
        macro_dir.mkdir(exist_ok=True)
        macro_path = macro_dir / f"{name}.json"
        # {cwd}/macros/{name}.json"

        with open(macro_path, "w", encoding="utf-8") as f:
            f.write(macro_json)

    def list_command_class_names(self):
        """List the names of the command classes."""
        return [cmd.__name__ for cmd in Commands.__dict__.values() if issubclass(cmd, Command)]

    def deserialize_command(self, serial_cmd: CommandData) -> Command:
        """Deserialize a command."""
        cmd_name, args = serial_cmd.command, serial_cmd.args
        return getattr(self._cmds, cmd_name)(self.table, **args)

    def list_macros(self):
        """List the available macros."""
        macro_dir = Path(os.curdir) / "macros"
        return [macro.split(".")[0] for macro in os.listdir(macro_dir) if macro.endswith(".json")]

    def run_macro(self, name: str):
        """Run a macro."""
        macro_path = Path(os.curdir) / "macros" / f"{name}.json"
        with open(
            macro_path,
            "r",
            encoding="utf-8",
        ) as f:
            macro = json.load(f)
            for cmd in macro:
                command = self.deserialize_command(CommandData(**cmd))
                self.exec_cmd(command)
