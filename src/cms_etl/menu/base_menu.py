"""Base class for menus."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, List, TypeVar

from cms_etl.utils import console, display_list

if TYPE_CHECKING:
    from cms_etl.app_context import AppContext

T = TypeVar("T")


@dataclass(kw_only=True)
class MenuOption[T]:
    """Menu Option."""

    name: str
    action: Callable[[], T]


@dataclass
class BaseMenu(ABC):
    """Base class for menus."""

    ctx: AppContext
    title: str
    options: List[MenuOption] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.menus = self.ctx.menu_ctrlr.menus

    @abstractmethod
    def _set_options(self):
        """Set the menu options."""

    def display(self):
        """Display the menu."""
        display_list(
            [option.name for option in self.options],
            title=self.title,
            max_col_len=6 if len(self.options) > 12 else None,
        )

    def run(self):
        """Run the menu."""
        self._set_options()
        self.display()
        try:
            choice = int(self.get_choice())
            self.options[choice - 1].action()
        except (IndexError, ValueError):
            console.print("Invalid choice.")

    def back(self):
        """Return to the previous menu."""
        self.ctx.menu_ctrlr.back()

    def clear(self):
        """Clear the console."""
        console.clear()

    def get_choice(self):
        """Get the user's choice."""
        choice = console.input("Enter choice: ")
        return choice
