"""This module contains all the commands that can be executed to transform a DataFrame."""

# flake8: noqa
from .add_column import AddColumnCommand
from .col_to_title_case import ColumnToTitleCaseCommand
from .find_column_duplicates import FindColumnDuplicatesCommand
from .remove_column import RemoveColumnCommand
from .rename_column import RenameColumnCommand
from .select_rows_by_value import SelectRowsByValueCommand
from .set_column_type import SetColumnTypeCommand
from .sort_rows import SortRowsCommand
from .split_address import SplitAddressLinesCommand


class Commands:
    """Container for all commands."""

    AddColumnCommand = AddColumnCommand
    ColumnToTitleCaseCommand = ColumnToTitleCaseCommand
    FindColumnDuplicatesCommand = FindColumnDuplicatesCommand
    RemoveColumnCommand = RemoveColumnCommand
    RenameColumnCommand = RenameColumnCommand
    SelectRowsByValueCommand = SelectRowsByValueCommand
    SetColumnTypeCommand = SetColumnTypeCommand
    SortRowsCommand = SortRowsCommand
    SplitAddressLinesCommand = SplitAddressLinesCommand
