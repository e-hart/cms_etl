"""Menu Controller module"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Type

from cms_etl.menu.base_menu import BaseMenu
from cms_etl.menu.menus import Menus
from cms_etl.utils import Stack, console

if TYPE_CHECKING:
    from cms_etl.app_context import AppContext


@dataclass
class MenuController:
    """Menu Controller."""

    ctx: AppContext
    menus: Menus = field(init=False, default_factory=Menus)
    menu_stack: Stack[Tuple[Type[BaseMenu], List, Dict[str, Any]]] = field(
        init=False, default_factory=Stack
    )

    def main_loop(self):
        """Run the menu controller."""
        while not self.menu_stack.is_empty:
            menu_class, args, kwargs = self.menu_stack.peek()
            menu = menu_class(self.ctx, *args, **kwargs)
            menu.run()

    def back(self):
        """Return to the previous menu."""
        console.clear()
        self.menu_stack.pop()

    def open_menu(self, menu_class: Type[BaseMenu], *args, **kwargs):
        """Change the current menu."""
        console.clear()
        if not issubclass(menu_class, BaseMenu):
            raise ValueError("Invalid menu class.")
        self.menu_stack.push((menu_class, list(args), kwargs))

    def run_main_menu(self):
        """Run the Main Menu."""
        self.open_menu(self.menus.main_menu, "Main Menu")
        self.main_loop()

    @property
    def current_menu(self):
        """Return the current menu."""
        return self.menu_stack.peek()[0]
