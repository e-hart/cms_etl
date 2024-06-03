"""Edit Table menu."""

from __future__ import annotations

import warnings
from functools import partial
from typing import TYPE_CHECKING

from pandasgui import show

from cms_etl.menu import BaseMenu, MenuOption
from cms_etl.table.commands import Commands
from cms_etl.table.render_table import render_table
from cms_etl.table.table import Table
from cms_etl.utils import Pick, console, display_list, select_from_list

if TYPE_CHECKING:
    from cms_etl.app_context import AppContext

display_cols = partial(display_list, max_col_len=20, max_item_len=26)
select_col = partial(select_from_list, max_col_len=20, max_item_len=26)


class EditTableMenu(BaseMenu):
    """Edit Table menu."""

    # MARK: - Menu Setup
    def __init__(self, ctx: AppContext, title: str, table: Table):
        super().__init__(ctx, title)
        self.table = table
        self.cmd_mgr = table.cmd_manager
        self.cmds = Commands()

    def _set_options(self):
        base_options = [
            MenuOption(name="Open in Viewer", action=self.open_in_viewer),
            MenuOption(name="Preview in Terminal", action=self.view_in_terminal),
            MenuOption(name="Add Columns", action=self.add_column),
            MenuOption(name="Select Columns", action=self.select_columns),
            MenuOption(name="Drop Columns", action=self.remove_columns),
            MenuOption(name="Rename Columns", action=self.rename_column),
            MenuOption(name="Filter Rows by Value", action=self.filter_rows),
            MenuOption(name="Sort on Column", action=self.sort_rows),
            MenuOption(name="Set Data Type of Column", action=self.set_data_type),
            MenuOption(name="Column to Title Case", action=self.column_to_title_case),
            MenuOption(name="Find Duplicates in Column", action=self.find_duplicates),
            MenuOption(name="View Metadata", action=self.view_metadata),
            MenuOption(name="Export to CSV", action=self.export_csv),
            MenuOption(name="Render to HTML", action=self.render_to_html),
        ]

        conditional_options = [
            (
                MenuOption(name="Save Commands as Macro", action=self.save_commands_as_macro)
                if self.cmd_mgr.can_undo
                else None
            ),
            (MenuOption(name="Undo", action=self.undo) if self.cmd_mgr.can_undo else None),
            (MenuOption(name="Redo", action=self.redo) if self.cmd_mgr.can_redo else None),
            (
                MenuOption(name="Apply Macro", action=self.run_macro)
                if not self.cmd_mgr.can_undo
                else None
            ),
            (
                MenuOption(name="Split Address Column", action=self.split_address)
                if self.table.metadata.get("source_type") == "cms"
                else None
            ),
        ]
        # Remove None values
        conditional_options = [option for option in conditional_options if option is not None]
        back_option = [MenuOption(name="Back", action=self.back)]
        self.options = base_options + conditional_options + back_option

    # MARK: - Menu Actions

    def undo(self):
        """Undo the last command."""
        self.cmd_mgr.undo()
        console.print(str(self.table))

    def redo(self):
        """Redo the last undone command."""
        self.cmd_mgr.redo()
        console.print(self.table)

    def _select_column(
        self, col_list: list[str], title_suff: str = "", prompt_suff: str = ""
    ) -> str:
        """Select a column from a list."""
        try:
            result = select_col(
                Pick.one,
                col_list,
                title="Select Column" f" {title_suff}" if title_suff else "",
                prompt=f"Enter index of column {prompt_suff}: ",
            )
            return result
        except (IndexError, ValueError):
            console.print("Invalid choice.")
            return ""

    def view_metadata(self):
        """View metadata for a Table."""
        console.print(self.table.metadata)
        console.print("Metadata displayed.")

    # MARK: - Macro Actions
    def save_commands_as_macro(self):
        """Save the commands as a macro."""
        macro_name = console.input("Enter a name for the macro: ")
        self.cmd_mgr.save_as_macro(macro_name)
        console.print(f"Commands saved as macro '{macro_name}'")

    def run_macro(self):
        """Apply a macro to a Table."""
        macros = self.cmd_mgr.list_macros()
        for i, macro in enumerate(macros, start=1):
            console.print(f"{i}. {macro}")

        print("\n")
        try:
            index = console.input("Enter index of macro to apply: ")
            macro_name = macros[int(index) - 1]

            self.cmd_mgr.run_macro(macro_name)

            console.print(
                f"Macro '{macro_name}' applied to Table '{self.table.name}' successfully."
            )
        except (IndexError, ValueError):
            console.print("Invalid choice.")

    # MARK: - View Actions
    def open_in_viewer(self):
        """Open the Table in the DataFrame Viewer."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            show(self.table.df)

    def view_in_terminal(self):
        """Preview the Table in the terminal."""
        self.clear()
        console.print(self.table)
        console.print(self.table.metadata)

    # MARK: - Edit Actions

    # MARK: - Add Columns
    def add_column(self):
        """Add columns to a Table."""
        cols = console.input("Enter columns to add (comma-separated): ").split(",")
        if not cols:
            console.print("No columns entered.")
            return

        for col in cols:
            cmd = self.cmds.AddColumnCommand(self.table, col.strip(), "")
            self.cmd_mgr.exec_cmd(cmd)

        console.print(
            f"Column(s) {', '.join([f'`{col}`' for col in cols])}"
            " added to Table '{self.table.name}'."
        )

    # MARK: - Select Columns
    def select_columns(self):
        """Select columns (dropping the rest)"""
        col_list = self.table.list_columns()
        try:
            cols_to_keep = select_col(
                Pick.many,
                col_list,
                title="Select Columns to Keep",
                prompt="Enter indices of columns to keep (comma-separated): ",
                allow_multiple=True,
            )
            if not cols_to_keep:
                raise ValueError("No columns selected.")
            cols_to_remove = list(set(col_list) - set(cols_to_keep))

            cmd = self.cmds.RemoveColumnCommand(self.table, cols_to_remove)
            self.cmd_mgr.exec_cmd(cmd)

            console.print(f"Success. Columns {cols_to_keep} selected in Table '{self.table.name}'.")

        except (IndexError, ValueError) as e:
            console.print(f"Invalid input: {e}")

    # MARK: - Drop Columns
    def remove_columns(self):
        """Remove columns from a Table."""
        col_list = self.table.list_columns()

        try:
            cols_to_remove = select_col(
                Pick.many,
                col_list,
                title="Select Columns to Remove",
                prompt="Enter indices of columns to remove (comma-separated): ",
                allow_multiple=True,
            )
            if isinstance(cols_to_remove, list):
                cols_to_remove = [col for col in cols_to_remove if col is not None]

            if cols_to_remove is None:
                raise ValueError("No columns selected.")

            cmd = self.cmds.RemoveColumnCommand(self.table, cols_to_remove)
            self.cmd_mgr.exec_cmd(cmd)

            console.print(
                f"Success. Columns {cols_to_remove} removed from Table '{self.table.name}'."
            )

        except (IndexError, ValueError) as e:
            console.print(f"Invalid input: {e}")

    # MARK: - Rename Columns
    def rename_column(self):
        """Rename columns in a Table."""
        col_list = self.table.list_columns()

        try:
            col_choice = select_col(
                Pick.many,
                col_list,
                title="Select Columns to Rename",
                prompt="Enter indices of columns to rename (comma-separated) or 'all': ",
                allow_multiple=True,
                allow_custom=True,
            )
            assert isinstance(col_choice, list)

            if col_choice != ["all"]:
                col_list = col_choice

            for column in col_list:
                new_name = console.input(f"Enter new name for column '{column}': ") or column
                if new_name is not None and column is not None:
                    cmd = self.cmds.RenameColumnCommand(self.table, column, new_name)
                    self.cmd_mgr.exec_cmd(cmd)

            console.print(f"Columns renamed in Table '{self.table.name}' successfully.")
        except (IndexError, ValueError):
            console.print("Invalid choice.")

    # MARK: - Filter/Sort Actions
    def filter_rows(self):
        """Filter rows in a Table."""
        columns = self.table.list_columns()

        try:
            col = self._select_column(columns)
            col_type = self.table.df[col].dtype

            val = console.input("Enter value to filter by: ")

            if col_type in ("int64", "float64") and not val.isnumeric():
                if val:
                    console.print(f"Invalid value for column '{col}'.")
                    return
                else:
                    console.print("No value entered.")
                    return

            match col_type:
                case "int64":
                    val = int(val)
                case "float64":
                    val = float(val)
                case _:
                    pass

            cmd = self.cmds.SelectRowsByValueCommand(self.table, col, val)
            self.cmd_mgr.exec_cmd(cmd)

            console.print(f"Rows filtered in Table '{self.table.name}' successfully.")
        except (IndexError, ValueError):
            console.print("Invalid choice.")

    def sort_rows(self):
        """Sort rows in a Table."""
        columns = self.table.list_columns()
        try:
            column = self._select_column(columns, title_suff="to Sort", prompt_suff="to sort by")

            ascending = console.input("Sort in ascending order? (y/n): ") or "y"

            cmd = self.cmds.SortRowsCommand(self.table, column, ascending == "y")
            self.cmd_mgr.exec_cmd(cmd)

            console.print(f"Rows sorted in Table '{self.table.name}' successfully.")
        except (IndexError, ValueError):
            console.print("Invalid choice.")

    # MARK: - Set Data Type
    def set_data_type(self):
        """Set the data type of a column in a Table."""
        columns = self.table.list_columns()

        try:
            column = self._select_column(
                columns,
                title_suff="to Set Data Type For",
                prompt_suff="to set data type for",
            )

            types = ["int", "float", "str", "bool"]

            data_type = select_from_list(
                Pick.one,
                types,
                title="Select Data Type",
                prompt="Enter index of data type: ",
            )
            assert isinstance(data_type, str)

            cmd = self.cmds.SetColumnTypeCommand(self.table, column, data_type)
            self.cmd_mgr.exec_cmd(cmd)

            console.print(
                f"Data type set for column '{column}' in Table '{self.table.name}' successfully."
            )
        except (IndexError, ValueError) as e:
            console.print("Invalid choice.", e)

    # MARK: - Split Address
    def split_address(self):
        """Split the address column into multiple columns."""
        self.clear()
        table_cols = self.table.list_columns()

        try:
            address_col = select_from_list(
                Pick.one,
                table_cols,
                title="Select the Address Column to Split",
                prompt="Enter index of address column: ",
            )
            assert isinstance(address_col, str)

            addr_line2_col = console.input(
                "Enter the index of the address_line2 column (or enter a name to create it): "
            )
            if addr_line2_col.isdigit():
                addr_line2_col = table_cols[int(addr_line2_col) - 1]
            elif not addr_line2_col:
                raise ValueError("No address_line2 column specified.")
            elif addr_line2_col not in table_cols:
                # add column after address column
                address_col_index = table_cols.index(address_col)
                cmd = self.cmds.AddColumnCommand(
                    self.table, addr_line2_col, "", after=table_cols[address_col_index]
                )
                self.cmd_mgr.exec_cmd(cmd)

            cmd = self.cmds.SplitAddressLinesCommand(self.table, address_col, addr_line2_col)
            self.cmd_mgr.exec_cmd(cmd)

            console.print(self.table.df[self.table.df[addr_line2_col].notnull()])
            console.print("Address column split success.")
        except (IndexError, ValueError):
            console.print("Invalid choice.")

    # MARK: - Column to Title Case
    def column_to_title_case(self):
        """Convert a columns values to title case."""
        table_cols = self.table.list_columns()
        col = self._select_column(table_cols)
        if col:
            try:
                cmd = self.cmds.ColumnToTitleCaseCommand(self.table, col)
                self.cmd_mgr.exec_cmd(cmd)
            except ValueError as e:
                console.log(e)
                return

            console.print(f"Column '{col}' converted to title case.")

    # MARK: - Export CSV
    def export_csv(self):
        """Export the Table to a CSV file."""
        self.clear()
        console.print(self.table)
        console.print("\n")

        path = (
            console.input(f"Name file ({self.table.name.replace(' ', '_')}): ")
            or f"{self.table.name.replace(' ', '_')}"
        )
        self.table.df.to_csv(f"{path}.csv", index=False)

        console.print(f"Table '{self.table.name}' exported to '{path}.csv'.")

    def render_to_html(self):
        """Render the table to HTML."""
        if len(self.table.df) > 2500:
            console.print("Table is too large to render to HTML. Please filter the table first.")
            return
        render_table(self.table, to="html")

    def find_duplicates(self):
        """Find duplicates in a column."""
        table_cols = self.table.list_columns()
        col = self._select_column(table_cols)
        if col:
            cmd = self.cmds.FindColumnDuplicatesCommand(self.table, col)
            self.cmd_mgr.exec_cmd(cmd)
            console.print(f"Duplicates found in column '{col}'.")
