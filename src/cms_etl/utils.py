"""Menu utilities."""

import os
from dataclasses import fields
from typing import List, Optional, Type, TypeVar, Union, overload

import pandas as pd
from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table

console = Console()


def get_cmd_args(cmd):
    """Get the arguments of a command (excluding table) for serialization."""
    cmd_fields = fields(cmd)
    return {
        field.name: getattr(cmd, field.name)
        for field in cmd_fields
        if field.name not in ["table", "_cmd_args"]
    }


type DType = pd.Int64Dtype | pd.Float64Dtype | pd.StringDtype | pd.BooleanDtype


def get_dtype_obj(dtype_str: str) -> DType:
    """Get a specified pandas dtype object."""
    match dtype_str:
        case "int":
            return pd.Int64Dtype()
        case "float":
            return pd.Float64Dtype()
        case "str":
            return pd.StringDtype()
        case "bool":
            return pd.BooleanDtype()
        case _:
            raise ValueError(
                "Invalid data type string. Must be one of: 'int', 'float', 'str', 'bool'."
            )


# MARK: - Stack
class Stack[T]:
    """A stack implementation."""

    def __init__(self) -> None:
        self._stack: List[T] = []

    def push(self, item: T):
        """Push an item onto the stack."""
        self._stack.append(item)

    def replace(self, item: T):
        """Replace the top item on the stack."""
        self._stack[-1] = item

    def pop(self) -> T:
        """Pop an item off the stack."""
        return self._stack.pop()

    def peek(self) -> T:
        """Return the top item of the stack."""
        return self._stack[-1]

    def clear(self):
        """Clear the stack."""
        self._stack.clear()

    @property
    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self._stack) == 0

    def __len__(self):
        return len(self._stack)

    def __str__(self):
        return str(self._stack)

    def __repr__(self):
        return repr(self._stack)

    def __iter__(self):
        return iter(self._stack)


U = TypeVar("U", str, List, Optional[Union[str, List[str]]])


class Pick:
    """
    Return options for select_from_list.

    Class attributes:
    - one: Return a single item.
    - maybe_one: Return a single item or None.
    - many: Return a list of items.
    - maybe_many: Return a list of items or None.
    """

    one = str
    maybe_one = Optional[str]
    many = List[str]
    maybe_many = Optional[List[str]]


@overload
def select_from_list(
    return_type: Type[str],
    items: List[str],
    *,
    title: str = ...,
    prompt: str = ...,
    max_col_len: Optional[int] = ...,
    max_item_len: Optional[int] = ...,
    allow_none: bool = ...,
    allow_multiple: bool = False,
    allow_custom: bool = ...,
) -> str: ...


@overload
def select_from_list(
    return_type: Type[List],
    items: List[str],
    *,
    title: str = ...,
    prompt: str = ...,
    max_col_len: Optional[int] = ...,
    max_item_len: Optional[int] = ...,
    allow_none: bool = ...,
    allow_multiple: bool = True,
    allow_custom: bool = ...,
) -> List[str]: ...


@overload
def select_from_list(
    return_type: Type[Optional[Union[str, List[str]]]],
    items: List[str],
    *,
    title: str = ...,
    prompt: str = ...,
    max_col_len: Optional[int] = ...,
    max_item_len: Optional[int] = ...,
    allow_none: bool = True,
    allow_multiple: bool = ...,
    allow_custom: bool = ...,
) -> Optional[Union[str, List[str]]]: ...
# MARK: - Menu Utilities
def select_from_list(
    return_type: Type[U],
    items: List[str],
    *,
    title: str = "Select an item",
    prompt: str = "Enter choice: ",
    max_col_len: Optional[int] = None,
    max_item_len: Optional[int] = None,
    allow_none: bool = False,
    allow_multiple: bool = False,
    allow_custom: bool = False,
) -> U:
    """Select an item from a list."""

    display_list(items, title=title, max_col_len=max_col_len, max_item_len=max_item_len)

    console.print("\n")
    choice = console.input(prompt)

    if allow_multiple:
        choices = choice.split(",")
        choices = [c.strip() for c in choices if c.strip()]
        selected_items = []
        for choice in choices:
            if choice.isdigit():
                if 1 <= int(choice) <= len(items):
                    selected_items.append(items[int(choice) - 1])
                else:
                    console.print(f"Invalid choice: {choice}")
            elif allow_none and choice == "":
                continue
            elif not allow_none and choice == "":
                console.print(f"Invalid choice: {choice}")
            elif allow_custom:
                selected_items.append(choice)
            else:
                console.print(f"Invalid choice: {choice}")
        return selected_items  # type: ignore

    if choice.isdigit():
        if 1 <= int(choice) <= len(items):
            return items[int(choice) - 1]  # type: ignore
        console.print("Invalid choice.")
        return None  # type: ignore

    if allow_none and choice == "":
        return None  # type: ignore

    if not allow_none and choice == "":
        console.print("Invalid choice.")
        return None  # type: ignore

    if allow_custom:
        return choice  # type: ignore

    return None  # type: ignore


def display_list(
    items: List[str],
    *,
    title: str = "",
    max_col_len: int | None = None,
    max_item_len: int | None = None,
):
    """Display a list of items."""
    console.rule(title)

    trunc_items = truncate_list_items(items, max_item_len)
    numd_items = [f"[blue]{i}.[/blue] {item}" for i, item in enumerate(trunc_items, start=1)]

    if max_col_len is None:
        for item_str in numd_items:
            console.print(item_str)
    else:
        col_items = [
            numd_items[i : i + max_col_len]
            for i in range(0, len(numd_items), max_col_len or len(numd_items))
        ]

        grid = Table.grid(expand=True)
        grid.box = ROUNDED
        grid.border_style = "yellow"
        grid.show_edge = True

        for _ in col_items:
            grid.add_column()

        longest_col = max(len(col) for col in col_items)
        for i in range(longest_col):
            grid.add_row(*[col[i] if i < len(col) else "" for col in col_items])
        console.print(grid)

    console.print("\n")


def prompt_mysql_config():
    """Prompt the user for database configuration."""
    db_config = {
        "db_name": console.input("Database name (senior-one): ") or "senior-one",
        "user": console.input("Database user (root): ") or "root",
        "password": console.input("Database password (example): ") or "example",
        "host": console.input("Database host (localhost): ") or "localhost",
        "port": console.input("Database port (3306): ") or 3306,
    }
    return db_config


def prompt_sqlite_config():
    """Prompt the user for database configuration."""
    console.print(f"[bold]Current directory:[/bold]{os.getcwd()}")
    db_config = {
        "file_path": console.input("Database path (./data/senior-one.db): ")
        or "./data/senior-one.db",
        "if_not_exists": select_from_list(
            Pick.one, ["create", "error"], title="If file does not exist:"
        )
        or "error",
    }
    return db_config


def truncate_list_items(items: List[str], max_len: Optional[int]) -> List[str]:
    """Truncate list items to a maximum length."""
    # console.log("before", items)
    if max_len is not None:
        items = [item[:max_len] + ("..." if len(item) > max_len else "") for item in items]
    # console.log("after", items)
    return items


def isolate_addr_head(address: str) -> str:
    """Normalize an address string."""
    if address is None or pd.isna(address):
        return ""
    print(" ".join(address.split(" ")[0:2]))
    return " ".join(address.split(" ")[0:1])
