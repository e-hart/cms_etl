"""Tests for the utils module."""

# pylint: disable=unsubscriptable-object, protected-access
from dataclasses import dataclass, field

import pandas as pd
from cms_etl.utils import (
    Pick,
    Stack,
    display_list,
    get_cmd_args,
    get_dtype_obj,
    select_from_list,
    truncate_list_items,
)
from pytest_mock import MockerFixture
from rich.table import Table


def test_select_from_list_valid_choice(mocker: MockerFixture):
    """Test selecting an item from a list."""
    mock_console = mocker.patch("cms_etl.utils.console")

    items = ["apple", "banana", "orange"]
    user_input = "2"  # Choose the second item
    expected_output = "banana"

    mock_console.input.return_value = user_input
    result = select_from_list(Pick.one, items)
    mock_console.print.assert_called()
    assert result == expected_output


def test_select_from_list_invalid_choice(mocker: MockerFixture):
    """Test selecting an item from a list."""
    mocker.patch("cms_etl.utils.console")

    items = ["apple", "banana", "orange"]
    user_input = "4"  # Choose an invalid item
    expected_output = None

    mocker.patch("cms_etl.utils.console.input", return_value=user_input)
    result = select_from_list(Pick.one, items)

    assert result == expected_output


def test_get_cmd_args():
    """Test the get_cmd_args function."""

    @dataclass
    class TestClass:
        """Test class."""

        arg1: int
        arg2: str
        table: str = field(default="TABLE", init=False)
        _cmd_args: list = field(default_factory=list, init=False)

    test_obj = TestClass(1, "test")
    cmd_args = get_cmd_args(test_obj)

    assert cmd_args == {"arg1": 1, "arg2": "test"}  # table and _cmd_args are excluded


def test_display_list(mocker: MockerFixture):
    """Test the display_list function."""
    mock_print = mocker.patch("cms_etl.utils.console.print")
    items = ["apple", "banana", "orange"]
    display_list(items)
    mock_print.assert_called()


def test_diplay_list_max_col_len(mocker: MockerFixture):
    """Test the display_list function with max_col_len."""
    mock_print = mocker.patch("cms_etl.utils.console.print")
    items = ["apple", "banana", "orange"]
    display_list(items, max_col_len=2)
    mock_print.assert_called()
    assert isinstance(mock_print.call_args_list[1][0][0], Table)


def test_display_list_max_item_len(mocker: MockerFixture):
    """Test the display_list function with max_item_len."""
    mock_print = mocker.patch("cms_etl.utils.console.print")
    items = ["apple", "banana", "orange", "me"]
    display_list(items, max_item_len=2)
    assert "ap..." in mock_print.call_args_list[1][0][0]
    assert "ba..." in mock_print.call_args_list[2][0][0]
    assert "or..." in mock_print.call_args_list[3][0][0]
    assert "me" in mock_print.call_args_list[4][0][0]
    assert "me..." not in mock_print.call_args_list[4][0][0]


def test_truncate_list_items():
    """Test the truncate_list_items function."""
    items = ["apple", "banana", "orange", "me"]
    trunc_items = truncate_list_items(items, 2)
    assert trunc_items == ["ap...", "ba...", "or...", "me"]


class TestStack:
    """Tests for the Stack class."""

    def test_push(self):
        """Test pushing an item onto the stack."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        assert stack._stack == [1, 2]

    def test_replace(self):
        """Test replacing the top item on the stack."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        stack.replace(3)
        assert stack._stack == [1, 3]

    def test_pop(self):
        """Test popping an item from the stack."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        item = stack.pop()
        assert item == 2
        assert stack._stack == [1]

    def test_peek(self):
        """Test peeking at the top item of the stack."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        item = stack.peek()
        assert item == 2
        assert stack._stack == [1, 2]

    def test_clear(self):
        """Test clearing the stack."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        stack.clear()
        assert stack._stack == []

    def test_is_empty(self):
        """Test checking if the stack is empty."""
        stack = Stack[int]()
        assert stack.is_empty
        stack.push(1)
        assert not stack.is_empty
        stack.pop()
        assert stack.is_empty

    def test_iter(self):
        """Test iterating over the stack."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        items = [item + 1 for item in stack]
        assert items == [2, 3, 4]

    def test_len(self):
        """Test getting the length of the stack."""
        stack = Stack[int]()
        stack.push(1)
        stack.push(2)
        assert len(stack) == 2


def test_get_dtype_class():
    """Test the get_dtype_class function."""
    int_dtype = get_dtype_obj("int")
    float_dtype = get_dtype_obj("float")
    str_dtype = get_dtype_obj("str")
    bool_dtype = get_dtype_obj("bool")

    assert int_dtype == pd.Int64Dtype()
    assert float_dtype == pd.Float64Dtype()
    assert str_dtype == pd.StringDtype()
    assert bool_dtype == pd.BooleanDtype()
